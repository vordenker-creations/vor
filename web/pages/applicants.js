/**
 * AI-Career Bridge - Applicants Module
 * Handles loading, filtering, rendering, updating application status, and CSV exports.
 */

import { STATE, BASE_URL, showToast } from '../app.js';

export let recruiterApplicants = [];

export async function loadApplicantsFromBackend() {
  if (!STATE.user.isLoggedIn || !STATE.user.email) return;
  
  try {
    const response = await fetch(`${BASE_URL}/recruiter/applications?email=${encodeURIComponent(STATE.user.email)}`);
    if (response.ok) {
      recruiterApplicants = await response.json();
      populateJobFilterDropdown();
      renderApplicantsTable();
    }
  } catch (error) {
    console.error("Failed to load recruiter applications:", error);
  }
}

export function populateJobFilterDropdown() {
  const dropdown = document.getElementById('filter-applicant-job');
  if (!dropdown) return;
  
  // Get unique job titles
  const jobTitles = [...new Set(recruiterApplicants.map(app => app.job_title))];
  
  dropdown.innerHTML = '<option value="">Tất cả công việc</option>' + 
    jobTitles.map(title => `<option value="${title}">${title}</option>`).join('');
}

export function renderApplicantsTable() {
  const tbody = document.getElementById('applicants-table-body');
  if (!tbody) return;
  
  const searchVal = document.getElementById('filter-applicant-search').value.toLowerCase().trim();
  const jobFilter = document.getElementById('filter-applicant-job').value;
  const statusFilter = document.getElementById('filter-applicant-status').value;
  
  const filtered = recruiterApplicants.filter(app => {
    // Search filter
    if (searchVal) {
      const matchName = (app.student_name || '').toLowerCase().includes(searchVal);
      const matchEmail = (app.student_email || '').toLowerCase().includes(searchVal);
      if (!matchName && !matchEmail) return false;
    }
    // Job title filter
    if (jobFilter && app.job_title !== jobFilter) return false;
    
    // Status filter
    if (statusFilter && app.application_status !== statusFilter) return false;
    
    return true;
  });
  
  if (filtered.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" class="px-5 py-8 text-center text-slate-500">
          Không tìm thấy hồ sơ ứng cử nào.
        </td>
      </tr>
    `;
    return;
  }
  
  tbody.innerHTML = filtered.map(app => {
    const studentName = app.student_name || "Sinh viên ẩn danh";
    const appliedDate = app.applied_at ? app.applied_at.split(' ')[0] : 'N/A';
    
    // Dropdown selection for status updates
    const statusSelect = `
      <select onchange="updateApplicationStatus(${app.application_id}, this.value)" class="bg-brand-card border border-slate-800 text-xs font-semibold rounded-lg px-2 py-1 outline-none text-slate-300 focus:border-cyan-500/50">
        <option value="applied" ${app.application_status === 'applied' ? 'selected' : ''}>Đã nộp</option>
        <option value="reviewing" ${app.application_status === 'reviewing' ? 'selected' : ''}>Đang duyệt</option>
        <option value="interview" ${app.application_status === 'interview' ? 'selected' : ''}>Hẹn phỏng vấn</option>
        <option value="accepted" ${app.application_status === 'accepted' ? 'selected' : ''}>Nhận việc</option>
        <option value="rejected" ${app.application_status === 'rejected' ? 'selected' : ''}>Từ chối</option>
      </select>
    `;
    
    // Display badges for current status
    let statusBadgeClass = 'bg-slate-900 border-slate-800 text-slate-400';
    let statusLabel = 'Đã nộp';
    if (app.application_status === 'reviewing') {
      statusBadgeClass = 'bg-yellow-500/10 border-yellow-500/20 text-yellow-400';
      statusLabel = 'Đang duyệt';
    } else if (app.application_status === 'interview') {
      statusBadgeClass = 'bg-cyan-500/10 border-cyan-500/20 text-cyan-400';
      statusLabel = 'Hẹn phỏng vấn';
    } else if (app.application_status === 'accepted') {
      statusBadgeClass = 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400';
      statusLabel = 'Nhận việc';
    } else if (app.application_status === 'rejected') {
      statusBadgeClass = 'bg-red-500/10 border-red-500/20 text-red-400';
      statusLabel = 'Từ chối';
    }
    
    const statusBadge = `
      <span class="inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-bold border ${statusBadgeClass}">
        ${statusLabel}
      </span>
    `;

    return `
      <tr class="hover:bg-slate-900/10 transition duration-150">
        <td class="px-5 py-4 font-bold text-white flex flex-col">
          <span>${studentName}</span>
          <span class="text-[10px] text-slate-500 font-medium">${app.student_email}</span>
        </td>
        <td class="px-5 py-4">
          <p class="font-medium text-slate-200">${app.student_major || 'Kỹ thuật Phần mềm'}</p>
          <span class="text-[10px] text-slate-500">Năm ${app.student_year || 1}</span>
        </td>
        <td class="px-5 py-4 text-cyan-400 font-semibold">${app.job_title}</td>
        <td class="px-5 py-4 text-slate-400">${appliedDate}</td>
        <td class="px-5 py-4">${statusBadge}</td>
        <td class="px-5 py-4 text-right flex items-center justify-end gap-3.5">
          ${statusSelect}
          <button onclick="showApplicantDetailsFromTable(${app.application_id})" class="text-slate-400 hover:text-white p-1" title="Chi tiết ứng viên">
            <i data-lucide="eye" class="w-4 h-4"></i>
          </button>
        </td>
      </tr>
    `;
  }).join('');
  
  if (window.lucide) window.lucide.createIcons();
}

export function filterApplicantsTable() {
  renderApplicantsTable();
}

export async function updateApplicationStatus(applicationId, newStatus) {
  try {
    const response = await fetch(`${BASE_URL}/applications/${applicationId}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        status: newStatus,
        email: STATE.user.email
      })
    });
    
    if (response.ok) {
      showToast("Đã cập nhật trạng thái hồ sơ ứng viên.");
      await loadApplicantsFromBackend();
    } else {
      const err = await response.json();
      showToast(err.detail || "Không thể cập nhật trạng thái.", "error");
    }
  } catch (error) {
    console.error("Error updating application status:", error);
    showToast("Lỗi kết nối khi cập nhật hồ sơ.", "error");
  }
}

export function exportApplicantsCSV() {
  if (recruiterApplicants.length === 0) {
    showToast("Không có dữ liệu ứng viên để xuất.", "error");
    return;
  }
  
  // Create CSV Header
  const headers = ["ID", "Tên Sinh viên", "Email Sinh viên", "Ngành Học", "Năm Học", "Vị trí ứng tuyển", "Ngày nộp", "Trạng thái"];
  const rows = recruiterApplicants.map(app => [
    app.application_id,
    `"${app.student_name || 'N/A'}"`,
    app.student_email,
    `"${app.student_major || 'N/A'}"`,
    app.student_year || 1,
    `"${app.job_title}"`,
    app.applied_at || 'N/A',
    app.application_status
  ]);
  
  const csvContent = "\uFEFF" + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement("a");
  link.setAttribute("href", url);
  link.setAttribute("download", `Danh_sach_ung_vien_${STATE.user.name.replace(/\s+/g, '_')}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  
  showToast("Tải về tệp CSV thành công!");
}

export function showApplicantDetailsFromTable(applicationId) {
  const app = recruiterApplicants.find(a => a.application_id === applicationId);
  if (!app) return;
  
  const applicantObj = {
    name: app.student_name,
    email: app.student_email,
    major: app.student_major,
    student_year: app.student_year,
    job_title: app.job_title,
    job_company: app.job_company
  };
  
  if (window.showApplicantDetails) {
    window.showApplicantDetails(applicantObj);
  }
}

// Bind to window for HTML inline access
window.updateApplicationStatus = updateApplicationStatus;
window.exportApplicantsCSV = exportApplicantsCSV;
window.filterApplicantsTable = filterApplicantsTable;
window.showApplicantDetailsFromTable = showApplicantDetailsFromTable;
window.loadApplicantsFromBackend = loadApplicantsFromBackend;
