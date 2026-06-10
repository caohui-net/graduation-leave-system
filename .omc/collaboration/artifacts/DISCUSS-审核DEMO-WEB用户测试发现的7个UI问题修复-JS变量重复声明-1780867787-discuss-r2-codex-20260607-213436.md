
            // For dean: group by application_id to avoid duplicates (cross-page
 deduplication)
            if (currentUser && currentUser.role === 'dean') {
                const appMap = new Map();
                filtered.forEach(approval => {
                    const appId = approval.application?.id;
                    if (appId && !deanDisplayedApps.has(appId) && !appMap.has(ap
pId)) {
                        appMap.set(appId, approval);
                        deanDisplayedApps.add(appId); // Track globally
                    }
                });
                filtered = Array.from(appMap.values());
            }

            filtered.forEach(approval => {
                const application = approval.application || {};

                // Use approval decision for status tag (more accurate for dean/
approval views)
                const decision = approval.decision || 'pending';
                const step = decisionMap[decision] ? decisionMap[decision].text
: decision;
                const tagCls = decisionMap[decision] ? decisionMap[decision].cls
 : 'tag-pending';

                htmlStr += '<div class="card" onclick="openApproval(\'' + approv
al.id + '\')" style="cursor: pointer;">' +
                  '<div class="flex-row justify-between align-center" style="mar
gin-bottom: 8px;">' +
                    '<span style="font-size: 16px; font-weight: bold;">申请 ' +
(application.id ? application.id.substring(0,8) : approval.id.substring(0,8)) +
'</span>' +
                    '<span class="tag ' + tagCls + '">' + step + '</span>' +
                  '</div>' +
                  '<div style="margin-bottom: 4px;">' +
                    '<span style="font-size: 14px; color: #999; margin-right: 8p
x;">学生:</span>' +
                    '<span style="font-size: 14px; color: #333;">' + (applicatio
n.student_name || '-') + ' (' + (application.student_id || '-') + ')</span>' +
                  '</div>';

                // Show approver and decision time for decided approvals
                if (approval.decision === 'approved' || approval.decision === 'r
ejected') {
                    // Extract real approver name from comment if auto-completed
                    let realApprover = approval.approver_name || '-';
                    if (approval.comment && approval.comment.includes('已由')) {
                        const match = approval.comment.match(/已由(.+?)完成审批/
);
                        if (match) {
                            realApprover = match[1];
                        }
                    }

                    htmlStr += '<div style="margin-bottom: 4px;">' +
                      '<span style="font-size: 14px; color: #999; margin-right:
8px;">审批人:</span>' +
                      '<span style="font-size: 14px; color: #333;">' + realAppro
ver + '</span>' +
                    '</div>';
                    if (approval.decided_at) {
                        htmlStr += '<div style="margin-bottom: 4px;">' +
                          '<span style="font-size: 14px; color: #999; margin-rig
ht: 8px;">审批时间:</span>' +
                          '<span style="font-size: 14px; color: #333;">' + new D
ate(approval.decided_at).toLocaleString() + '</span>' +
                        '</div>';
                    }
                }

                htmlStr += '<div style="margin-top: 8px; padding-top: 8px; borde
r-top: 1px solid #f0f0f0;">' +
                    '<span style="font-size: 12px; color: #999;">创建: ' + new D
ate(approval.created_at || application.created_at).toLocaleString() + '</span>'
+
                  '</div>' +
                '</div>';
            });

            if (append) {
                listContainer.innerHTML += htmlStr;
            } else {
                listContainer.innerHTML = htmlStr;
            }

            approvalOffset += filtered.length;
            approvalHasMore = data.count > approvalOffset;

            if (loadMoreBtn) {
                loadMoreBtn.style.display = approvalHasMore ? 'block' : 'none';
            }
        } else {
            if (!append) {
                listContainer.innerHTML = '<div style="text-align:center; paddin
g: 20px; color:#999;">暂无数据</div>';
            }
            if (loadMoreBtn) {
                loadMoreBtn.style.display = 'none';
            }
        }
    }

    function filterApprovals(filter) {
        currentFilter = filter;

        // Update tab active state
        const tabs = document.querySelectorAll('#approval-tabs .nav-tab');
        tabs.forEach((tab, index) => {
            tab.classList.remove('active');
            if ((filter === 'all' && index === 0) ||
                (filter === 'pending' && index === 1) ||
                (filter === 'decided' && index === 2)) {
                tab.classList.add('active');
            }
        });

        // Reload list with filter
        if (currentUser && currentUser.role === 'student') {
            loadMyApplications();
        } else {
            loadApprovals();
        }
    }

    let currentApprovalId = null;
    async function openApproval(id) {
        currentApprovalId = id;
        showScreen(2);

        const res = await fetch(API_BASE_URL + '/approvals/' + id + '/', {
            headers: getAuthHeaders()
        });
        if (res.ok) {
            const detail = await res.json();

            const appRes = await fetch(API_BASE_URL + '/applications/' + detail.
application_id + '/', {
                headers: getAuthHeaders()
            });
            const appData = appRes.ok ? await appRes.json() : null;

            // Fetch attachments
            const attachments = await apiGetAttachments(detail.application_id);

            const container = document.querySelector('#screen-2');

            const basicInfoHtml = '<div class="card">' +
                '<div style="font-size: 16px; font-weight: bold; margin-bottom:
10px;">基本信息</div>' +
                '<div style="display: flex; margin-bottom: 8px;">' +
                  '<span style="font-size: 14px; color: #999; width: 80px;">申请
ID:</span>' +
                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (det
ail.application_id || detail.id.substring(0,8)) + '</span>' +
                '</div>' +
                '<div style="display: flex; margin-bottom: 8px;">' +
                  '<span style="font-size: 14px; color: #999; width: 80px;">学生
:</span>' +
                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (det
ail.student_name || '-') + ' (' + (detail.student_id || '-') + ')</span>' +
                '</div>' +
                '<div style="display: flex; margin-bottom: 8px;">' +
                  '<span style="font-size: 14px; color: #999; width: 80px;">联系
电话:</span>' +
                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (det
ail.contact_phone || '-') + '</span>' +
                '</div>' +
                '<div style="display: flex; margin-bottom: 8px;">' +
                  '<span style="font-size: 14px; color: #999; width: 80px;">申请
原因:</span>' +
                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (det
ail.reason || '无') + '</span>' +
                '</div>' +
              '</div>';

            // Generate attachment HTML
            let attachmentHtml = '';
            if (attachments && attachments.length > 0) {
                attachmentHtml = '<div class="card"><div style="font-size: 16px;
 font-weight: bold; margin-bottom: 10px;">附件材料</div>';
                attachments.forEach(att => {
                    attachmentHtml += '<div style="display: flex; align-items: c
enter; padding: 8px 0; border-bottom: 1px solid #f0f0f0;">' +
                        '<span style="font-size: 14px; color: #333; flex: 1;">'
+ (att.original_filename || att.file) + '</span>' +
                        '<a href="' + att.file + '" download style="font-size: 1
4px; color: var(--primary-color); text-decoration: none;">下载</a>' +
                    '</div>';
                });
                attachmentHtml += '</div>';
            }

            // 动态生成审批时间轴
            const timelineHtml = generateTimeline(detail, appData);

            const cards = container.querySelectorAll('.card');
            if (cards.length > 0) {
                cards[0].outerHTML = basicInfoHtml;
            }
            if (cards.length > 1) {
                if (attachmentHtml) {
                    cards[1].outerHTML = attachmentHtml + timelineHtml;
                } else {
                    cards[1].outerHTML = timelineHtml;
                }
            }
        }
    }

    function generateTimeline(detail, appData) {
        const stepNames = {
            'dorm_manager': '宿管员审批',
            'counselor': '辅导员审批',
            'dean': '学工部审批'
        };

        const appStatus = appData ? appData.status : detail.step;

        // Filter workflow based on current user role
        let workflow = ['dorm_manager', 'counselor', 'dean'];
        if (currentUser && currentUser.role === 'dorm_manager') {
            workflow = ['dorm_manager'];
        } else if (currentUser && currentUser.role === 'counselor') {
            workflow = ['dorm_manager', 'counselor'];
        }
        // dean/admin sees all steps (default)

        // Calculate current level index
        let currentLevel;
        if (appStatus === 'approved') {
            currentLevel = workflow.length;
        } else if (appStatus === 'rejected') {
            currentLevel = workflow.indexOf(detail.step);
        } else if (appStatus.startsWith('pending_')) {
            const pendingStep = appStatus.replace('pending_', '');
            currentLevel = workflow.indexOf(pendingStep);
        } else {
            currentLevel = -1;
        }

        let html = '<div class="card"><div style="font-size: 16px; font-weight:
bold; margin-bottom: 10px;">审批记录</div>';

        for (let i = workflow.length - 1; i >= 0; i--) {
            const step = workflow[i];
            const stepName = stepNames[step];
            const isLast = i === 0;

            let state, tagText, tagCls, dotBg, dotBorder, showConnector;

            // Check if this is the current approval's step
            if (step === detail.step) {
                if (detail.decision === 'approved') {
                    state = 'approved';
                    tagText = '已通过';
                    tagCls = 'tag-approved';
                    dotBg = 'var(--status-success)';
                    dotBorder = 'var(--status-success)';
                } else if (detail.decision === 'rejected') {
                    state = 'rejected';
                    tagText = '已驳回';
                    tagCls = 'tag-rejected';
                    dotBg = 'var(--status-error)';
                    dotBorder = 'var(--status-error)';
                } else {
                    state = 'pending';
                    tagText = '待审批';
                    tagCls = 'tag-pending';
                    dotBg = 'white';
                    dotBorder = 'var(--primary-color)';
                }
                showConnector = !isLast;
            } else if (i < currentLevel || appStatus === 'approved') {
                state = 'approved';
                tagText = '已通过';
                tagCls = 'tag-approved';
                dotBg = 'var(--status-success)';
                dotBorder = 'var(--status-success)';
                showConnector = !isLast;
            } else if (i === currentLevel && appStatus !== 'rejected') {
                state = 'pending';
                tagText = '待审批';
                tagCls = 'tag-pending';
                dotBg = 'white';
                dotBorder = 'var(--primary-color)';
                showConnector = !isLast;
            } else {
                state = 'future';
                tagText = '未开始';
                tagCls = 'tag';
                dotBg = '#e8e8e8';
                dotBorder = '#e8e8e8';
                showConnector = !isLast;
            }

            html += '<div style="position: relative; padding-left: 30px;' + (isL
ast ? '' : ' margin-bottom: 20px;') + '">' +
              '<div style="position: absolute; left: 10px; top: 4px; width: 10px
; height: 10px; border-radius: 50%; background: ' + dotBg + '; border: 2px solid
 ' + dotBorder + ';"></div>';

            if (showConnector) {
                html += '<div style="position: absolute; left: 14px; top: 16px;
bottom: -20px; width: 1px; background: #e8e8e8;"></div>';
            }

            html += '<div class="flex-row justify-between align-center" style="m
argin-bottom: 6px;">' +
                '<span style="font-size: 15px; font-weight: 600;">' + stepName +
 '</span>' +
                '<span class="tag ' + tagCls + '">' + tagText + '</span>' +
              '</div>';

            if (state === 'approved' || state === 'pending' || state === 'reject
ed') {
                if (detail.step === step) {
                    html += '<div style="font-size: 13px; color: #666;">审批人:
' + (detail.approver_name || '待分配') + '</div>';
                    if (detail.decided_at) {
                        html += '<div style="font-size: 13px; color: #666;">时间
: ' + detail.decided_at + '</div>';
                    }
                    if (detail.comment) {
                        html += '<div style="font-size: 13px; color: #666; margi
n-top: 4px;">意见: ' + detail.comment + '</div>';
                    }
                }
            }

            html += '</div>';
        }

        html += '<div style="position: relative; padding-left: 30px; margin-top:
 20px;">' +
          '<div style="position: absolute; left: 10px; top: 4px; width: 10px; he
ight: 10px; border-radius: 50%; background: var(--status-success); border: 2px s
olid var(--status-success);"></div>' +
          '<div class="flex-row justify-between align-center" style="margin-bott
om: 6px;">' +
            '<span style="font-size: 15px; font-weight: 600;">提交申请</span>' +
            '<span class="tag tag-approved">已完成</span>' +
          '</div>' +
          '<div style="font-size: 13px; color: #666;">学生已提交</div>' +
        '</div></div>';

        return html;
    }

    async function doApprove() {
        if(!currentApprovalId) return;
        const comment = document.getElementById('approvalComment').value;
        const btn = event?.target || document.querySelector('#approval-actions .
btn-primary');

        const originalText = btn.textContent;
        btn.disabled = true;
        btn.textContent = '处理中...';

        try {
            const ok = await apiApprove(currentApprovalId, comment);
            if(ok) { showToast('审批通过', 'success'); showScreen(1); loadApprov
als(); }
            else { showToast('审批失败', 'error'); }
        } finally {
            btn.disabled = false;
            btn.textContent = originalText;
        }
    }

    async function doReject() {
        if(!currentApprovalId) return;
        const comment = document.getElementById('approvalComment').value;
        const btn = event?.target || document.querySelector('#approval-actions .
btn-outline');

        const originalText = btn.textContent;
        btn.disabled = true;
        btn.textContent = '处理中...';

        try {
            const ok = await apiReject(currentApprovalId, comment);
            if(ok) { showToast('审批拒绝', 'success'); showScreen(1); loadApprov
als(); }
            else { showToast('审批失败', 'error'); }

exec
/bin/bash -lc "rtk sed -n '1,180p' backend/apps/approvals/serializers.py" in /ho
me/caohui/projects/graduation-leave-system
 succeeded in 0ms:
        </div>
      </div>

      <!-- 审批操作 -->
      <div id="approval-section" style="padding: 10px;">
        <div class="card" style="margin-bottom: 10px;">
          <label style="display: block; font-size: 14px; color: #333; margin-bot
tom: 6px; font-weight: 500;">审批意见（可选）</label>
          <textarea id="approvalComment" style="width: 100%; min-height: 60px; p
adding: 8px; border: 1px solid #e8e8e8; border-radius: 4px; font-size: 14px;" pl
aceholder="请输入审批意见"></textarea>
          <span style="display: block; text-align: right; font-size: 12px; color
: #999; margin-top: 4px;">0/200</span>
        </div>
        <div style="display: flex; gap: 10px;" id="approval-actions">
          <button class="btn-primary" style="flex: 1;" onclick="doApprove()">通
过</button>
          <button class="btn-outline" style="flex: 1;" onclick="doReject()">拒绝
</button>
        </div>
      </div>
    </div>
  </div>

  <script>
    // Status mapping
    const statusMap = {
      'pending_dorm_manager': { text: '待宿管审批', class: 'tag-pending' },
      'pending_counselor': { text: '待辅导员审批', class: 'tag-pending' },
      'pending_dean': { text: '待学工部审批', class: 'tag-pending' },
      'approved': { text: '已通过', class: 'tag-approved' },
      'rejected': { text: '已拒绝', class: 'tag-rejected' }
    };

    function getStatusDisplay(status) {
      return statusMap[status] || { text: status, class: 'tag' };
    }

    function showScreen(index) {
      document.querySelectorAll('.screen').forEach((s, i) => {
        s.classList.toggle('active', i === index);
      });
      document.querySelectorAll('.nav-tabs .nav-tab').forEach((t, i) => {
        t.classList.toggle('active', i === index);
      });
    }

    async function doLogin() {
      const userId = document.getElementById('loginUserId').value.trim();
      const password = document.getElementById('loginPassword').value.trim();
      const errorEl = document.getElementById('loginError');
      const btn = event?.target || document.querySelector('#screen-login .btn-pr
imary');

      if (!userId || !password) {
        errorEl.textContent = '请输入用户ID和密码';
        errorEl.style.display = 'block';
        return;
      }

      // Loading state
      const originalText = btn.textContent;
      btn.disabled = true;
      btn.textContent = '登录中...';

      try {
        const result = await apiLogin(userId, password);

        if (result.success) {
          errorEl.style.display = 'none';
          document.getElementById('loginUserId').value = '';
          document.getElementById('loginPassword').value = '';

          // Show nav tabs and user bar
          document.getElementById('navTabs').style.display = 'flex';
          document.getElementById('userBar').style.display = 'flex';
          document.getElementById('currentUserName').textContent = result.user.n
ame;
          const roleMap = {
            'student': '学生',
            'dorm_manager': '宿管员',
            'counselor': '辅导员',
            'dean': '学工部'
          };
          document.getElementById('currentUserRole').textContent = '(' + (roleMa
p[result.user.role] || result.user.role) + ')';

          // Update UI based on role
          updateUIForRole(result.user.role);

          // Hide login screen
          document.getElementById('screen-login').classList.remove('active');

          // Route based on role and application status
          if (result.user.role === 'student') {
            document.getElementById('studentName').textContent = result.user.nam
e;
            document.getElementById('studentId').textContent = result.user.user_
id;

            // Pre-fill phone if available
            if (result.user.phone) {
              document.getElementById('contactPhone').value = result.user.phone;
            }

            // Check if student has applications
            const applications = await apiGetApplications();
            if (applications.results && applications.results.length > 0) {
              showScreen(1); // Show application progress
              loadMyApplications();
            } else {
              showScreen(0); // Show application form
            }
          } else {
            showScreen(1); // Approval list screen
            loadApprovals();
          }
        } else {
          errorEl.textContent = result.error.error || '登录失败，请检查用户ID和
密码';
          errorEl.style.display = 'block';
        }
      } finally {
        btn.disabled = false;
        btn.textContent = originalText;
      }
    }

    function updateUIForRole(role) {
      const isStudent = role === 'student';
      const isDean = role === 'dean';

      // Hide "学生申请" tab for non-students
      const navTabs = document.querySelectorAll('#navTabs .nav-tab');
      if (navTabs[0]) {
        navTabs[0].style.display = isStudent ? 'block' : 'none';
      }

      // Update nav tab text
      document.getElementById('nav-approval-text').textContent = isStudent ? '我
的申请' : (isDean ? '审批查询' : '审批列表');

      // Update list page title and role display
      document.getElementById('list-title').textContent = isStudent ? '我的申请'
 : (isDean ? '审批查询' : '审批列表');
      document.getElementById('role-display').textContent = (isStudent ? '学生'
: isDean ? '学工部' : role === 'counselor' ? '辅导员' : '宿管员');

      // Show/hide approval section for student/dean
      const approvalSection = document.getElementById('approval-section');
      if (approvalSection) {
        approvalSection.style.display = (isStudent || isDean) ? 'none' : 'block'
;
      }
    }

    function logout() {
      currentToken = null;
      currentUser = null;
      document.getElementById('navTabs').style.display = 'none';
      document.getElementById('userBar').style.display = 'none';
      document.querySelectorAll('.screen').forEach(s => s.classList.remove('acti
ve'));
      document.getElementById('screen-login').classList.add('active');
    }

    // File upload management
    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
    const ALLOWED_TYPES = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx'];
    let uploadedFiles = [];

    const fileInput = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');
    const uploadArea = document.querySelector('.upload-area');

    // File selection handler
    fileInput.addEventListener('change', (e) => {
      handleFiles(e.target.files);
    });

    // Drag and drop handlers
    uploadArea.addEventListener('dragover', (e) => {
      e.preventDefault();
      uploadArea.style.borderColor = 'var(--primary-color)';
      uploadArea.style.background = '#fafafa';
    });

    uploadArea.addEventListener('dragleave', () => {
      uploadArea.style.borderColor = '#d9d9d9';
      uploadArea.style.background = 'white';
    });

    uploadArea.addEventListener('drop', (e) => {
      e.preventDefault();
      uploadArea.style.borderColor = '#d9d9d9';
      uploadArea.style.background = 'white';
      handleFiles(e.dataTransfer.files);
    });

    function handleFiles(files) {
      const validFiles = [];
      const errors = [];

      Array.from(files).forEach(file => {
        const ext = '.' + file.name.split('.').pop().toLowerCase();

        if (!ALLOWED_TYPES.includes(ext)) {
          errors.push(`${file.name}: 不支持的文件格式`);
          return;
        }

        if (file.size > MAX_FILE_SIZE) {
          errors.push(`${file.name}: 文件大小超过10MB`);
          return;
        }

        validFiles.push(file);
      });

      if (errors.length > 0) {
        errors.forEach(err => showToast(err, 'error'));
      }

      uploadedFiles = uploadedFiles.concat(validFiles);
      renderFileList();
      fileInput.value = ''; // Reset input
    }

    function renderFileList() {
      fileList.innerHTML = uploadedFiles.map((file, index) => `
        <div class="file-item">
          <span style="font-size: 20px;">📄</span>
          <div class="file-info">
            <div class="file-name">${file.name}</div>
            <div class="file-size">${formatFileSize(file.size)}</div>
          </div>
          <button class="btn-delete" onclick="removeFile(${index})" type="button
">×</button>
        </div>
      `).join('');
    }

    function removeFile(index) {
      uploadedFiles.splice(index, 1);
      renderFileList();
    }

    function formatFileSize(bytes) {
      if (bytes < 1024) return bytes + ' B';
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
      return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }
  </script>

<!-- Toast容器 -->
<div class="toast-container" id="toastContainer"></div>

<script>
// Toast通知函数
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = 'toast' + (type !== 'info' ? ' ' + type : '');
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'slideIn 0.3s ease-out reverse';
    setTimeout(() => container.removeChild(toast), 300);
  }, 3000);
}
</script>
</body>
</html>

 succeeded in 0ms:
from rest_framework import serializers
from .models import Approval


class ApplicationBriefSerializer(serializers.Serializer):
    """Brief application info for approval list"""
    id = serializers.CharField(source='application_id')
    status = serializers.CharField()
    student_name = serializers.CharField(source='student.name')
    student_id = serializers.CharField(source='student.user_id')


class ApprovalListSerializer(serializers.ModelSerializer):
    """Lean serializer for approval lists - nested application structure"""
    id = serializers.CharField(source='approval_id', read_only=True)
    application = ApplicationBriefSerializer(read_only=True)
    approver_id = serializers.CharField(source='approver.user_id', read_only=Tru
e)

    class Meta:
        model = Approval
        fields = ['id', 'application', 'step', 'approver_id',
                  'approver_name', 'decision', 'comment', 'created_at']
        read_only_fields = ['id', 'step', 'approver_id',
                            'approver_name', 'decision', 'comment', 'created_at'
]


class ApprovalSerializer(serializers.ModelSerializer):
    """Full approval detail with nested application info"""
    application_id = serializers.CharField(source='application.application_id',
read_only=True)
    student_name = serializers.CharField(source='application.student.name', read
_only=True)
    student_id = serializers.CharField(source='application.student.user_id', rea
d_only=True)
    contact_phone = serializers.CharField(source='application.contact_phone', re
ad_only=True)
    reason = serializers.CharField(source='application.reason', read_only=True)
    approver_id = serializers.CharField(source='approver.user_id', read_only=Tru
e)

    class Meta:
        model = Approval
        fields = ['approval_id', 'application_id', 'student_name', 'student_id',
                  'contact_phone', 'reason', 'step', 'approver_id',
                  'approver_name', 'decision', 'comment', 'decided_at']
        read_only_fields = ['approval_id', 'application_id', 'student_name', 'st
udent_id',
                            'contact_phone', 'reason', 'step',
                            'approver_id', 'approver_name', 'decision', 'decided
_at']


class ApprovalActionSerializer(serializers.Serializer):
    comment = serializers.CharField(required=False, allow_blank=True)


class ApprovalListResponseSerializer(serializers.Serializer):
    """Schema-only: approval list response with pagination"""
    count = serializers.IntegerField()
    results = ApprovalListSerializer(many=True)

exec
/bin/bash -lc 'rtk git log --oneline --decorate --max-count=10 -- demo-web/index
.html backend/apps/approvals/serializers.py' in /home/caohui/projects/graduation
-leave-system
 succeeded in 0ms:
a153eb2 fix(demo-web): dean cross-page deduplication for approvals
08fbb2a fix(demo-web): use approval decision for status tag in list
f094a84 fix: extract real approver name from auto-completed approvals
e1dabf0 fix(demo-web): counselor timeline shows dorm manager approval
ef69064 feat(demo-web): add back button to approval detail page
19dece4 fix(demo-web): hide 申请详情 tab from navigation
b66c859 fix(demo-web): remove duplicate approvalOffset/approvalHasMore declarati
ons
658a8c1 fix(demo-web): remove duplicate let currentFilter declarations
d2e7c75 debug: 添加loadApprovals调试日志
92b78ce revert: 移除学生申请列表分页

exec
/bin/bash -lc "rtk sed -n '430,790p' demo-web/index.html" in /home/caohui/projec
ts/graduation-leave-system
 succeeded in 0ms:
            else { showToast('审批失败', 'error'); }
        } finally {
            btn.disabled = false;
            btn.textContent = originalText;
        }
    }

    async function doSubmitApplication() {
        const phone = document.getElementById('contactPhone').value;
        const reason = document.getElementById('applicationReason').value;
        const leaveDate = document.getElementById('leaveDate').value;

        // 验证必填字段
        if (!phone || !leaveDate) {
             showToast('请输入联系电话和离校日期', 'error');
             return;
        }

        // 验证附件（必需）
        if (!uploadedFiles || uploadedFiles.length === 0) {
             showToast('请上传附件材料', 'error');
             return;
        }

        // 验证手机号格式（11位，1开头）
        if (!/^1\d{10}$/.test(phone)) {
             showToast('请输入有效的11位手机号码', 'error');
             return;
        }

        // 验证原因长度（最多500字符）
        if (reason && reason.length > 500) {
             showToast('离校原因不能超过500字', 'error');
             return;
        }

        // 验证离校日期（不能早于今天）
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const selectedDate = new Date(leaveDate);
        if (selectedDate < today) {
             showToast('离校日期不能早于今天', 'error');
             return;
        }

        const btn = event?.target || document.querySelector('#screen-0 .btn-prim
ary');
        const originalText = btn.textContent;
        btn.disabled = true;
        btn.textContent = '提交中...';

        try {
            const result = await apiSubmitApplication(phone, reason, leaveDate,
uploadedFiles);
            if (result.success) {
                showToast('申请提交成功', 'success');
                document.getElementById('contactPhone').value = '';
                document.getElementById('applicationReason').value = '';
                document.getElementById('leaveDate').value = '';
                uploadedFiles = [];
                renderFileList();

                // Switch to progress view
                showScreen(1);
                loadMyApplications();
            } else {
                showToast(result.error.message || '申请提交失败', 'error');
            }
        } finally {
            btn.disabled = false;
            btn.textContent = originalText;
        }
    }
</script>
  <style>
    /* 导航标签 */
    .nav-tabs {
      background: white;
      display: flex;
      border-bottom: 1px solid #f0f0f0;
      position: sticky;
      top: 0;
      z-index: 10;
    }
    .nav-tab {
      flex: 1;
      text-align: center;
      padding: 12px 0;
      font-size: 14px;
      color: #666;
      cursor: pointer;
      position: relative;
      border: none;
      background: none;
    }
    .nav-tab.active {
      color: var(--primary-color);
      font-weight: 600;
    }
    .nav-tab.active::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 30px;
      height: 2px;
      background: var(--primary-color);
      border-radius: 1px;
    }

    /* 响应式：桌面端Tab导航优化 */
    @media (min-width: 1024px) {
      .nav-tabs {
        padding: 0 40px;
      }
      .nav-tab {
        padding: 16px 24px;
        font-size: 16px;
      }
      .nav-tab.active::after {
        width: 50px;
        height: 3px;
      }
    }

    /* 附件上传区域样式 */
    .upload-area {
      border: 2px dashed #d9d9d9;
      border-radius: 8px;
      padding: 30px;
      text-align: center;
      cursor: pointer;
      transition: all 0.3s;
    }
    .upload-area:hover {
      border-color: var(--primary-color);
      background: #fafafa;
    }
    .file-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px;
      background: #fafafa;
      border-radius: 4px;
      margin-bottom: 8px;
    }
    .file-info {
      flex: 1;
      margin-left: 8px;
    }
    .file-name {
      font-size: 14px;
      color: #333;
    }
    .file-size {
      font-size: 12px;
      color: #999;
    }
    .btn-delete {
      background: none;
      border: none;
      color: var(--status-error);
      font-size: 20px;
      cursor: pointer;
      padding: 0 8px;
    }

    .screen {
      display: none;
      min-height: calc(100vh - 45px);
    }
    .screen.active {
      display: block;
    }
    .login-screen {
      display: none;
      min-height: calc(100vh - 45px);
    }
    .login-screen.active {
      display: block;
    }
  </style>
</head>
<body>
  <!-- 顶部导航 -->
  <div class="nav-tabs" id="navTabs" style="display: none;">
    <button class="nav-tab active" onclick="showScreen(0)">学生申请</button>
    <button class="nav-tab" onclick="showScreen(1)"><span id="nav-approval-text"
>审批列表</span></button>
    <button class="nav-tab" onclick="showScreen(2)" style="display: none;">申请
详情</button>
  </div>

  <!-- 登录状态栏 -->
  <div id="userBar" style="background: white; padding: 8px 16px; border-bottom:
1px solid #f0f0f0; display: none; align-items: center; justify-content: space-be
tween;">
    <div>
      <span style="font-size: 14px; color: #666;">当前用户:</span>
      <span id="currentUserName" style="font-size: 14px; font-weight: 500; margi
n-left: 8px;"></span>
      <span id="currentUserRole" style="font-size: 12px; color: #999; margin-lef
t: 8px;"></span>
    </div>
    <button onclick="logout()" style="padding: 4px 12px; border: 1px solid #d9d9
d9; border-radius: 4px; background: white; cursor: pointer;">退出登录</button>
  </div>

  <!-- 登录屏幕 -->
  <div class="login-screen active" id="screen-login">
    <div style="padding: 40px 20px; max-width: 400px; margin: 0 auto;">
      <div class="card">
        <div style="text-align: center; margin-bottom: 30px;">
          <h2 style="color: var(--primary-color); margin-bottom: 8px;">毕业离校
申请系统</h2>
          <p style="color: #666; font-size: 14px;">请登录以继续</p>
        </div>
        <div style="margin-bottom: 20px;">
          <label style="display: block; font-size: 14px; margin-bottom: 8px; fon
t-weight: 500;">用户ID</label>
          <input id="loginUserId" type="text" style="width: 100%; padding: 12px;
 border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="
请输入用户ID（如 2020001）" required>
        </div>
        <div style="margin-bottom: 24px;">
          <label style="display: block; font-size: 14px; margin-bottom: 8px; fon
t-weight: 500;">密码</label>
          <input id="loginPassword" type="password" style="width: 100%; padding:
 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placehol
der="请输入密码" required>
        </div>
        <div id="loginError" style="display: none; padding: 10px; background: #f
ff2f0; border: 1px solid #ffccc7; border-radius: 4px; color: #cf1322; font-size:
 14px; margin-bottom: 16px;"></div>
        <button class="btn-primary" onclick="doLogin()">登录</button>
      </div>
    </div>
  </div>

  <div class="screen" id="screen-0">
    <div style="padding: 20px;">
      <!-- 用户信息卡片 -->
      <div class="card" style="margin-bottom: 20px;">
        <div style="font-size: 16px; font-weight: 600; color: var(--primary-colo
r); margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #f0f0f0;
">
          申请人信息
        </div>
        <div style="display: flex; align-items: center; padding: 10px 0;">
          <span style="font-size: 14px; color: #666; width: 80px;">姓名</span>
          <span id="studentName" style="font-size: 14px; color: #333;">-</span>
        </div>
        <div style="display: flex; align-items: center; padding: 10px 0;">
          <span style="font-size: 14px; color: #666; width: 80px;">学号</span>
          <span id="studentId" style="font-size: 14px; color: #333;">-</span>
        </div>
      </div>

      <!-- 表单卡片 -->
      <div class="card">
        <div style="margin-bottom: 20px;">
          <label style="display: block; font-size: 14px; margin-bottom: 8px; fon
t-weight: 500;">联系电话</label>
          <input id="contactPhone" type="tel" name="contact_phone" maxlength="20
" inputmode="numeric" style="width: 100%; padding: 12px; border: 1px solid #d9d9
d9; border-radius: 4px; font-size: 14px;" placeholder="请输入联系电话" required>
        </div>
        <div style="margin-bottom: 20px;">
          <label style="display: block; font-size: 14px; margin-bottom: 8px; fon
t-weight: 500;">离校原因</label>
          <textarea id="applicationReason" style="width: 100%; min-height: 120px
; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;
" placeholder="请输入离校原因"></textarea>
          <span style="display: block; text-align: right; font-size: 12px; color
: #999; margin-top: 4px;">0/500</span>
        </div>
        <div style="margin-bottom: 20px;">
          <label style="display: block; font-size: 14px; margin-bottom: 8px; fon
t-weight: 500;">离校日期</label>
          <input id="leaveDate" type="date" name="leave_date" style="width: 100%
; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;
" required>
        </div>

        <!-- 附件上传区域 -->
        <div style="margin-bottom: 20px;">
          <label style="display: block; font-size: 14px; margin-bottom: 8px; fon
t-weight: 500;">附件材料（必需）</label>
          <div class="upload-zone">
            <input type="file" id="fileInput" multiple accept=".jpg,.jpeg,.png,.
pdf,.doc,.docx" style="display: none;">
            <div class="upload-area" onclick="document.getElementById('fileInput
').click()">
              <div style="font-size: 40px; color: #999; margin-bottom: 8px;">📎<
/div>
              <div style="font-size: 14px; color: #666;">点击或拖拽文件到此处上
传</div>
              <div style="font-size: 12px; color: #999; margin-top: 4px;">支持jp
g/png/pdf/doc/docx，单文件不超过10MB</div>
            </div>
          </div>
          <!-- 文件列表 -->
          <div id="fileList" style="margin-top: 12px;"></div>
        </div>

        <button class="btn-primary" onclick="doSubmitApplication()">提交申请</bu
tton>
      </div>
    </div>
  </div>

  <!-- 屏幕2: 审批列表页 -->
  <div class="screen" id="screen-1">
    <div style="background: white; padding: 16px; display: flex; justify-content
: space-between; align-items: center;">
      <div style="font-size: 18px; font-weight: bold;" id="list-title">审批列表<
/div>
      <div style="font-size: 12px; color: #999;" id="role-display">宿管员</div>
    </div>

    <!-- Tab切换 -->
    <div style="background: white; display: flex; border-bottom: 1px solid #f0f0
f0;" id="approval-tabs">
      <div class="nav-tab active" style="flex: 1;" onclick="filterApprovals('all
')">全部</div>
      <div class="nav-tab" style="flex: 1;" onclick="filterApprovals('pending')"
>待审批</div>
      <div class="nav-tab" style="flex: 1;" onclick="filterApprovals('decided')"
>已审批</div>
    </div>

    <div style="padding: 10px;" id="approval-list-container">
      <!-- 列表项 -->
      <div style="text-align:center; padding: 20px; color:#999;">加载中...</div>
    </div>
    <div style="padding: 10px; text-align: center;">
      <button id="load-more-approvals" onclick="loadApprovals(true)" style="disp
lay: none; padding: 10px 20px; border: 1px solid var(--primary-color); backgroun
d: white; color: var(--primary-color); border-radius: 4px; cursor: pointer;">加
载更多</button>
    </div>
  </div>

  <!-- 屏幕3: 申请详情页 -->
  <div class="screen" id="screen-2">
    <div style="background: white; padding: 16px; display: flex; align-items: ce
nter; gap: 12px;">
      <button onclick="showScreen(1)" style="border: none; background: none; fon
t-size: 20px; cursor: pointer; color: var(--primary-color); padding: 0;">←</butt
on>
      <div style="font-size: 18px; font-weight: bold;">申请详情</div>
    </div>

    <div style="padding: 10px;">
      <!-- 基本信息 -->
      <div class="card">
        <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">基
本信息</div>
        <div style="display: flex; margin-bottom: 8px;">
          <span style="font-size: 14px; color: #999; width: 80px;">申请ID:</span
>
          <span style="font-size: 14px; color: #333; flex: 1;">-</span>
        </div>
        <div style="display: flex; margin-bottom: 8px;">
          <span style="font-size: 14px; color: #999; width: 80px;">学生:</span>
          <span style="font-size: 14px; color: #333; flex: 1;">-</span>
        </div>
        <div style="display: flex; margin-bottom: 8px;">
          <span style="font-size: 14px; color: #999; width: 80px;">离校日期:</sp
an>
          <span style="font-size: 14px; color: #333; flex: 1;">-</span>
        </div>
        <div style="display: flex; margin-bottom: 8px;">
          <span style="font-size: 14px; color: #999; width: 80px;">申请原因:</sp
an>
          <span style="font-size: 14px; color: #333; flex: 1;">-</span>
        </div>
      </div>

      <!-- 审批记录时间轴 -->
      <div class="card">
        <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">审
批记录</div>

        <!-- 时间轴项 -->
        <div style="position: relative; padding-left: 30px; margin-bottom: 20px;
">
          <div style="position: absolute; left: 10px; top: 4px; width: 10px; hei
ght: 10px; border-radius: 50%; background: white; border: 2px solid var(--primar
y-color);"></div>
          <div style="position: absolute; left: 14px; top: 16px; bottom: -20px;
width: 1px; background: #e8e8e8;"></div>
          <div class="flex-row justify-between align-center" style="margin-botto
m: 6px;">
            <span style="font-size: 15px; font-weight: 600;">宿管员审批</span>
            <span class="tag tag-pending">待审批</span>
          </div>
          <div style="font-size: 13px; color: #666;">审批人: 李老师</div>
        </div>

        <div style="position: relative; padding-left: 30px; margin-bottom: 20px;
">
          <div style="position: absolute; left: 10px; top: 4px; width: 10px; hei
ght: 10px; border-radius: 50%; background: var(--status-success); border: 2px so
lid var(--status-success);"></div>
          <div class="flex-row justify-between align-center" style="margin-botto
m: 6px;">
            <span style="font-size: 15px; font-weight: 600;">提交申请</span>
            <span class="tag tag-approved">已完成</span>
          </div>
          <div style="font-size: 13px; color: #666;">提交时间: 2024-06-01 10:30<
/div>
        </div>
      </div>

      <!-- 审批操作 -->
      <div id="approval-section" style="padding: 10px;">
        <div class="card" style="margin-bottom: 10px;">
          <label style="display: block; font-size: 14px; color: #333; margin-bot
tom: 6px; font-weight: 500;">审批意见（可选）</label>
          <textarea id="approvalComment" style="width: 100%; min-height: 60px; p
adding: 8px; border: 1px solid #e8e8e8; border-radius: 4px; font-size: 14px;" pl
aceholder="请输入审批意见"></textarea>
          <span style="display: block; text-align: right; font-size: 12px; color
: #999; margin-top: 4px;">0/200</span>
        </div>
        <div style="display: flex; gap: 10px;" id="approval-actions">

exec
/bin/bash -lc "rtk sed -n '1,260p' demo-web/js/api.js" in /home/caohui/projects/
graduation-leave-system
 succeeded in 0ms:
// API Integration Layer
const API_BASE_URL = 'http://localhost:8001/api';

let currentToken = null;
let currentUser = null;

async function apiLogin(userId, password) {
    try {
        const response = await fetch(API_BASE_URL + '/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: userId,
                password: password
            })
        });

        if (response.ok) {
            const data = await response.json();
            currentToken = data.access_token;
            currentUser = data.user;
            return { success: true, user: data.user };
        } else {
            currentToken = null;
            currentUser = null;
            const error = await response.json().catch(() => ({ error: 'Login fai
led' }));
            return { success: false, error: error };
        }
    } catch (e) {
        console.error("Login failed:", e);
        currentToken = null;
        currentUser = null;
        return { success: false, error: 'Network error' };
    }
}

function getAuthHeaders() {
    return {
        'Authorization': 'Bearer ' + currentToken
    };
}

async function apiSubmitApplication(phone, reason, leaveDate, files) {
    const formData = new FormData();
    formData.append('contact_phone', phone);
    formData.append('reason', reason);
    formData.append('leave_date', leaveDate);
    files.forEach(f => formData.append('attachments', f));

    try {
        const response = await fetch(API_BASE_URL + '/applications/', {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + currentToken },
            body: formData
        });
        if (response.ok) {
            return { success: true, data: await response.json() };
        } else {
            const error = await response.json().catch(() => ({ error: { message:
 '提交失败' } }));
            return { success: false, error: error.error || { message: '提交失败'
 } };
        }
    } catch (e) {
        console.error("Submit application failed:", e);
        return { success: false, error: { message: '网络错误，请检查连接' } };
    }
}

async function apiGetApplications() {
    try {
        const response = await fetch(API_BASE_URL + '/applications/', {
            headers: getAuthHeaders()
        });
        if (response.ok) {
            return await response.json();
        }
    } catch (e) {
        console.error("Get applications failed:", e);
    }
    return { results: [] };
}

async function apiGetApprovals(decision = 'pending', limit = 20, offset = 0) {
    try {
        const url = API_BASE_URL + '/approvals/?decision=' + decision + '&limit=
' + limit + '&offset=' + offset;
        const response = await fetch(url, {
            headers: getAuthHeaders()
        });
        if (response.ok) {
            return await response.json();
        }
    } catch (e) {
        console.error("Get approvals failed:", e);
    }
    return { results: [], count: 0 };
}

async function apiApprove(approvalId, comment) {
    try {
        const response = await fetch(API_BASE_URL + '/approvals/' + approvalId +
 '/approve/', {
            method: 'POST',
            headers: Object.assign({}, getAuthHeaders(), { 'Content-Type': 'appl
ication/json' }),
            body: JSON.stringify({ comment: comment })
        });
        return response.ok;
    } catch (e) {
        console.error("Approve failed:", e);
        return false;
    }
}

async function apiReject(approvalId, comment) {
    try {
        const response = await fetch(API_BASE_URL + '/approvals/' + approvalId +
 '/reject/', {
            method: 'POST',
            headers: Object.assign({}, getAuthHeaders(), { 'Content-Type': 'appl
ication/json' }),
            body: JSON.stringify({ comment: comment })
        });
        return response.ok;
    } catch (e) {
        console.error("Reject failed:", e);
        return false;
    }
}

async function apiUploadAttachment(applicationId, file, attachmentType = 'other'
) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('attachment_type', attachmentType);

    try {
        const response = await fetch(API_BASE_URL + '/applications/' + applicati
onId + '/attachments/', {
            method: 'POST',
            headers: getAuthHeaders(),
            body: formData
        });
        if (response.ok) {
            return await response.json();
        }
    } catch (e) {
        console.error("Upload attachment failed:", e);
    }
    return null;
}

async function apiGetAttachments(applicationId) {
    try {
        const response = await fetch(API_BASE_URL + '/applications/' + applicati
onId + '/attachments/', {
            headers: getAuthHeaders()
        });
        if (response.ok) {
            return await response.json();
        }
    } catch (e) {
        console.error("Get attachments failed:", e);
    }
    return [];
}

async function apiDeleteAttachment(applicationId, attachmentId) {
    try {
        const response = await fetch(API_BASE_URL + '/applications/' + applicati
onId + '/attachments/' + attachmentId + '/', {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        return response.ok;
    } catch (e) {
        console.error("Delete attachment failed:", e);
        return false;
    }
}

exec
/bin/bash -lc 'rtk rg -n "decision|decided_at|ApprovalListSerializer|ApprovalSer
ializer|pending_dean|dean" backend/apps/approvals backend/apps/applications back
end/apps/users' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/approvals/admin.py:7:    list_display = ['approval_id', 'applicatio
n', 'step', 'approver', 'decision', 'decided_at']
backend/apps/approvals/admin.py:8:    list_filter = ['step', 'decision']
backend/apps/users/migrations/0001_initial.py:25:                ('role', models
.CharField(choices=[('student', '学生'), ('counselor', '辅导员'), ('dean', '学工
部')], max_length=20)),
backend/apps/approvals/migrations/0003_alter_approval_step.py:16:            fie
ld=models.CharField(choices=[('dorm_manager', '宿管员'), ('counselor', '辅导员')
, ('dean', '学工部')], max_length=20),
backend/apps/approvals/migrations/0001_initial.py:20:                ('step', mo
dels.CharField(choices=[('counselor', '辅导员'), ('dean', '学工部')], max_length
=20)),
backend/apps/approvals/migrations/0001_initial.py:22:                ('decision'
, models.CharField(choices=[('pending', '待审批'), ('approved', '已通过'), ('rej
ected', '已驳回')], default='pending', max_length=20)),
backend/apps/approvals/migrations/0001_initial.py:24:                ('decided_a
t', models.DateTimeField(blank=True, null=True)),
backend/apps/users/migrations/0006_add_admin_role.py:21:                    ('de
an', '学工部'),
backend/apps/approvals/tests/test_rejection_flow.py:104:        self.assertEqual
(response.data['decision'], ApprovalDecision.REJECTED)
backend/apps/approvals/tests/test_rejection_flow.py:130:        self.assertEqual
(response.data['decision'], ApprovalDecision.REJECTED)
backend/apps/approvals/tests/test_list_permissions.py:33:        self.dean1 = Us
er.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
backend/apps/approvals/tests/test_list_permissions.py:34:        self.dean1.set_
password('D001')
backend/apps/approvals/tests/test_list_permissions.py:35:        self.dean1.save
()
backend/apps/approvals/tests/test_list_permissions.py:37:        self.dean2 = Us
er.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
backend/apps/approvals/tests/test_list_permissions.py:38:        self.dean2.set_
password('D002')
backend/apps/approvals/tests/test_list_permissions.py:39:        self.dean2.save
()
backend/apps/approvals/tests/test_list_permissions.py:59:            decision=Ap
provalDecision.PENDING
backend/apps/approvals/tests/test_list_permissions.py:68:            decision=Ap
provalDecision.PENDING
backend/apps/approvals/tests/test_list_permissions.py:101:    def test_dean_sees
_all_approvals_for_archive(self):
backend/apps/approvals/tests/test_list_permissions.py:102:        self.client.fo
rce_authenticate(user=self.dean1)
backend/apps/approvals/tests/test_list_permissions.py:115:    def test_decision_
all_does_not_leak_cross_approver_data(self):
backend/apps/approvals/tests/test_list_permissions.py:132:            decision=A
pprovalDecision.APPROVED
backend/apps/approvals/tests/test_list_permissions.py:151:            decision=A
pprovalDecision.PENDING
backend/apps/approvals/tests/test_list_permissions.py:154:        # Counselor1 c
alls decision=all
backend/apps/approvals/tests/test_list_permissions.py:156:        response = sel
f.client.get('/api/approvals/?decision=all')
backend/apps/approvals/tests/test_permissions.py:61:        self.dean1 = User.ob
jects.create_user(
backend/apps/approvals/tests/test_permissions.py:67:        self.dean2 = User.ob
jects.create_user(
backend/apps/approvals/tests/test_permissions.py:110:            decision=Approv
alDecision.PENDING
backend/apps/approvals/tests/test_permissions.py:124:            decision=Approv
alDecision.PENDING
backend/apps/approvals/tests/test_permissions.py:145:    def test_dean_cannot_ac
t_on_counselor_step(self):
backend/apps/approvals/tests/test_permissions.py:147:        self.client.force_a
uthenticate(user=self.dean1)
backend/apps/approvals/tests/test_state_machine.py:41:        # Create dean
backend/apps/approvals/tests/test_state_machine.py:42:        self.dean = User.o
bjects.create_user(
backend/apps/approvals/tests/test_state_machine.py:77:            decision=Appro
valDecision.PENDING
backend/apps/approvals/tests/test_state_machine.py:150:            decision=Appr
ovalDecision.PENDING
backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:28:
        field=models.CharField(choices=[('student', '学生'), ('dorm_manager', '
宿管员'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20),
backend/apps/approvals/views.py:10:from .serializers import ApprovalSerializer,
ApprovalActionSerializer, ApprovalListSerializer, ApprovalListResponseSerializer
backend/apps/approvals/views.py:25:        OpenApiParameter('decision', str, des
cription='决策过滤：pending/approved/rejected/all（默认pending）'),
backend/apps/approvals/views.py:72:    decision_param = request.query_params.get
('decision', 'pending')
backend/apps/approvals/views.py:73:    if decision_param != 'all':
backend/apps/approvals/views.py:74:        queryset = queryset.filter(decision=d
ecision_param)
backend/apps/approvals/views.py:84:    serializer = ApprovalListSerializer(page,
 many=True)
backend/apps/approvals/views.py:94:        200: ApprovalSerializer,
backend/apps/approvals/views.py:111:    # Permission check: only the approver or
 dean can view this approval
backend/apps/approvals/views.py:113:        return Response(ApprovalSerializer(a
pproval).data)
backend/apps/approvals/views.py:125:        200: ApprovalSerializer,
backend/apps/approvals/views.py:158:    if approval.decision != ApprovalDecision
.PENDING:
backend/apps/approvals/views.py:171:    approval.decision = ApprovalDecision.APP
ROVED
backend/apps/approvals/views.py:173:    approval.decided_at = timezone.now()
backend/apps/approvals/views.py:185:            decision=ApprovalDecision.PENDIN
G
backend/apps/approvals/views.py:190:                decision=ApprovalDecision.AP
PROVED,
backend/apps/approvals/views.py:192:                decided_at=timezone.now()
backend/apps/approvals/views.py:242:            decision=ApprovalDecision.PENDIN
G
backend/apps/approvals/views.py:249:    return Response(ApprovalSerializer(appro
val).data)
backend/apps/approvals/views.py:258:        200: ApprovalSerializer,
backend/apps/approvals/views.py:291:    if approval.decision != ApprovalDecision
.PENDING:
backend/apps/approvals/views.py:304:    approval.decision = ApprovalDecision.REJ
ECTED
backend/apps/approvals/views.py:306:    approval.decided_at = timezone.now()
backend/apps/approvals/views.py:315:    return Response(ApprovalSerializer(appro
val).data)
backend/apps/approvals/serializers.py:13:class ApprovalListSerializer(serializer
s.ModelSerializer):
backend/apps/approvals/serializers.py:22:                  'approver_name', 'dec
ision', 'comment', 'created_at']
backend/apps/approvals/serializers.py:24:                            'approver_n
ame', 'decision', 'comment', 'created_at']
backend/apps/approvals/serializers.py:27:class ApprovalSerializer(serializers.Mo
delSerializer):
backend/apps/approvals/serializers.py:40:                  'approver_name', 'dec
ision', 'comment', 'decided_at']
backend/apps/approvals/serializers.py:43:                            'approver_i
d', 'approver_name', 'decision', 'decided_at']
backend/apps/approvals/serializers.py:53:    results = ApprovalListSerializer(ma
ny=True)
backend/apps/applications/views.py:75:            decision=ApprovalDecision.PEND
ING
backend/apps/applications/views.py:84:            decision=ApprovalDecision.PEND
ING
backend/apps/applications/views.py:211:                decision=ApprovalDecision
.PENDING
backend/apps/users/serializers.py:57:    role = serializers.ChoiceField(choices=
['student', 'dorm_manager', 'counselor', 'dean'])
backend/apps/users/serializers.py:64:        'dean': 'D001',
backend/apps/approvals/models.py:9:    DEAN = 'dean', '学工部'
backend/apps/approvals/models.py:24:    decision = models.CharField(max_length=2
0, choices=ApprovalDecision.choices, default=ApprovalDecision.PENDING)
backend/apps/approvals/models.py:26:    decided_at = models.DateTimeField(null=T
rue, blank=True)
backend/apps/applications/migrations/0001_initial.py:22:                ('status
', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员
审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '
已驳回')], default='draft', max_length=20)),
backend/apps/applications/migrations/0005_alter_application_status.py:16:
     field=models.CharField(choices=[('draft', '草稿'), ('pending_dorm_manager',
 '待宿管员审批'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学
工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', ma
x_length=20),
backend/apps/applications/tests/test_p0_fixes.py:136:            decision=Approv
alDecision.PENDING
backend/apps/applications/tests/test_p0_fixes.py:145:            decision=Approv
alDecision.APPROVED
backend/apps/applications/tests/test_p0_fixes.py:154:            decision=Approv
alDecision.REJECTED
backend/apps/applications/tests/test_p0_fixes.py:160:            decision=Approv
alDecision.PENDING
backend/apps/applications/tests/test_p0_fixes.py:168:            decision=Approv
alDecision.APPROVED
backend/apps/applications/tests/test_p0_fixes.py:176:            decision=Approv
alDecision.REJECTED
backend/apps/applications/tests/test_error_cases.py:67:        self.dean = User.
objects.create_user(
backend/apps/users/management/commands/seed_data.py:114:            self.stdout.
write(f'Created dean: {user.user_id}')
backend/apps/applications/tests/test_detail_permissions.py:41:        self.dean1
 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
backend/apps/applications/tests/test_detail_permissions.py:42:        self.dean1
.set_password('D001')
backend/apps/applications/tests/test_detail_permissions.py:43:        self.dean1
.save()
backend/apps/applications/tests/test_detail_permissions.py:45:        self.dean2
 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
backend/apps/applications/tests/test_detail_permissions.py:46:        self.dean2
.set_password('D002')
backend/apps/applications/tests/test_detail_permissions.py:47:        self.dean2
.save()
backend/apps/applications/tests/test_detail_permissions.py:87:    def test_dean_
cannot_access_in_progress_application(self):
backend/apps/applications/tests/test_detail_permissions.py:99:        self.clien
t.force_authenticate(user=self.dean2)
backend/apps/applications/tests/test_list_permissions.py:38:        self.dean =
User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
backend/apps/applications/tests/test_list_permissions.py:39:        self.dean.se
t_password('D001')
backend/apps/applications/tests/test_list_permissions.py:40:        self.dean.sa
ve()
backend/apps/applications/tests/test_list_permissions.py:74:            decision
=ApprovalDecision.PENDING
backend/apps/applications/tests/test_list_permissions.py:102:    def test_dean_s
ees_only_approved_applications_for_archive(self):
backend/apps/applications/tests/test_list_permissions.py:103:        self.client
.force_authenticate(user=self.dean)
backend/apps/applications/tests/test_application_flow.py:45:        self.dean =
User.objects.create_user(
backend/apps/applications/tests/test_application_flow.py:100:        self.assert
Equal(response.data['decision'], ApprovalDecision.APPROVED)
backend/apps/applications/tests/test_application_flow.py:120:        self.assert
Equal(response.data['decision'], ApprovalDecision.APPROVED)
backend/apps/applications/serializers.py:31:        from apps.approvals.serializ
ers import ApprovalSerializer
backend/apps/applications/serializers.py:32:        return ApprovalSerializer(ob
j.approvals.all(), many=True).data
backend/apps/users/models.py:9:    DEAN = 'dean', '学工部'

exec
/bin/bash -lc "rtk sed -n '1,220p' backend/apps/approvals/models.py" in /home/ca
ohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.db import models
from apps.users.models import User
from apps.applications.models import Application


class ApprovalStep(models.TextChoices):
    DORM_MANAGER = 'dorm_manager', '宿管员'
    COUNSELOR = 'counselor', '辅导员'
    DEAN = 'dean', '学工部'


class ApprovalDecision(models.TextChoices):
    PENDING = 'pending', '待审批'
    APPROVED = 'approved', '已通过'
    REJECTED = 'rejected', '已驳回'


class Approval(models.Model):
    approval_id = models.CharField(max_length=50, primary_key=True)
    application = models.ForeignKey(Application, on_delete=models.PROTECT, relat
ed_name='approvals')
    step = models.CharField(max_length=20, choices=ApprovalStep.choices)
    approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='a
pprovals')
    approver_name = models.CharField(max_length=100)
    decision = models.CharField(max_length=20, choices=ApprovalDecision.choices,
 default=ApprovalDecision.PENDING)
    comment = models.TextField(null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'approvals'

exec
/bin/bash -lc "rtk sed -n '1,280p' backend/apps/approvals/views.py" in /home/cao
hui/projects/graduation-leave-system
 succeeded in 0ms:
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
import logging
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Approval, ApprovalDecision, ApprovalStep
from .serializers import ApprovalSerializer, ApprovalActionSerializer, ApprovalL
istSerializer, ApprovalListResponseSerializer
from .pagination import ApprovalLimitOffsetPagination
from .validators import approval_step_matches_application_status
from apps.applications.models import Application, ApplicationStatus
from apps.users.models import User, UserRole
from apps.notifications.services import notify_approval_decided
from schema import ErrorResponseSerializer
import uuid


@extend_schema(
    operation_id='approvals_list',
    summary='获取审批列表',
    description='获取当前用户的待审批列表（辅导员或学工部）',
    parameters=[
        OpenApiParameter('decision', str, description='决策过滤：pending/approve
d/rejected/all（默认pending）'),
        OpenApiParameter('limit', int, description='每页数量（默认20）'),
        OpenApiParameter('offset', int, description='偏移量（默认0）'),
    ],
    responses={
        200: ApprovalListResponseSerializer,
        403: ErrorResponseSerializer,
    },
    tags=['审批']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_approvals(request):
    user = request.user

    # 学生禁止访问
    if user.role == UserRole.STUDENT:
        return Response(
            {'error': {'code': 'FORBIDDEN', 'message': '学生不能访问审批列表'}},
            status=status.HTTP_403_FORBIDDEN
        )

    # 宿管员: 只看自己的dorm_manager审批
    if user.role == UserRole.DORM_MANAGER:
        queryset = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.DORM_MANAGER
        ).select_related('application', 'application__student', 'approver')

    # 辅导员: 只看自己的counselor审批
    elif user.role == UserRole.COUNSELOR:
        queryset = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.COUNSELOR
        ).select_related('application', 'application__student', 'approver')

    # 学工部: 查看所有审批（存档用）
    elif user.role == UserRole.DEAN:
        queryset = Approval.objects.all().select_related('application', 'applica
tion__student', 'approver')

    else:
        return Response(
            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
            status=status.HTTP_403_FORBIDDEN
        )

    # Decision filtering (default: pending)
    decision_param = request.query_params.get('decision', 'pending')
    if decision_param != 'all':
        queryset = queryset.filter(decision=decision_param)

    # 排序
    queryset = queryset.order_by('-created_at', '-approval_id')

    # 分页
    paginator = ApprovalLimitOffsetPagination()
    page = paginator.paginate_queryset(queryset, request)

    # 序列化
    serializer = ApprovalListSerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)


@extend_schema(
    operation_id='approvals_get',
    summary='获取审批详情',
    description='获取指定审批的详细信息',
    responses={
        200: ApprovalSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
    tags=['审批']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_approval(request, approval_id):
    try:
        approval = Approval.objects.select_related('application', 'approver').ge
t(approval_id=approval_id)
    except Approval.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存
在'}},
                        status=status.HTTP_404_NOT_FOUND)

    user = request.user

    # Permission check: only the approver or dean can view this approval
    if user.role == UserRole.DEAN or approval.approver_id == user.user_id:
        return Response(ApprovalSerializer(approval).data)

    return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源
'}},
                    status=status.HTTP_403_FORBIDDEN)


@extend_schema(
    operation_id='approvals_approve',
    summary='通过审批',
    description='审批人通过指定的审批申请',
    request=ApprovalActionSerializer,
    responses={
        200: ApprovalSerializer,
        400: ErrorResponseSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
        409: ErrorResponseSerializer,
    },
    tags=['审批']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def approve_approval(request, approval_id):
    try:
        approval = Approval.objects.select_for_update().get(approval_id=approval
_id)
    except Approval.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存
在'}},
                        status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM
_MANAGER:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此
操作'}},
                        status=status.HTTP_403_FORBIDDEN)
    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSEL
OR:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此
操作'}},
                        status=status.HTTP_403_FORBIDDEN)
    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此
操作'}},
                        status=status.HTTP_403_FORBIDDEN)

    if approval.approver_id != user.user_id:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此
操作'}},
                        status=status.HTTP_403_FORBIDDEN)

    if approval.decision != ApprovalDecision.PENDING:
        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，
不能重复操作'}},
                        status=status.HTTP_409_CONFLICT)

    if not approval_step_matches_application_status(approval):
        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审
批步骤不匹配'}},
                        status=status.HTTP_409_CONFLICT)

    serializer = ApprovalActionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求
参数验证失败'}},
                        status=status.HTTP_400_BAD_REQUEST)

    approval.decision = ApprovalDecision.APPROVED
    approval.comment = serializer.validated_data.get('comment', '')
    approval.decided_at = timezone.now()
    approval.save()

    notify_approval_decided(approval)

    application = approval.application
    if approval.step == ApprovalStep.DORM_MANAGER:
        # Auto-complete other pending dorm manager approvals for the same buildi
ng
        # (New requirement: any dorm manager in the building can approve, others
 see "already approved")
        other_dorm_approvals = Approval.objects.filter(
            application=application,
            step=ApprovalStep.DORM_MANAGER,
            decision=ApprovalDecision.PENDING
        ).exclude(approval_id=approval.approval_id)

        if other_dorm_approvals.exists():
            other_dorm_approvals.update(
                decision=ApprovalDecision.APPROVED,
                comment=f'已由{approval.approver_name}完成审批，无需重复操作',
                decided_at=timezone.now()
            )
            logging.info(
                f"Auto-completed {other_dorm_approvals.count()} other dorm manag
er approvals "
                f"for application {application.application_id} after approval by
 {approval.approver.user_id}"
            )

        # Check for existing counselor approval to prevent duplicates
        existing_counselor_approval = Approval.objects.filter(
            application=application,
            step=ApprovalStep.COUNSELOR
        ).exists()

        if existing_counselor_approval:
            return Response({'error': {'code': 'CONFLICT', 'message': '辅导员审
批已存在，不能重复创建'}},
                            status=status.HTTP_409_CONFLICT)

        application.status = ApplicationStatus.PENDING_COUNSELOR
        application.save()

        # Get counselor by department (Phase 3 design: department-based routing)
        # Note: Original design used ClassMapping (class_id), but Phase 3 user r
equirements
        # changed to "按学院向辅导员审批" (approval by department/college).
        # Multiple counselors per department are allowed (different classes with
in department).
        # Selection: order_by('user_id') picks lowest ID for deterministic routi
ng.
        counselors = User.objects.filter(
            role=UserRole.COUNSELOR,
            department=application.student.department,
            active=True
        ).order_by('user_id')

        if counselors.count() > 1:
            logging.warning(
                f"Multiple counselors found for department {application.student.
department}: "
                f"{counselors.count()} matches. Selected {counselors.first().use
r_id} via order_by('user_id')"
            )

        counselor = counselors.first()

        if not counselor:
            return Response({'error': {'code': 'NOT_FOUND', 'message': '该学院辅
导员不存在',
                                        'details': {'department': application.st
udent.department}}},
                            status=status.HTTP_404_NOT_FOUND)

        Approval.objects.create(
            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=counselor,
            approver_name=counselor.name,
            decision=ApprovalDecision.PENDING
        )
    elif approval.step == ApprovalStep.COUNSELOR:
        # Counselor approval completes the process (2-level approval)
        application.status = ApplicationStatus.APPROVED
        application.save()

    return Response(ApprovalSerializer(approval).data)


@extend_schema(
    operation_id='approvals_reject',
    summary='驳回审批',
    description='审批人驳回指定的审批申请',
    request=ApprovalActionSerializer,
    responses={
        200: ApprovalSerializer,
        400: ErrorResponseSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
        409: ErrorResponseSerializer,
    },
    tags=['审批']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def reject_approval(request, approval_id):
    try:
        approval = Approval.objects.select_for_update().get(approval_id=approval
_id)
    except Approval.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存
在'}},
                        status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM
_MANAGER:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此
操作'}},
                        status=status.HTTP_403_FORBIDDEN)
    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSEL
OR:

codex
[RESPONSE_START]
{
  "consensus": false,
  "decision": "不同意直接判定7个UI问题修复已达到生产就绪；多数表层修复已落地，但
分页去重实现仍存在阻塞级缺陷，需要先修正并补充验证。",
  "blocking_issues": [
    "demo-web/index.html 的 loadApprovals() 用 filtered.length 推进 approvalOffs
et；在学工部去重或已审批前端过滤后，offset 不等于后端已读取的原始页大小，会导致
重复拉取、漏拉或加载更多卡住。",
    "ApprovalListSerializer 未返回 decided_at，但前端审批列表已尝试显示 approval
.decided_at；已审批列表无法展示审批时间，属于前后端契约不一致。"
  ],
  "reasoning": "我同意 DISCUSS-审核DEMO-WEB用户测试发现的7个UI问题修复-JS变量重
复声明-1780867787-r0-claude 中强调的兼容性和证据要求。当前代码已能看到重复 let
声明移除、详情 tab 隐藏、返回按钮、审批人从自动完成 comment 提取、状态标签改用 a
pproval.decision、学工部跨页去重 Set 等修改。但分页逻辑把渲染后的 filtered.lengt
h 当成 API offset 推进依据，这是错误的契约：offset 必须按后端返回的原始 page 数
量推进。尤其 currentFilter=decided 时 API 拉 decision=all 再前端过滤，若当前页没
有已审批记录，filtered.length 为 0 且 data.count > approvalOffset，加载更多会持
续请求同一页。学工部去重同样可能让 filtered.length 小于原始页大小，造成重叠请求
或卡住。因此不能达成生产就绪共识。",
  "previous_responses": [
    "DISCUSS-审核DEMO-WEB用户测试发现的7个UI问题修复-JS变量重复声明-1780867787-r
0-claude"
  ],
  "targeted_challenges": [
    {
      "target_agent": "claude",
      "target_response_id": "DISCUSS-审核DEMO-WEB用户测试发现的7个UI问题修复-JS
变量重复声明-1780867787-r0-claude",
      "question": "请确认分页验收标准是否应明确为：approvalOffset 按后端本页原始
 results.length 推进，而不是按前端过滤/去重后的显示数量推进。",
      "rationale": "这是分页 API 契约问题，不修正会在已审批过滤和学工部去重场景
中造成重复请求、漏数据或加载更多无法结束。"
    }
  ],
  "dissent": "表层UI问题中有多项已修复，但分页和列表字段契约问题使我不能认可生产
就绪结论。",
  "evidence": [
    "demo-web/index.html:10-13 仅保留 currentFilter、approvalOffset、approvalHas
More、deanDisplayedApps 的单处全局声明，JS重复声明问题表面已解决。",
    "demo-web/index.html:103-114 学工部使用 deanDisplayedApps 和 appMap 做 appli
cation.id 去重。",
    "demo-web/index.html:164-165 使用 approvalOffset += filtered.length 和 data.
count > approvalOffset 推进分页；filtered 已经过 decided 过滤和 dean 去重，不等
于后端原始页大小。",
    "demo-web/index.html:96-99 currentFilter=decided 时先请求 decision=all，再用
 approval.decision 做前端过滤，可能产生 filtered.length 为 0 但后端仍有更多原始
记录的情况。",
    "backend/apps/approvals/serializers.py:20-24 ApprovalListSerializer 字段包含
 created_at 但不包含 decided_at；demo-web/index.html:147-151 却尝试读取 approval
.decided_at。"
  ],
  "action_items": [
    {
      "owner": "claude",
      "task": "修正 loadApprovals 分页 offset：保存 rawResultsLength=data.result
s.length，offset 按 rawResultsLength 推进；空显示页但 rawResultsLength>0 时继续
允许下一页或给出稳定结束条件。",
      "due": "before consensus",
      "verification": "构造 decision=all 且第一页无 decided 记录、以及 dean 去重
后一页 filtered.length < data.results.length 的场景，验证加载更多不会重复同一 of
fset。"
    },
    {
      "owner": "claude",
      "task": "决定并统一审批列表是否需要 decided_at；若前端要显示审批时间，则将
 decided_at 加入 ApprovalListSerializer fields/read_only_fields。",
      "due": "before consensus",
      "verification": "已审批列表接口返回 decided_at，前端能显示审批时间；或移除
前端对应显示逻辑并更新验收说明。"
    },
    {
      "owner": "codex",
      "task": "分页和字段契约修复后进行复审。",
      "due": "after fix",
      "verification": "复查 demo-web/index.html 与 backend/apps/approvals/serial
izers.py，并给出是否可达成生产就绪共识。"
    }
  ]
}
[RESPONSE_END]
tokens used
67,094

