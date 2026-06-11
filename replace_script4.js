const fs = require('fs');
let html = fs.readFileSync('demo-web/index.html', 'utf8');

html = html.replace('function openApproval(id) {\n        currentApprovalId = id;\n        showScreen(2);\n    }', 
"async function openApproval(id) {\n" +
"        currentApprovalId = id;\n" +
"        showScreen(2);\n" +
"        \n" +
"        const res = await fetch(API_BASE_URL + '/approvals/' + id + '/', {\n" +
"            headers: getAuthHeaders()\n" +
"        });\n" +
"        if (res.ok) {\n" +
"            const detail = await res.json();\n" +
"            const container = document.querySelector('#screen-2');\n" +
"            \n" +
"            const basicInfoHtml = '<div class=\"card\">' +\n" +
"                '<div style=\"font-size: 16px; font-weight: bold; margin-bottom: 10px;\">基本信息</div>' +\n" +
"                '<div style=\"display: flex; margin-bottom: 8px;\">' +\n" +
"                  '<span style=\"font-size: 14px; color: #999; width: 80px;\">申请ID:</span>' +\n" +
"                  '<span style=\"font-size: 14px; color: #333; flex: 1;\">' + (detail.application_id || detail.id.substring(0,8)) + '</span>' +\n" +
"                '</div>' +\n" +
"                '<div style=\"display: flex; margin-bottom: 8px;\">' +\n" +
"                  '<span style=\"font-size: 14px; color: #999; width: 80px;\">学生:</span>' +\n" +
"                  '<span style=\"font-size: 14px; color: #333; flex: 1;\">' + (detail.student_name || '-') + ' (' + (detail.student_id || '-') + ')</span>' +\n" +
"                '</div>' +\n" +
"                '<div style=\"display: flex; margin-bottom: 8px;\">' +\n" +
"                  '<span style=\"font-size: 14px; color: #999; width: 80px;\">联系电话:</span>' +\n" +
"                  '<span style=\"font-size: 14px; color: #333; flex: 1;\">' + (detail.contact_phone || '-') + '</span>' +\n" +
"                '</div>' +\n" +
"                '<div style=\"display: flex; margin-bottom: 8px;\">' +\n" +
"                  '<span style=\"font-size: 14px; color: #999; width: 80px;\">申请原因:</span>' +\n" +
"                  '<span style=\"font-size: 14px; color: #333; flex: 1;\">' + (detail.reason || '无') + '</span>' +\n" +
"                '</div>' +\n" +
"              '</div>';\n" +
"            \n" +
"            const cards = container.querySelectorAll('.card');\n" +
"            if (cards.length > 0) {\n" +
"                cards[0].outerHTML = basicInfoHtml;\n" +
"            }\n" +
"        }\n" +
"    }");

fs.writeFileSync('demo-web/index.html', html);
