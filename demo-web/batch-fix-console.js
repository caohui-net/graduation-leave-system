// 临时修复脚本 - 在浏览器控制台粘贴执行
// 用途：修复批量审批undefined问题，无需刷新页面

(function() {
  console.log('[TEMP-FIX] Installing batch approval fix...');

  // 保存原函数
  window._originalConfirmBatchAction = window.confirmBatchAction;

  // 覆盖批量审批函数
  window.confirmBatchAction = async function() {
    console.log('[TEMP-FIX] Batch action triggered, fetching real approval IDs...');

    const checkboxes = document.querySelectorAll('.approval-checkbox:checked');
    const comment = document.getElementById('batch-comment').value;

    if (checkboxes.length === 0) {
      alert('请选择要操作的审批');
      return;
    }

    try {
      // 1. 从API获取所有pending审批
      const response = await fetch(API_BASE_URL + '/approvals/?decision=pending&limit=500', {
        headers: getAuthHeaders()
      });

      if (!response.ok) {
        throw new Error('获取审批列表失败');
      }

      const data = await response.json();
      console.log('[TEMP-FIX] Fetched approvals:', data.results.length);

      // 2. 构建 appId -> approvalId 映射
      const appToApprovalMap = {};
      data.results.forEach(approval => {
        if (approval.application && approval.application.id) {
          appToApprovalMap[approval.application.id] = approval.id;
        }
      });

      // 3. 从checkbox所在卡片提取appId，映射到真实approvalId
      const validIds = [];
      checkboxes.forEach(cb => {
        const card = cb.closest('.card');
        if (!card) return;

        // 从onclick属性提取application_id
        const clickable = card.querySelector('[onclick*="openApplication"]');
        if (clickable) {
          const onclick = clickable.getAttribute('onclick');
          const match = onclick.match(/openApplication\('([^']+)'\)/);

          if (match && match[1]) {
            const appId = match[1];
            const approvalId = appToApprovalMap[appId];

            if (approvalId) {
              validIds.push(approvalId);
              console.log('[TEMP-FIX] Mapped:', appId, '->', approvalId);
            } else {
              console.warn('[TEMP-FIX] No approval found for app:', appId);
            }
          }
        }
      });

      if (validIds.length === 0) {
        alert('无法获取有效的审批ID，请联系管理员');
        console.error('[TEMP-FIX] No valid IDs found');
        return;
      }

      console.log('[TEMP-FIX] Submitting with IDs:', validIds);

      // 4. 提交批量操作
      const res = await fetchWithTimeout(API_BASE_URL + '/approvals/batch-action/', {
        method: 'POST',
        headers: {...getAuthHeaders(), 'Content-Type': 'application/json'},
        body: JSON.stringify({
          approval_ids: validIds,
          action: batchAction,
          comment: comment
        })
      });

      const result = await res.json();

      // 5. 关闭模态框
      const modal = document.getElementById('batch-confirm-modal');
      if (modal) modal.style.display = 'none';

      // 6. 显示结果
      if (res.ok) {
        showToast(`批量${batchAction === 'approve' ? '通过' : '驳回'}成功`, 'success');
        loadApprovals();
        const bar = document.getElementById('batch-action-bar');
        if (bar) bar.style.display = 'none';
      } else {
        showToast(result.error?.message || '操作失败', 'error');
        console.error('[TEMP-FIX] API error:', result.error);
      }

    } catch (err) {
      console.error('[TEMP-FIX] Exception:', err);

      const modal = document.getElementById('batch-confirm-modal');
      if (modal) modal.style.display = 'none';

      showToast('操作失败：' + err.message, 'error');
    }
  };

  console.log('[TEMP-FIX] ✓ Fix installed. Batch approval now works.');
  console.log('[TEMP-FIX] Permanent fix: use index-v2.html or clear browser cache');
})();
