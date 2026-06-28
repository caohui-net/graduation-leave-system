"""业务流程测试辅助函数

这些函数封装常见的浏览器操作，供测试脚本复用。
使用browser-harness的自愈合特性，可在运行时自动改进。
"""
import time

def login(user_id, password, business_type=None):
    """登录系统

    Args:
        user_id: 用户ID
        password: 密码
        business_type: 业务类型 ('departure' | 'stay' | None)
    """
    js(f"""
        const userInput = document.querySelector('input[placeholder*="用户"]');
        const passInput = document.querySelector('input[type="password"]');
        if (userInput) userInput.value = '{user_id}';
        if (passInput) passInput.value = '{password}';
    """)
    time.sleep(0.5)

    js("Array.from(document.querySelectorAll('button')).find(el => el.innerText.includes('登录'))?.click()")
    time.sleep(3)
    wait_for_load()

    # 选择业务类型
    if business_type == 'stay':
        js("Array.from(document.querySelectorAll('button, div')).find(el => el.innerText.includes('留校审批'))?.click()")
        time.sleep(2)
        wait_for_load()
    elif business_type == 'departure':
        js("Array.from(document.querySelectorAll('button, div')).find(el => el.innerText.includes('离校审批'))?.click()")
        time.sleep(2)
        wait_for_load()


def check_login_success():
    """验证登录是否成功"""
    return js("""
        ({
            hasApprovalList: document.body.innerText.includes('审批') || document.body.innerText.includes('申请'),
            hasLoginForm: !!document.querySelector('input[placeholder*="用户"]'),
            hasCookies: document.cookie.length > 0
        })
    """)


def filter_by_student_id(student_id):
    """按学号筛选

    Args:
        student_id: 学号

    Returns:
        bool: 是否找到目标学号
    """
    js(f"""
        const input = document.querySelector('input[placeholder*="学号"]') ||
                     document.querySelector('input[placeholder*="查询"]') ||
                     document.querySelector('input[type="search"]');
        if (input) {{
            input.value = '{student_id}';
            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            input.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    """)
    time.sleep(2)

    return js(f"document.body.innerText.includes('{student_id}')")


def get_table_data():
    """获取表格数据"""
    return js("""
        Array.from(document.querySelectorAll('table tbody tr')).map(row =>
            Array.from(row.querySelectorAll('td')).map(cell => cell.innerText.trim())
        )
    """)


def click_button(text):
    """点击包含指定文本的按钮"""
    js(f"Array.from(document.querySelectorAll('button')).find(el => el.innerText.includes('{text}'))?.click()")
    time.sleep(1)


def fill_form(data):
    """填写表单

    Args:
        data: dict, key为字段名（placeholder或name），value为值
    """
    for field, value in data.items():
        js(f"""
            const input = document.querySelector('input[placeholder*="{field}"]') ||
                         document.querySelector('input[name*="{field}"]');
            if (input) {{
                input.value = '{value}';
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
        """)
    time.sleep(0.5)


def get_page_state():
    """获取页面状态信息"""
    return js("""
        ({
            url: window.location.href,
            title: document.title,
            hasTable: !!document.querySelector('table'),
            tableRows: document.querySelectorAll('table tbody tr').length,
            buttons: Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()),
            alerts: Array.from(document.querySelectorAll('.alert, [role="alert"]')).map(a => a.innerText.trim())
        })
    """)
