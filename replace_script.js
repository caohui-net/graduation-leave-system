const fs = require('fs');

let html = fs.readFileSync('demo-web/index.html', 'utf8');

// Inject api script tag
html = html.replace('<link rel="stylesheet" href="css/global.css">', '<link rel="stylesheet" href="css/global.css">\n  <script src="js/api.js"></script>');

// 1. Hook up the switchRole to login
html = html.replace('function switchRole(role) {', 'async function switchRole(role) {\n      const loggedIn = await apiLogin(role);\n      if (!loggedIn) {\n          console.error("Failed to login as", role);\n      } else {\n          console.log("Logged in as", role);\n          if (role !== "student") {\n             loadApprovals();\n          }\n      }');

// 2. Add loadApprovals function
const extraScript = "\n" +
"    async function loadApprovals() {\n" +
"        if (!currentToken) return;\n" +
"        const data = await apiGetApprovals();\n" +
"        const listContainer = document.querySelector('#screen-1 .card').parentNode;\n" +
"        \n" +
"        // Status map based on backend expectations\n" +
"        const statusMap = {\n" +
"            'pending_dorm_manager': { text: '待宿管审批', cls: 'tag-pending' },\n" +
"            'pending_counselor': { text: '待辅导员审批', cls: 'tag-pending' },\n" +
"            'pending_dean': { text: '待学工部审批', cls: 'tag-pending' },\n" +
"            'approved': { text: '已通过', cls: 'tag-approved' },\n" +
"            'rejected': { text: '已拒绝', cls: 'tag-rejected' }\n" +
"        };\n" +
"\n" +
"        if (data.results && data.results.length > 0) {\n" +
"            let htmlStr = '';\n" +
"            data.results.forEach(app => {\n" +
"                const step = statusMap[app.status] ? statusMap[app.status].text : app.status;\n" +
"                const tagCls = statusMap[app.status] ? statusMap[app.status].cls : 'tag-pending';\n" +
"                \n" +
"                htmlStr += '<div class=\"card\" onclick=\"openApproval(\\'' + app.id + '\\')\" style=\"cursor: pointer;\">' +\n" +
"                  '<div class=\"flex-row justify-between align-center\" style=\"margin-bottom: 8px;\">' +\n" +
"                    '<span style=\"font-size: 16px; font-weight: bold;\">申请 ' + (app.application_id || app.id.substring(0,8)) + '</span>' +\n" +
"                    '<span class=\"tag ' + tagCls + '\">' + step + '</span>' +\n" +
"                  '</div>' +\n" +
"                  '<div style=\"margin-bottom: 4px;\">' +\n" +
"                    '<span style=\"font-size: 14px; color: #999; margin-right: 8px;\">学生:</span>' +\n" +
"                    '<span style=\"font-size: 14px; color: #333;\">' + app.student_name + ' (' + app.student_id + ')</span>' +\n" +
"                  '</div>' +\n" +
"                  '<div style=\"margin-top: 8px; padding-top: 8px; border-top: 1px solid #f0f0f0;\">' +\n" +
"                    '<span style=\"font-size: 12px; color: #999;\">' + new Date(app.created_at).toLocaleString() + '</span>' +\n" +
"                  '</div>' +\n" +
"                '</div>';\n" +
"            });\n" +
"            listContainer.innerHTML = htmlStr;\n" +
"        } else {\n" +
"             listContainer.innerHTML = '<div style=\"text-align:center; padding: 20px; color:#999;\">暂无数据</div>';\n" +
"        }\n" +
"    }\n" +
"    \n" +
"    let currentApprovalId = null;\n" +
"    function openApproval(id) {\n" +
"        currentApprovalId = id;\n" +
"        showScreen(2);\n" +
"    }\n" +
"    \n" +
"    async function doApprove() {\n" +
"        if(!currentApprovalId) return;\n" +
"        const comment = document.getElementById('approvalComment').value;\n" +
"        const ok = await apiApprove(currentApprovalId, comment);\n" +
"        if(ok) { alert('审批通过'); showScreen(1); loadApprovals(); }\n" +
"        else { alert('审批失败'); }\n" +
"    }\n" +
"\n" +
"    async function doReject() {\n" +
"        if(!currentApprovalId) return;\n" +
"        const comment = document.getElementById('approvalComment').value;\n" +
"        const ok = await apiReject(currentApprovalId, comment);\n" +
"        if(ok) { alert('审批拒绝'); showScreen(1); loadApprovals(); }\n" +
"        else { alert('审批失败'); }\n" +
"    }\n" +
"    \n" +
"    async function doSubmitApplication() {\n" +
"        const phone = document.getElementById('contactPhone').value;\n" +
"        const reason = document.getElementById('applicationReason').value;\n" +
"        if (!phone) {\n" +
"             alert('请输入联系电话');\n" +
"             return;\n" +
"        }\n" +
"        const ok = await apiSubmitApplication(phone, reason, uploadedFiles);\n" +
"        if (ok) {\n" +
"            alert('申请提交成功');\n" +
"            document.getElementById('contactPhone').value = '';\n" +
"            document.getElementById('applicationReason').value = '';\n" +
"            uploadedFiles = [];\n" +
"            renderFileList();\n" +
"        } else {\n" +
"            alert('申请提交失败');\n" +
"        }\n" +
"    }\n" +
"</script>";

html = html.replace('</script>', extraScript);

// 3. Update Submit Button
html = html.replace('<button class="btn-primary">提交申请</button>', '<button class="btn-primary" onclick="doSubmitApplication()">提交申请</button>');

// 4. Update text area id
html = html.replace('<textarea style="width: 100%; min-height: 120px; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入离校原因"></textarea>', '<textarea id="applicationReason" style="width: 100%; min-height: 120px; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入离校原因"></textarea>');

// 5. Update Approval buttons
html = html.replace('<button class="btn-primary" style="flex: 1;">通过</button>', '<button class="btn-primary" style="flex: 1;" onclick="doApprove()">通过</button>');
html = html.replace('<button class="btn-outline" style="flex: 1;">拒绝</button>', '<button class="btn-outline" style="flex: 1;" onclick="doReject()">拒绝</button>');

// 6. Update Comment area id
html = html.replace('<textarea style="width: 100%; min-height: 60px; padding: 8px; border: 1px solid #e8e8e8; border-radius: 4px; font-size: 14px;" placeholder="请输入审批意见"></textarea>', '<textarea id="approvalComment" style="width: 100%; min-height: 60px; padding: 8px; border: 1px solid #e8e8e8; border-radius: 4px; font-size: 14px;" placeholder="请输入审批意见"></textarea>');

fs.writeFileSync('demo-web/index.html', html);
