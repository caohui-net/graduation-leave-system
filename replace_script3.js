const fs = require('fs');
let html = fs.readFileSync('demo-web/index.html', 'utf8');

html = html.replace("const roleMap = {\n        'dorm_manager': '宿管员',\n        'counselor': '辅导员',\n        'dean': '学工部'\n      };", 
"const roleMap = {\n        'student': '学生',\n        'dorm_manager': '宿管员',\n        'counselor': '辅导员',\n        'dean': '学工部'\n      };");

html = html.replace("document.getElementById('list-title').textContent = isDean ? '备案查询' : '审批列表';", "document.getElementById('list-title').textContent = (isStudent || isDean) ? '我的申请' : '审批列表';");

fs.writeFileSync('demo-web/index.html', html);
