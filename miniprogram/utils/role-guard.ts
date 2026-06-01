// Role-based navigation guard to prevent duplicate redirects
let isRedirecting = false;

export function checkRoleAndRedirect(
  userInfo: any | null,
  allowedRoles: string[]
): boolean {
  if (isRedirecting) return true;

  if (!userInfo) {
    isRedirecting = true;
    wx.reLaunch({ url: '/pages/login/login' });
    setTimeout(() => { isRedirecting = false; }, 500);
    return true;
  }

  if (!allowedRoles.includes(userInfo.role)) {
    isRedirecting = true;
    const targetUrl = userInfo.role === 'student'
      ? '/pages/student-application/student-application'
      : '/pages/approvals/approvals';
    wx.redirectTo({ url: targetUrl });
    setTimeout(() => { isRedirecting = false; }, 500);
    return true;
  }

  return false;
}
