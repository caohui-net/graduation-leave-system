# XG外部数据源API数据示例表

**API名称：** 获取租户下人员信息（信息中心数据）  
**数据来源：** XG学工系统  
**文档日期：** 2026-06-03

---

## API端点信息

**测试环境：** `https://dev-saas-api.goliveplus.cn/api/open-api/user-center/tenant/auth-user-info`  
**生产环境：** `https://saas.api.goliveplus.cn/api/open-api/user-center/tenant/auth-user-info`  
**请求方式：** POST

---

## 请求参数

### Header参数

| 参数名 | 必选 | 类型 | 说明 |
|---|---|---|---|
| appKey | 是 | string | 第三方系统应用ID |
| timestamp | 是 | string | Unix时间戳 |
| randStr | 是 | string | 随机字符串 |
| sign | 是 | string | 认证签名 |
| encryptionType | 否 | string | 加密类型（sha1/md5） |

### Form-Data参数

| 参数名 | 必选 | 类型 | 说明 | 示例值 |
|---|---|---|---|---|
| tenantCode | 是 | string | 租户Code | C10026 |
| page | 是 | int | 当前页 | 1 |
| pageNum | 是 | int | 每页显示条数 | 10 |
| name | 否 | string | 姓名 | 张颖 |
| number | 否 | string | 学工号 | 17 |
| phone | 否 | string | 手机号 | 18626409896 |
| isDelete | 否 | int | 查询被删数据（传1） | 0 |
| identityId | 否 | string | 身份ID（逗号分隔） | 203,204 |
| departmentId | 否 | string | 部门ID（逗号分隔） | 203,204 |
| departmentCode | 否 | string | 部门code（逗号分隔） | - |
| updatedTime | 否 | array | 更新时间段 | ["2021-02-01 00:00:00", "2021-04-06 00:00:00"] |

---

## 响应数据结构

### 分页信息

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "current_page": 1,
    "first_page_url": "http://...?page=1",
    "from": 1,
    "last_page": 4311,
    "last_page_url": "http://...?page=4311",
    "next_page_url": "http://...?page=2",
    "path": "http://...",
    "per_page": "10",
    "prev_page_url": null,
    "to": 10,
    "total": 4311,
    "data": [...]
  }
}
```

### 用户数据记录（data数组元素）

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
  "invitation_code": null,
  "reason": null,
  "refuse": null,
  "activation_time": "2021-06-23 16:57:09",
  "status": 1,
  "country": null,
  "nation": null,
  "updated_at": "2021-11-03 13:50:03"
}
```

---

## 核心字段说明表

### 用户基本信息

| XG字段 | 类型 | 说明 | 映射到内部字段 |
|---|---|---|---|
| user_id | int | 用户自增ID | - |
| name | string | 姓名 | User.name |
| phone | string | 手机号 | User.phone |
| number | string | 工号/学号 | User.user_id |
| identity_id | int | 身份ID | - |
| id_card | string | 身份证 | - |
| activation_time | datetime | 激活时间 | - |
| status | int | 人员状态 | User.active |
| updated_at | datetime | 更新时间 | - |

**状态值：**
- `1`: 正常 → `active=True`
- `2`: 注销 → `active=False`

### 身份信息（user_identity对象）

```json
{
  "id": 183,
  "name": "来宾",
  "type": 1,
  "invitation_code": null,
  "validity_type": 1,
  "duration": 0,
  "deadline": null
}
```

| 字段 | 类型 | 说明 | 可选值 |
|---|---|---|---|
| id | int | 身份ID | - |
| name | string | 身份名称 | 学生、教师、来宾 |
| type | int | 身份类型 | 1=信息库内, 2=信息库外 |
| validity_type | int | 有效期类型 | 1=永久有效, 2=具体时间, 3=有效时长 |

### 部门信息（department数组）

```json
{
  "id": 47,
  "tenant_id": 46,
  "tenant_code": "C10026",
  "name": "产品测试",
  "third_code": "",
  "department_code": "C100261159409057535680",
  "level": 2,
  "parent_id": 35,
  "key": "35-",
  "sort": 6,
  "created_at": "2020-07-07 10:56:15",
  "updated_at": "2021-09-28 15:53:48",
  "deleted_at": null
}
```

| 字段 | 类型 | 说明 | 映射到内部字段 |
|---|---|---|---|
| name | string | 部门名称 | User.department |
| department_code | string | 部门唯一Code | - |
| third_code | string | 第三方系统标识 | - |
| level | int | 部门级别 | - |
| parent_id | int | 父级部门ID | - |

### 用户账号信息（user对象）

```json
{
  "id": 1401,
  "tenant_id": 46,
  "tenant_code": "C10026",
  "phone": "18626409896",
  "number": "",
  "status": 3,
  "one_card_status": 0
}
```

| 字段 | 类型 | 说明 | 可选值 |
|---|---|---|---|
| phone | string | 手机号 | - |
| number | string | 工号/学号 | - |
| status | int | 账号状态 | 1=未认证, 2=待审核, 3=审核通过, 4=审核不通过 |
| one_card_status | int | 一卡通状态 | 0=未绑定, 1=已绑定, 2=已解绑, 3=已挂失 |

### 扩展字段（user_auth_extra_field数组）

```json
{
  "id": 448,
  "user_auth_id": 41388,
  "key": "h8WxQd_sLeYqz",
  "name": "身高",
  "value": "XX"
}
```

| 字段 | 说明 |
|---|---|
| name | 扩展字段名称 |
| value | 扩展字段值 |

### 微信信息（we_chat对象）

```json
{
  "id": 523,
  "user_id": 327,
  "user_code": "o2dY06ayLwoWmAFtcyZW3yGAXa4Y",
  "nickname": "YANG",
  "headimgurl": "https://..."
}
```

| 字段 | 说明 |
|---|---|
| user_code | 微信openId |
| nickname | 微信昵称 |
| headimgurl | 微信头像 |

---

## 字段映射规则

### XG → 内部系统映射表

| XG字段路径 | 内部User模型字段 | 转换规则 |
|---|---|---|
| `number` | `user_id` | 直接映射（学号） |
| `name` | `name` | 直接映射 |
| `phone` | `phone` | 直接映射 |
| `department[0].name` | `department` | 取第一个部门名称 |
| `status` | `active` | 1→True, 2→False |
| `user_identity.name` | `role` | 需要映射规则（学生/教师→对应角色） |

### 提取规则（参考backend/apps/users/integrations/xg_user_mapper.py）

1. **用户ID提取：** `number` 字段
2. **姓名提取：** `name` 字段
3. **手机号提取：** `phone` 或 `user.phone` （优先前者）
4. **部门提取：** `department[0].name` （取第一个部门）
5. **状态映射：** `status == 1` → `active=True`

---

## 数据验证要点

### 必填字段验证
- ✓ `number` 不为空（作为user_id）
- ✓ `name` 不为空
- ✓ `phone` 格式正确（11位数字）

### 数据完整性
- ✓ `department` 数组至少有一个元素
- ✓ `user_identity` 对象存在
- ✓ `updated_at` 时间戳有效

### 特殊情况处理
- `phone` 为null → 从 `user.phone` 提取
- `department` 为空 → department字段为null
- `status` != 1 → 标记为inactive

---

**相关文件：**
- API文档原文：`docs/api说明.txt`
- 映射器代码：`backend/apps/users/integrations/xg_user_mapper.py`
- 客户端代码：`backend/apps/users/integrations/xg_user_client.py`
- 同步服务：`backend/apps/users/services/xg_user_sync.py`
