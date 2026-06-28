# E2E业务流程测试框架

基于 browser-harness 的自愈合浏览器测试框架，用于本项目的业务流程自动化测试。

## 快速开始

### 前置条件

1. **安装 browser-harness**（如未安装）
   ```bash
   uv tool install browser-harness
   ```

2. **启动浏览器调试**
   - 打开 Chrome: `chrome://inspect/#remote-debugging`
   - 勾选 "Discover network targets"
   - 允许远程调试（Chrome 144+）

3. **启动本地服务**
   ```bash
   # 后端
   cd backend && source venv/bin/activate
   python manage.py runserver 0.0.0.0:8000
   
   # 前端
   python scripts/serve-frontend.py
   ```

### 运行测试

```bash
cd tests/e2e

# 运行所有测试
./run_tests.sh

# 运行指定测试
./run_tests.sh login        # 登录流程测试
./run_tests.sh stay         # 留校审批测试
```

## 测试结构

```
tests/e2e/
├── config/
│   └── test_config.py          # 测试配置（URL、账号、超时）
├── helpers/
│   └── common.py               # 可复用辅助函数
├── flows/
│   ├── test_login.py           # 登录流程测试
│   └── test_stay_approval.py   # 留校审批测试
└── run_tests.sh                # 测试运行器
```

## 已实现测试

### 1. 登录流程测试 (`test_login.py`)

测试所有角色登录：
- 学生账号 (2020001)
- 辅导员账号 (19970545)
- 宿管员账号 (M001)

验证：
- 登录成功进入对应界面
- Cookies正确设置
- 会话持久性

### 2. 留校审批测试 (`test_stay_approval.py`)

测试辅导员审批流程：
1. 登录并进入留校审批模块
2. 按学号筛选数据
3. 验证筛选结果准确性

## 辅助函数库

在 `helpers/common.py` 中提供：

```python
# 登录
login(user_id, password, business_type='stay')

# 验证登录
check_login_success()

# 筛选数据
filter_by_student_id(student_id)

# 获取表格数据
get_table_data()

# 点击按钮
click_button(text)

# 填写表单
fill_form({'字段名': '值'})

# 获取页面状态
get_page_state()
```

## 编写新测试

### 示例：创建离校申请测试

```python
#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config.test_config import BASE_URL, TEST_ACCOUNTS
from helpers.common import login, fill_form, click_button

def test_departure_application():
    """测试离校申请流程"""
    new_tab(BASE_URL)
    wait_for_load()
    
    # 学生登录
    student = TEST_ACCOUNTS['student']
    login(student['user_id'], student['password'], business_type='departure')
    
    # 填写申请表单
    fill_form({
        '联系电话': '13800138000',
        '离校日期': '2026-07-01'
    })
    
    # 提交申请
    click_button('提交')
    
    # 验证提交成功
    state = get_page_state()
    return '提交成功' in str(state['alerts'])

if __name__ == '__main__':
    success = test_departure_application()
    sys.exit(0 if success else 1)
```

保存为 `flows/test_departure_application.py`，并在 `run_tests.sh` 中添加对应case。

## 配置说明

### 环境变量

在 `config/test_config.py` 或通过环境变量设置：

```bash
# 测试目标URL
export E2E_BASE_URL=http://172.17.12.196:7788

# CDP端点（默认本地）
export BU_CDP_URL=http://127.0.0.1:9222
```

### 测试账号

默认测试账号在 `config/test_config.py` 中定义：

```python
TEST_ACCOUNTS = {
    'student': {'user_id': '2020001', 'password': '2020001'},
    'counselor': {'user_id': '19970545', 'password': '123456'},
    'dorm_manager': {'user_id': 'M001', 'password': 'M001'}
}
```

## 自愈合特性

browser-harness 的核心优势是**运行时自我改进**：

- 首次运行遇到缺失功能时，LLM代理会自动编写辅助函数
- 生成的代码保存到 `agent_helpers.py`
- 后续运行自动使用改进后的版本

**示例**：如果测试脚本调用了 `wait_for_table_load()`（尚未定义），agent会：
1. 检测到缺失
2. 分析DOM结构
3. 生成等待逻辑
4. 保存到helpers并继续执行

## 调试技巧

### 1. 查看页面状态
```python
state = get_page_state()
print(state)  # 输出URL、按钮列表、表格行数等
```

### 2. 截图调试
```python
capture_screenshot()  # 生成截图供分析
```

### 3. 检查DOM
```python
result = js("document.body.innerText")
print(result)  # 输出页面文本内容
```

### 4. 手动运行单个测试
```bash
BU_CDP_URL=http://127.0.0.1:9222 browser-harness < flows/test_login.py
```

## CI/CD集成

### GitHub Actions 示例

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install browser-harness
        run: uv tool install browser-harness
      
      - name: Start services
        run: |
          docker-compose up -d
          
      - name: Run E2E tests
        run: cd tests/e2e && ./run_tests.sh
        env:
          E2E_BASE_URL: http://localhost:7788
          BU_CDP_URL: http://chrome:9222
```

## 故障排查

### 问题1: browser-harness: command not found

**解决**：
```bash
uv tool install browser-harness
# 或更新
uv tool upgrade browser-harness
```

### 问题2: 无法连接CDP

**检查**：
```bash
curl http://127.0.0.1:9222/json/version
```

**解决**：确保Chrome已启动远程调试

### 问题3: 登录后会话丢失

**原因**：HTTP环境下 `SESSION_COOKIE_SECURE=True`

**解决**：设置 `FORCE_HTTPS=False`（见 `docs/HTTP-DEPLOYMENT-FIX.md`）

## 扩展方向

- [ ] 离校申请完整流程测试
- [ ] 审批流程测试（通过/驳回）
- [ ] 数据导出测试
- [ ] 权限验证测试
- [ ] 性能测试（页面加载时间）
- [ ] 移动端适配测试

## 参考资料

- browser-harness GitHub: https://github.com/browser-use/browser-harness
- 本项目故障排查: `PROJECT-QUICKREF.md`
- HTTP部署修复: `docs/HTTP-DEPLOYMENT-FIX.md`

---

**维护**: 测试框架随业务迭代持续更新  
**联系**: 遇到问题查阅 `PROJECT-QUICKREF.md` 故障排查章节
