# XG外部API数据采集样表

**数据来源：** XG学工系统API示例响应  
**采集日期：** 2026-06-03  
**数据状态：** 基于文档示例（生产API需要实际凭证）

---

## 用户数据样例

### 样例1：学生用户（张颖）

```json
{
  "id": 40934,
  "tenant_id": 46,
  "tenant_code": "C10026",
  "type": 2,
  "user_id": 1401,
  "identity_id": 183,
  "name": "张颖",
  "sex": 2,
  "number": "17",
  "phone": "18626409896",
  "id_card": null,
  "activation_time": "2021-06-23 16:57:09",
  "status": 1,
  "updated_at": "2021-11-03 13:50:03"
}
```

**数据表格：**

| 字段 | 值 | 说明 |
|---|---|---|
| number | 17 | 学号/工号（映射为user_id） |
| name | 张颖 | 姓名 |
| phone | 18626409896 | 手机号 |
| sex | 2 | 性别（2=女） |
| status | 1 | 状态（1=正常→active=True） |
| identity_id | 183 | 身份ID |
| activation_time | 2021-06-23 16:57:09 | 激活时间 |
| updated_at | 2021-11-03 13:50:03 | 更新时间 |

---

### 关联数据：身份信息

```json
{
  "id": 183,
  "name": "来宾",
  "type": 1,
  "validity_type": 1,
  "duration": 0
}
```

| 字段 | 值 | 说明 |
|---|---|---|
| id | 183 | 身份ID |
| name | 来宾 | 身份名称 |
| type | 1 | 身份类型（1=信息库内） |
| validity_type | 1 | 有效期类型（1=永久有效） |

---

### 关联数据：部门层级

#### 一级部门（parent_dep[0]）

```json
{
  "id": 35,
  "name": "杭州青橄榄网络技术有限公司",
  "department_code": "C100260159402712838523",
  "level": 1,
  "parent_id": 0
}
```

#### 二级部门（parent_dep[1] / department[0]）

```json
{
  "id": 47,
  "name": "产品测试",
  "department_code": "C100261159409057535680",
  "level": 2,
  "parent_id": 35,
  "key": "35-"
}
```

**部门层级表格：**

| 层级 | ID | 名称 | 部门Code | 父级ID |
|---|---|---|---|---|
| 1 | 35 | 杭州青橄榄网络技术有限公司 | C100260159402712838523 | 0 |
| 2 | 47 | 产品测试 | C100261159409057535680 | 35 |

**映射规则：** 取 `department[0].name` → `User.department = "产品测试"`

---

### 关联数据：用户账号

```json
{
  "id": 1401,
  "phone": "18626409896",
  "number": "",
  "status": 3,
  "one_card_status": 0
}
```

| 字段 | 值 | 说明 |
|---|---|---|
| status | 3 | 账号状态（3=审核通过） |
| one_card_status | 0 | 一卡通状态（0=未绑定） |

---

### 关联数据：扩展字段

```json
{
  "id": 448,
  "user_auth_id": 41388,
  "key": "h8WxQd_sLeYqz",
  "name": "身高",
  "value": "XX"
}
```

| 字段名 | 字段值 |
|---|---|
| 身高 | XX |

---

### 关联数据：微信信息

```json
{
  "id": 523,
  "user_id": 327,
  "user_code": "o2dY06ayLwoWmAFtcyZW3yGAXa4Y",
  "nickname": "YANG",
  "headimgurl": "https://thirdwx.qlogo.cn/mmopen/..."
}
```

| 字段 | 值 | 说明 |
|---|---|---|
| user_code | o2dY06ayLwoWmAFtcyZW3yGAXa4Y | 微信openId |
| nickname | YANG | 微信昵称 |

---

## 字段映射验证表

### XG → 内部系统映射实例

| XG来源字段 | XG示例值 | 内部目标字段 | 映射后值 | 映射规则 |
|---|---|---|---|---|
| number | "17" | User.user_id | "17" | 直接映射 |
| name | "张颖" | User.name | "张颖" | 直接映射 |
| phone | "18626409896" | User.phone | "18626409896" | 优先主记录phone |
| department[0].name | "产品测试" | User.department | "产品测试" | 取第一个部门 |
| status | 1 | User.active | True | 1→True, 其他→False |
| user_identity.name | "来宾" | User.role | - | 需要身份映射规则 |

---

## 数据完整性检查清单

### 必填字段验证

| 字段 | 要求 | 示例验证 | 结果 |
|---|---|---|---|
| number | 不为空 | "17" | ✓ |
| name | 不为空 | "张颖" | ✓ |
| phone | 11位数字 | "18626409896" | ✓ |
| status | 整数 | 1 | ✓ |

### 关联数据验证

| 关联对象 | 要求 | 示例验证 | 结果 |
|---|---|---|---|
| user_identity | 存在 | {"id": 183, ...} | ✓ |
| department | 至少1个 | [{"id": 47, ...}] | ✓ |
| parent_dep | 存在 | [2个层级] | ✓ |

---

## 特殊情况处理示例

### 情况1：phone字段为null

**XG响应：**
```json
{
  "phone": null,
  "user": {
    "phone": "18626409896"
  }
}
```

**处理：** 从 `user.phone` 提取 → `User.phone = "18626409896"`

### 情况2：department数组为空

**XG响应：**
```json
{
  "department": []
}
```

**处理：** `User.department = None`

### 情况3：status != 1（注销用户）

**XG响应：**
```json
{
  "status": 2
}
```

**处理：** `User.active = False`

---

## 分页响应结构示例

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "current_page": 1,
    "per_page": "10",
    "total": 4311,
    "last_page": 4311,
    "data": [
      { "id": 40934, "name": "张颖", ... }
    ]
  }
}
```

**分页参数表格：**

| 参数 | 示例值 | 说明 |
|---|---|---|
| current_page | 1 | 当前页码 |
| per_page | "10" | 每页记录数 |
| total | 4311 | 总记录数 |
| last_page | 4311 | 总页数 |

---

## 数据采集说明

**当前状态：** 基于文档示例  
**实际采集要求：** 需要XG生产凭证（appKey + 签名）  
**验证方式：** 运行 `backend/scripts/diagnose_xg_api.py`

**实际采集命令（需要凭证）：**
```bash
# 设置环境变量
export XG_RUN_LIVE_API_TEST=1

# 运行诊断脚本
cd backend
python scripts/diagnose_xg_api.py --live
```

---

**数据来源：** `docs/api说明.txt`  
**映射器：** `backend/apps/users/integrations/xg_user_mapper.py`  
**客户端：** `backend/apps/users/integrations/xg_user_client.py`
