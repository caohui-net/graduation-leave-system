# 前端缓存控制配置指南

**问题：** 浏览器缓存HTML导致bug修复延迟生效

**解决方案：** 3层防护机制

---

## 层1 - 前端版本检测（已实现）

**位置：** `demo-web/index.html` (第12-24行)

**机制：**
- 每次页面加载检查版本号
- 版本不匹配自动刷新（带nocache参数）
- 强制加载最新代码

**维护：**
每次重要修复后，更新版本号：
```javascript
const APP_VERSION = '20260616-fix2'; // ← 递增此版本号
```

**效果：** 用户下次访问自动获取新版本

---

## 层2 - 服务端Cache-Control配置

### Nginx配置

**文件：** `/etc/nginx/sites-available/graduation-system` 或对应配置文件

**添加配置：**
```nginx
server {
    listen 7788;
    root /path/to/demo-web;

    # HTML文件禁止缓存
    location ~* \.html$ {
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        add_header Expires "0";
    }

    # JS/CSS文件长期缓存（依赖版本号）
    location ~* \.(js|css)$ {
        add_header Cache-Control "public, max-age=31536000";
    }

    # 其他静态资源
    location ~* \.(jpg|jpeg|png|gif|ico|svg)$ {
        add_header Cache-Control "public, max-age=86400";
    }
}
```

**重启Nginx：**
```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### dufs配置（如使用dufs）

**启动参数：**
```bash
dufs /path/to/demo-web \
  --port 7788 \
  --render-index \
  --header "Cache-Control: no-cache" \
  --header "Pragma: no-cache"
```

---

### Python http.server配置

**方法1 - 自定义Handler：**
```python
# serve.py
from http.server import SimpleHTTPRequestHandler, HTTPServer

class NoCacheHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        SimpleHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
    HTTPServer(('0.0.0.0', 7788), NoCacheHTTPRequestHandler).serve_forever()
```

**运行：**
```bash
cd /path/to/demo-web
python3 serve.py
```

---

## 层3 - 部署脚本自动化

**文件：** `scripts/deploy-frontend.sh`

```bash
#!/bin/bash
# 前端部署脚本 - 自动更新版本号

set -e

# 1. 生成新版本号
NEW_VERSION=$(date +%Y%m%d-%H%M)

# 2. 更新HTML中的APP_VERSION
sed -i "s/const APP_VERSION = '[^']*'/const APP_VERSION = '$NEW_VERSION'/" demo-web/index.html

# 3. 更新JS/CSS版本号
sed -i "s/\?v=[0-9-]*/\?v=$NEW_VERSION/g" demo-web/index.html

# 4. 重启服务（根据实际情况选择）
# sudo systemctl reload nginx
# 或
# pkill -HUP dufs

echo "✓ Frontend deployed with version: $NEW_VERSION"
```

**使用：**
```bash
bash scripts/deploy-frontend.sh
```

---

## 验证配置

### 1. 检查HTTP响应头

**方法1 - curl：**
```bash
curl -I http://218.75.196.218:7788/demo-web/index.html
```

**期望输出：**
```
Cache-Control: no-cache, no-store, must-revalidate
Pragma: no-cache
Expires: 0
```

**方法2 - 浏览器开发者工具：**
1. F12 → Network标签
2. 刷新页面
3. 点击`index.html`
4. 查看Response Headers

### 2. 测试版本检测

**控制台执行：**
```javascript
// 模拟旧版本
localStorage.setItem('app_version', 'old-version');
location.reload();
// 应自动刷新并更新为新版本
```

---

## 应急方案

**如用户仍遇到缓存问题：**

1. **URL参数破缓存：**
   ```
   http://218.75.196.218:7788/demo-web/index.html?t=时间戳
   ```

2. **提供清除缓存指引：**
   - Chrome: Ctrl+Shift+Delete → 清除缓存
   - 或开发者工具 → 勾选"Disable cache"

3. **备用URL：**
   创建`index-v2.html`，发送给用户

---

## 监控与维护

### 版本历史记录

**文件：** `demo-web/CHANGELOG.md`

记录每次版本更新内容：
```markdown
## 20260616-fix2
- 修复批量审批undefined问题
- 添加版本检测机制
- 增强错误详情返回

## 20260614
- 初始版本
```

### 自动化检查

**脚本：** `scripts/check-version.sh`
```bash
#!/bin/bash
# 检查前端版本一致性

HTML_VERSION=$(grep "APP_VERSION = " demo-web/index.html | sed -E "s/.*'([^']+)'.*/\1/")
CSS_VERSION=$(grep "global.css?v=" demo-web/index.html | sed -E "s/.*v=([0-9-]+).*/\1/")
JS_VERSION=$(grep "api.js?v=" demo-web/index.html | sed -E "s/.*v=([0-9-]+).*/\1/")

echo "HTML Version: $HTML_VERSION"
echo "CSS Version:  $CSS_VERSION"
echo "JS Version:   $JS_VERSION"

if [ "$CSS_VERSION" != "$JS_VERSION" ]; then
    echo "⚠ Warning: JS/CSS version mismatch"
    exit 1
fi
```

---

**维护人员：** 曹辉（caohui）  
**创建日期：** 2026-06-16  
**最后更新：** 2026-06-16
