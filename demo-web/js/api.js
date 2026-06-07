// API Integration Layer
const API_BASE_URL = 'http://localhost:8001/api';

let currentToken = null;
let currentUser = null;

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

async function apiGetApprovals() {
    try {
        const response = await fetch(API_BASE_URL + '/approvals/', {
            headers: getAuthHeaders()
        });
        if (response.ok) {
            return await response.json();
        }
    } catch (e) {
        console.error("Get approvals failed:", e);
    }
    return [];
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
