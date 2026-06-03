# XG外部数据源API全面采集测试指南

**测试目的：** 验证XG API数据范围、内容完整性、数据量统计

**测试脚本：** `backend/scripts/xg_api_collection_test.py`

---

## 前置条件

### 1. 获取XG生产凭证

需要从XG学工系统管理员获取：
- `XG_TENANT_CODE`: 租户代码（如 C10026）
- `XG_APP_KEY`: 应用密钥
- `XG_APP_SECRET`: 签名密钥
- `XG_API_BASE_URL`: API基础URL（测试/生产环境）

### 2. 配置环境变量

**方法A：临时设置（推荐用于测试）**
```bash
export XG_RUN_LIVE_API_TEST=1
export XG_TENANT_CODE="C10026"
export XG_APP_KEY="your_app_key"
export XG_APP_SECRET="your_secret"
export XG_API_BASE_URL="https://saas.api.goliveplus.cn"
```

**方法B：配置文件（生产环境）**
编辑 `backend/.env`：
```
XG_RUN_LIVE_API_TEST=1
XG_TENANT_CODE=C10026
XG_APP_KEY=your_app_key
XG_APP_SECRET=your_secret
XG_API_BASE_URL=https://saas.api.goliveplus.cn
```

---

## 测试执行

### 基础测试（3页，20条样本）
```bash
cd backend
python scripts/xg_api_collection_test.py --output reports/
```

### 完整测试（指定页数和样本数）
```bash
python scripts/xg_api_collection_test.py \
  --output reports/ \
  --max-pages 10 \
  --sample-size 50
```

---

## 测试内容

### 测试1：分页数据采集
- **范围：** 前N页数据
- **验证点：**
  - current_page 与请求一致
  - per_page 与请求一致
  - total 总记录数
  - next_page_url 分页链接
  - 数据记录数与per_page匹配

### 测试2：过滤条件测试
- **姓名过滤：** `name='张'`
- **学号过滤：** `number='2020'`
- **验证点：** 过滤结果数量，数据匹配度

### 测试3：字段完整性检查
- **必填字段：** number, name, phone, status
- **关联对象：** user_identity, department, parent_dep, user
- **统计指标：**
  - present（有效值数量）
  - null（空值数量）
  - empty（空字符串数量）
  - 完整性百分比

### 测试4：数据量统计
- **总记录数：** total
- **总页数：** last_page
- **每页记录数：** per_page
- **预估全量采集时间**

---

## 输出文件

### 1. 测试报告（JSON格式）
**路径：** `reports/xg_collection_test_YYYYMMDD_HHMMSS.json`

**结构：**
```json
{
  "test_time": "2026-06-03T...",
  "scope_tests": {
    "pagination": {
      "status": "completed",
      "pages_tested": 3,
      "results": [...]
    },
    "filters": {
      "status": "completed",
      "tests": [...]
    }
  },
  "content_tests": {
    "field_completeness": {
      "sample_size": 20,
      "required_fields": {...},
      "related_objects": {...}
    }
  },
  "volume_tests": {
    "statistics": {
      "total_records": 4311,
      "total_pages": 432,
      "per_page": 10,
      "estimated_fetch_time_minutes": 3.6
    }
  }
}
```

### 2. 数据示例表文档
**路径：** `docs/XG-API-ACTUAL-DATA-SAMPLES.md`

**内容：** 基于实际API响应的完整数据示例

---

## 验证清单

采集测试完成后验证：
- [ ] 测试报告JSON文件已生成
- [ ] 分页测试覆盖至少3页
- [ ] 过滤条件测试通过
- [ ] 必填字段完整性 ≥ 95%
- [ ] 关联对象完整性 ≥ 80%
- [ ] 数据量统计准确
- [ ] 数据示例表文档已创建

---

## 常见问题

### Q1: 签名认证失败
**错误：** `{"code": 401, "msg": "签名验证失败"}`

**排查：**
1. 检查 `XG_APP_KEY` 和 `XG_APP_SECRET` 是否正确
2. 检查时间戳是否同步（系统时间与服务器时间差 < 5分钟）
3. 确认 `encryptionType` 设置正确（sha1/md5）

### Q2: 租户代码错误
**错误：** `{"code": 404, "msg": "租户不存在"}`

**排查：**
检查 `XG_TENANT_CODE` 是否与实际租户代码一致

### Q3: API速率限制
**错误：** `{"code": 429, "msg": "请求过于频繁"}`

**解决：**
- 减少 `--max-pages` 参数
- 增加脚本中的 `time.sleep(0.5)` 延迟

---

**相关文档：**
- API文档原文：`docs/api说明.txt`
- 字段映射规则：`docs/XG-API-DATA-EXAMPLES.md`
- 映射器代码：`backend/apps/users/integrations/xg_user_mapper.py`
- 客户端代码：`backend/apps/users/integrations/xg_user_client.py`
