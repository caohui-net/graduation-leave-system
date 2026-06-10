// API Integration Layer
const API_BASE_URL = `http://${window.location.hostname}:7787/api`;

let currentToken = null;
let currentUser = null;

// 页面加载时自动恢复登录状态
function restoreAuthState() {
    const savedToken = localStorage.getItem('auth_token');
    const savedUser = localStorage.getItem('user_info');

    if (savedToken) {
        currentToken = savedToken;
        if (savedUser) {
            try {
                currentUser = JSON.parse(savedUser);
                console.log('Auth state restored from localStorage', currentUser);
            } catch (e) {
                console.error('Failed to parse user info:', e);
            }
        }
    }
}

// 恢复登录后初始化UI
function initializeUIAfterRestore(user) {
    // 隐藏登录界面
    const loginScreen = document.getElementById('screen-login');
    if (loginScreen && loginScreen.classList.contains('active')) {
        loginScreen.classList.remove('active');

        // 显示导航栏和用户栏
        const navTabs = document.getElementById('navTabs');
        const userBar = document.getElementById('userBar');
        if (navTabs) navTabs.style.display = 'flex';
        if (userBar) userBar.style.display = 'flex';

        // 显示用户信息
        const userNameEl = document.getElementById('currentUserName');
        const userRoleEl = document.getElementById('currentUserRole');
        if (userNameEl && user.real_name) userNameEl.textContent = user.real_name;
        if (userRoleEl && user.role) {
            const roleMap = { 'student': '学生', 'dorm_manager': '宿管', 'counselor': '辅导员', 'dean': '学工部', 'admin': '管理员' };
            userRoleEl.textContent = '(' + (roleMap[user.role] || user.role) + ')';
        }

        // 根据角色显示对应界面
        if (user.role === 'student') {
            if (typeof showScreen === 'function') showScreen(0);
        } else {
            if (typeof showScreen === 'function') showScreen(2); // 审批界面
        }

        console.log('UI initialized for user:', user.username);
    }
}

// 页面加载时立即执行
restoreAuthState();

async function apiLogin(userId, password) {
    try {
        const response = await fetch(API_BASE_URL + '/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: userId,
                password: password
            })
        });

        if (response.ok) {
            const data = await response.json();
            currentToken = data.access_token;
            currentUser = data.user;
            return { success: true, user: data.user };
        } else {
            currentToken = null;
            currentUser = null;
            const error = await response.json().catch(() => ({ error: 'Login failed' }));
            return { success: false, error: error };
        }
    } catch (e) {
        console.error("Login failed:", e);
        currentToken = null;
        currentUser = null;
        return { success: false, error: 'Network error' };
    }
}

function getAuthHeaders() {
    return {
        'Authorization': 'Bearer ' + currentToken
    };
}

async function apiSubmitApplication(phone, reason, leaveDate, files) {
    const formData = new FormData();
    formData.append('contact_phone', phone);
    formData.append('reason', reason);
    formData.append('leave_date', leaveDate);
    files.forEach(f => formData.append('attachments', f));

    try {
        const response = await fetch(API_BASE_URL + '/applications/', {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + currentToken },
            body: formData
        });
        if (response.ok) {
            return { success: true, data: await response.json() };
        } else {
            const error = await response.json().catch(() => ({ error: { message: '提交失败' } }));
            return { success: false, error: error.error || { message: '提交失败' } };
        }
    } catch (e) {
        console.error("Submit application failed:", e);
        return { success: false, error: { message: '网络错误，请检查连接' } };
    }
}

async function apiGetApplications() {
    try {
        const response = await fetch(API_BASE_URL + '/applications/', {
            headers: getAuthHeaders()
        });
        if (response.ok) {
            return await response.json();
        }
    } catch (e) {
        console.error("Get applications failed:", e);
    }
    return { results: [] };
}

async function apiGetApprovals(decision = 'pending', limit = 20, offset = 0) {
    try {
        const url = API_BASE_URL + '/approvals/?decision=' + decision + '&limit=' + limit + '&offset=' + offset;
        const response = await fetch(url, {
            headers: getAuthHeaders()
        });
        if (response.ok) {
            return await response.json();
        }
    } catch (e) {
        console.error("Get approvals failed:", e);
    }
    return { results: [], count: 0 };
}

async function apiApprove(approvalId, comment) {
    try {
        const response = await fetch(API_BASE_URL + '/approvals/' + approvalId + '/approve/', {
            method: 'POST',
            headers: Object.assign({}, getAuthHeaders(), { 'Content-Type': 'application/json' }),
            body: JSON.stringify({ comment: comment })
        });
        return response.ok;
    } catch (e) {
        console.error("Approve failed:", e);
        return false;
    }
}

async function apiReject(approvalId, comment) {
    try {
        const response = await fetch(API_BASE_URL + '/approvals/' + approvalId + '/reject/', {
            method: 'POST',
            headers: Object.assign({}, getAuthHeaders(), { 'Content-Type': 'application/json' }),
            body: JSON.stringify({ comment: comment })
        });
        return response.ok;
    } catch (e) {
        console.error("Reject failed:", e);
        return false;
    }
}

async function apiUploadAttachment(applicationId, file, attachmentType = 'other') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('attachment_type', attachmentType);

    try {
        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/', {
            method: 'POST',
            headers: getAuthHeaders(),
            body: formData
        });
        if (response.ok) {
            return await response.json();
        }
    } catch (e) {
        console.error("Upload attachment failed:", e);
    }
    return null;
}

async function apiGetAttachments(applicationId) {
    try {
        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/', {
            headers: getAuthHeaders()
        });
        if (response.ok) {
            return await response.json();
        }
    } catch (e) {
        console.error("Get attachments failed:", e);
    }
    return [];
}

async function apiDeleteAttachment(applicationId, attachmentId) {
    try {
        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/' + attachmentId + '/', {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        return response.ok;
    } catch (e) {
        console.error("Delete attachment failed:", e);
        return false;
    }
}

// DOM加载完成后，如果有token则自动初始化UI
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', function() {
        if (currentToken && currentUser) {
            console.log('Initializing UI after token restore');
            initializeUIAfterRestore(currentUser);
        }
    });
}
