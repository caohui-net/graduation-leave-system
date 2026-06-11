const fs = require('fs');
let html = fs.readFileSync('demo-web/index.html', 'utf8');

// The original role map is missing student because I replaced the entire function
// Need to add it back correctly
html = html.replace("const roleMap = {\\n        'dorm_manager': '宿管员',\\n        'counselor': '辅导员',\\n        'dean': '学工部'\\n      };", 
"const roleMap = {\\n        'student': '学生',\\n        'dorm_manager': '宿管员',\\n        'counselor': '辅导员',\\n        'dean': '学工部'\\n      };");

html = html.replace("const isDean = role === 'dean';", "const isStudent = role === 'student';\n      const isDean = role === 'dean';");
html = html.replace("document.getElementById('nav-approval-text').textContent = isDean ? '备案查询' : '审批列表';", "document.getElementById('nav-approval-text').textContent = (isStudent || isDean) ? '我的申请' : '审批列表';");

fs.writeFileSync('demo-web/index.html', html);
