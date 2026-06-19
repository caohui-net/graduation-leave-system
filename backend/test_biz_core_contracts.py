"""
B2 兼容合约验收测试 — graduation-leave-system × biz-core
按 docs/compatibility-contract.md 清单逐项验证
"""
import pytest
from unittest.mock import MagicMock, patch
from django.test import RequestFactory


# ─── 合约1：import 全部子包 ───────────────────────────────────────────────────
class TestContract1Import:
    def test_all_modules_importable(self):
        import biz_core.feature_flags.service
        import biz_core.audit.service
        import biz_core.rbac.service
        import biz_core.notify.service
        import biz_core.export.service
        import biz_core.workflow.service
        import biz_core.attachments.service
        import biz_core.healthcheck.views


# ─── 合约2+3：migration 隔离 ──────────────────────────────────────────────────
class TestContract23Migration:
    def test_biz_app_labels_independent(self):
        from django.apps import apps
        biz_labels = {
            "biz_feature_flags", "biz_audit", "biz_rbac",
            "biz_notify", "biz_export", "biz_workflow",
            "biz_attachments", "biz_healthcheck",
        }
        installed = {app.label for app in apps.get_app_configs()}
        assert biz_labels.issubset(installed)

    def test_no_cross_app_migration_deps(self):
        from django.db.migrations.loader import MigrationLoader
        loader = MigrationLoader(None, ignore_no_migrations=True)
        for (app, _), migration in loader.disk_migrations.items():
            if not app.startswith("biz_"):
                continue
            for dep_app, _ in migration.dependencies:
                assert dep_app.startswith("biz_") or dep_app in (
                    "contenttypes", "auth"
                ), f"biz_core migration {app} depends on {dep_app}"


# ─── 合约5：User identity（无直接 FK）─────────────────────────────────────────
class TestContract5UserIdentity:
    def test_auditlog_user_id_is_charfield(self):
        from biz_core.audit.models import AuditLog
        field = AuditLog._meta.get_field("user_id")
        assert field.get_internal_type() == "CharField"

    def test_workflowinstance_submitter_is_charfield(self):
        from biz_core.workflow.models import WorkflowInstance
        field = WorkflowInstance._meta.get_field("submitter_id")
        assert field.get_internal_type() == "CharField"

    def test_attachment_owner_is_charfield(self):
        from biz_core.attachments.models import Attachment
        field = Attachment._meta.get_field("owner_id")
        assert field.get_internal_type() == "CharField"


# ─── 合约6：feature_flags ─────────────────────────────────────────────────────
@pytest.mark.django_db
class TestContract6FeatureFlags:
    def test_flag_enabled_global(self):
        from biz_core.feature_flags.models import FeatureFlag
        from biz_core.feature_flags.service import flag_enabled, invalidate_flag
        FeatureFlag.objects.create(
            name="export_excel", namespace="graduation_leave", enabled=True
        )
        assert flag_enabled("export_excel", namespace="graduation_leave") is True

    def test_flag_disabled_by_default(self):
        from biz_core.feature_flags.service import flag_enabled
        assert flag_enabled("nonexistent_flag", namespace="graduation_leave") is False

    def test_cache_invalidation(self):
        from biz_core.feature_flags.models import FeatureFlag
        from biz_core.feature_flags.service import flag_enabled, invalidate_flag
        FeatureFlag.objects.create(
            name="batch_approval", namespace="graduation_leave", enabled=True
        )
        flag_enabled("batch_approval", namespace="graduation_leave")  # populate cache
        FeatureFlag.objects.filter(name="batch_approval", namespace="graduation_leave").update(enabled=False)
        invalidate_flag("batch_approval", namespace="graduation_leave")
        assert flag_enabled("batch_approval", namespace="graduation_leave") is False


# ─── 合约7：audit 写入 ────────────────────────────────────────────────────────
@pytest.mark.django_db
class TestContract7Audit:
    def test_audit_log_written_with_correct_fields(self):
        from biz_core.audit.service import AuditService
        from biz_core.audit.models import AuditLog
        log = AuditService.log(
            action="leave.submit",
            user_id=42,
            obj_type="application",
            obj_id=1,
            ip_address="10.0.0.1",
        )
        assert log.user_id == "42"
        assert log.action == "leave.submit"
        assert log.obj_type == "application"
        assert log.ip_address == "10.0.0.1"
        assert AuditLog.objects.count() == 1


# ─── 合约8+9：notify 幂等 + 副作用隔离 ───────────────────────────────────────
class TestContract89Notify:
    def test_notify_idempotency(self):
        from biz_core.notify import service as svc
        from biz_core.notify.service import NotifyService
        from django.core.cache import cache
        cache.clear()
        mock_ch = MagicMock()
        mock_ch.send.return_value = True
        with patch.object(svc, "_CHANNELS", [mock_ch]):
            NotifyService.send("1", "leave_approved", idempotency_key="app-1-approved")
            NotifyService.send("1", "leave_approved", idempotency_key="app-1-approved")
        assert mock_ch.send.call_count == 1
        cache.clear()

    def test_notify_failure_does_not_raise(self):
        from biz_core.notify import service as svc
        from biz_core.notify.service import NotifyService
        mock_ch = MagicMock()
        mock_ch.send.side_effect = Exception("channel down")
        with patch.object(svc, "_CHANNELS", [mock_ch]):
            result = NotifyService.send("1", "leave_approved")
        assert result is False  # 失败返回 False，不抛异常


# ─── 合约10：export 输出格式 ──────────────────────────────────────────────────
class TestContract10Export:
    def test_xlsx_is_valid_zip(self):
        from biz_core.export.service import ExportService
        rows = [{"applicant": "张三", "days": 3, "status": "approved"}]
        data = ExportService.export(rows, format="xlsx")
        assert data[:4] == b"PK\x03\x04"  # xlsx = ZIP magic bytes

    def test_formula_injection_sanitized(self):
        from biz_core.export.service import ExportService
        rows = [{"reason": "=DANGEROUS()"}]
        csv_data = ExportService.export(rows, format="csv").decode("utf-8-sig")
        assert "'=DANGEROUS()" in csv_data


# ─── 合约11：workflow 状态转换 ─────────────────────────────────────────────────
@pytest.mark.django_db
class TestContract11Workflow:
    def test_leave_approval_flow(self):
        from biz_core.workflow.service import WorkflowService
        from biz_core.workflow.models import WorkflowInstance
        inst = WorkflowService.submit(
            obj_type="application", obj_id=1, submitter_id=100,
            steps=[
                {"approver_id": "201", "label": "宿管员"},
                {"approver_id": "202", "label": "辅导员"},
                {"approver_id": "203", "label": "学工部"},
            ],
        )
        assert inst.status == WorkflowInstance.PENDING
        WorkflowService.approve(inst.pk, approver_id="201")
        WorkflowService.approve(inst.pk, approver_id="202")
        inst = WorkflowService.approve(inst.pk, approver_id="203")
        assert inst.status == WorkflowInstance.APPROVED

    def test_rejection_terminates_flow(self):
        from biz_core.workflow.service import WorkflowService
        from biz_core.workflow.models import WorkflowInstance
        inst = WorkflowService.submit(
            obj_type="application", obj_id=2, submitter_id=100,
            steps=[{"approver_id": "201"}, {"approver_id": "202"}],
        )
        inst = WorkflowService.reject(inst.pk, approver_id="201", comment="材料不完整")
        assert inst.status == WorkflowInstance.REJECTED


# ─── 合约13：healthcheck ──────────────────────────────────────────────────────
@pytest.mark.django_db
class TestContract13Healthcheck:
    def test_liveness(self):
        from biz_core.healthcheck.views import liveness
        rf = RequestFactory()
        resp = liveness(rf.get("/healthz"))
        assert resp.status_code == 200

    def test_readiness_db_ok(self):
        from biz_core.healthcheck.views import readiness
        import json
        rf = RequestFactory()
        resp = readiness(rf.get("/readyz"))
        data = json.loads(resp.content)
        assert data["status"] == "ok"
        assert data["db"] == "ok"
