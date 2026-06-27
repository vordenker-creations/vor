/**
 * AI-Career Bridge - Job Detail Module
 * Handles displaying job details, editing, deleting, and closing/opening recruitment.
 */

import { STATE, BASE_URL, showToast, switchTab, t } from '../app.js';
import { loadJobsFromBackend } from './jobs.js';

export function renderJobDetail(jobId) {
  const detailContainer = document.getElementById('job-detail-content');
  if (!detailContainer) return;
  
  const job = STATE.jobs.find(j => j.id === jobId);
  if (!job) {
    detailContainer.innerHTML = `<p class="text-center text-slate-500 col-span-full">Job not found.</p>`;
    return;
  }

  const isOwner = STATE.user.isLoggedIn && job.posted_by === STATE.user.email;
  
  // Job recruitment status controls
  const statusLabel = job.status === 'closed' ? `
    <span class="rounded-lg bg-red-950 border border-red-800/40 px-2.5 py-1 text-xs text-red-400 font-bold">${t('detail_status_closed')}</span>
  ` : `
    <span class="rounded-lg bg-cyan-950 border border-cyan-800/40 px-2.5 py-1 text-xs text-cyan-400 font-bold">${t('detail_status_active')}</span>
  `;
 
  let toggleStatusBtn = '';
  if (isOwner) {
    if (job.status === 'closed') {
      toggleStatusBtn = `
        <button onclick="toggleJobStatus(${job.id}, 'active')" class="w-full rounded-xl py-3 border border-emerald-500/30 bg-emerald-500/5 hover:bg-emerald-500/10 text-emerald-400 hover:text-emerald-300 text-xs font-bold transition-all duration-300 mt-2 flex items-center justify-center gap-1.5">
          <i data-lucide="play" class="w-4 h-4"></i> ${t('detail_open_recruitment')}
        </button>
      `;
    } else {
      toggleStatusBtn = `
        <button onclick="toggleJobStatus(${job.id}, 'closed')" class="w-full rounded-xl py-3 border border-red-500/30 bg-red-500/5 hover:bg-red-500/10 text-red-400 hover:text-red-300 text-xs font-bold transition-all duration-300 mt-2 flex items-center justify-center gap-1.5">
          <i data-lucide="square" class="w-4 h-4"></i> ${t('detail_close_recruitment')}
        </button>
      `;
    }
  }

  const requirementsHtml = job.description.split('\n').map(p => {
    if (p.startsWith('###')) {
      return `<h4 class="text-sm font-bold text-white uppercase tracking-wider mt-6 mb-3">${p.replace('###', '').trim()}</h4>`;
    }
    if (p.startsWith('-')) {
      return `<li class="ml-4 list-disc text-sm text-slate-300 mb-1.5">${p.replace('-', '').trim()}</li>`;
    }
    if (p.trim() === '') return '';
    return `<p class="text-sm text-slate-300 leading-relaxed mb-4">${p}</p>`;
  }).join('');

  detailContainer.innerHTML = `
    <!-- Left details column -->
    <div class="lg:col-span-8 space-y-6">
      <div class="glass-card rounded-3xl p-8 shadow-glass border border-slate-800/60">
        
        <div class="flex items-start gap-4 pb-6 border-b border-slate-800/60 mb-6">
          ${job.logo && (job.logo.startsWith('data:image/') || job.logo.startsWith('http'))
            ? `<img src="${job.logo}" class="w-14 h-14 rounded-2xl object-cover shrink-0 border border-slate-700/60 bg-slate-900/30 shadow-md">`
            : `<div class="w-14 h-14 rounded-2xl flex items-center justify-center font-extrabold text-lg shrink-0 ${job.logoBg}">${job.logoInitials || job.company.charAt(0).toUpperCase()}</div>`
          }
          <div>
            <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">${job.title}</h2>
            <p class="text-sm text-cyan-400 font-bold mt-1">${job.company}</p>
            <div class="flex flex-wrap gap-2.5 mt-3">
              <span class="rounded-lg bg-slate-900 border border-slate-800/80 px-2.5 py-1 text-xs text-slate-300 font-semibold">${job.type}</span>
              <span class="rounded-lg bg-slate-900 border border-slate-800/80 px-2.5 py-1 text-xs text-emerald-400 font-bold">${job.salary}</span>
              <span class="rounded-lg bg-slate-900 border border-slate-800/80 px-2.5 py-1 text-xs text-slate-400 font-medium">${job.location}</span>
              ${statusLabel}
            </div>
          </div>
        </div>

        <!-- Custom parsed descriptions -->
        <div class="prose prose-invert max-w-none">
          ${requirementsHtml}
        </div>

      </div>
    </div>

    <!-- Right sidebar card -->
    <div class="lg:col-span-4 space-y-6">
      <div class="glass-card rounded-3xl p-6 shadow-md border border-slate-800/60 space-y-5">
        <h3 class="text-xs font-bold tracking-wider text-slate-400 uppercase">${t('detail_sidebar_title')}</h3>
        
        <div class="space-y-3.5 text-xs text-slate-300">
          <div class="flex justify-between pb-2.5 border-b border-slate-800/40">
            <span class="text-slate-500">${t('detail_label_location')}</span>
            <span class="font-semibold text-right">${job.location}</span>
          </div>
          <div class="flex justify-between pb-2.5 border-b border-slate-800/40">
            <span class="text-slate-500">${t('detail_label_salary')}</span>
            <span class="font-semibold text-emerald-400">${job.salary}</span>
          </div>
          <div class="flex justify-between pb-2.5 border-b border-slate-800/40">
            <span class="text-slate-500">${t('detail_label_experience')}</span>
            <span class="font-semibold text-right">${t('detail_experience_value')}</span>
          </div>
          <div class="flex justify-between pb-2.5 border-b border-slate-800/40">
            <span class="text-slate-500">${t('detail_label_stack')}</span>
            <span class="font-semibold text-right text-cyan-400">${job.tags.join(', ')}</span>
          </div>
          ${job.gpa ? `
          <div class="flex justify-between pb-2.5 border-b border-slate-800/40">
            <span class="text-slate-500">${t('detail_label_gpa')}</span>
            <span class="font-semibold text-right text-cyan-400">${job.gpa}</span>
          </div>
          ` : ''}
          ${job.languages ? `
          <div class="flex justify-between pb-2.5 border-b border-slate-800/40">
            <span class="text-slate-500">${t('detail_label_languages')}</span>
            <span class="font-semibold text-right text-cyan-400">${job.languages}</span>
          </div>
          ` : ''}
          ${job.other_reqs ? `
          <div class="flex justify-between pb-2.5 border-b border-slate-800/40 font-sans">
            <span class="text-slate-500 shrink-0 pr-2">${t('detail_label_other')}</span>
            <span class="font-semibold text-right text-slate-300 max-w-[60%] break-words">${job.other_reqs}</span>
          </div>
          ` : ''}
        </div>

        ${isOwner ? `
          <button onclick="exportJobApplicantsCSV(${job.id})" class="w-full rounded-xl py-3 border border-cyan-500/30 bg-cyan-500/5 hover:bg-cyan-500/10 text-cyan-400 hover:text-cyan-300 text-xs font-bold transition-all duration-300 flex items-center justify-center gap-1.5 mb-2">
            <i data-lucide="download" class="w-4 h-4"></i> ${t('detail_export_csv')}
          </button>
          <button onclick="openJobModal(${job.id})" class="w-full rounded-xl py-3 border border-cyan-500/30 bg-cyan-500/5 hover:bg-cyan-500/10 text-cyan-400 hover:text-cyan-300 text-xs font-bold transition-all duration-300 flex items-center justify-center gap-1.5">
            <i data-lucide="edit-3" class="w-4 h-4"></i> ${t('detail_edit_listing')}
          </button>
          ${toggleStatusBtn}
          <button onclick="handleDeleteJob(${job.id})" class="w-full rounded-xl py-3 border border-red-500/30 bg-red-500/5 hover:bg-red-500/10 text-red-400 hover:text-red-300 text-xs font-bold transition-all duration-300 mt-2 flex items-center justify-center gap-1.5">
            <i data-lucide="trash-2" class="w-4 h-4"></i> ${t('detail_delete_listing')}
          </button>
        ` : `
          <p class="text-xs text-slate-400 text-center py-2 bg-slate-900/50 rounded-xl border border-slate-800">
            ${t('detail_other_company_job')}
          </p>
        `}
      </div>
    </div>
  `;

  if (window.lucide) window.lucide.createIcons();
}

export async function toggleJobStatus(jobId, newStatus) {
  if (!STATE.user.isLoggedIn) return;
  
  try {
    const response = await fetch(`${BASE_URL}/jobs/${jobId}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        status: newStatus,
        email: STATE.user.email
      })
    });
    
    if (response.ok) {
      showToast(`Đã chuyển trạng thái tin tuyển dụng thành: ${newStatus === 'active' ? 'Đang nhận đơn' : 'Đóng nhận đơn'}`);
      await loadJobsFromBackend();
      renderJobDetail(jobId);
    } else {
      const err = await response.json();
      showToast(err.detail || "Không thể cập nhật trạng thái tin.", "error");
    }
  } catch (error) {
    console.error("Error toggling job status:", error);
    showToast("Lỗi kết nối khi cập nhật trạng thái tin.", "error");
  }
}

export async function handleDeleteJob(jobId) {
  if (!confirm(t('confirm_delete_job'))) return;
  
  try {
    const response = await fetch(`${BASE_URL}/jobs/${jobId}?email=${encodeURIComponent(STATE.user.email)}`, {
      method: 'DELETE'
    });
    
    if (response.ok) {
      const result = await response.json();
      if (result.success) {
        showToast("Job listing deleted successfully!");
        await loadJobsFromBackend();
        switchTab('jobs');
      } else {
        showToast(result.detail || "Failed to delete listing", "error");
      }
    } else {
      const err = await response.json().catch(() => ({}));
      showToast(err.detail || "Unauthorized or listing not found", "error");
    }
  } catch (e) {
    console.error(e);
    showToast("Connection Error: Unable to delete listing.", "error");
  }
}

export function openJobModal(jobId) {
  const job = STATE.jobs.find(j => j.id === jobId);
  if (!job) return;
  
  const idEl = document.getElementById('edit-job-id');
  const companyEl = document.getElementById('edit-job-company');
  const titleEl = document.getElementById('edit-job-title');
  const locationEl = document.getElementById('edit-job-location');
  const salaryEl = document.getElementById('edit-job-salary');
  const descEl = document.getElementById('edit-job-desc');
  
  const gpaEl = document.getElementById('edit-job-gpa');
  const languagesEl = document.getElementById('edit-job-languages');
  const otherReqsEl = document.getElementById('edit-job-other-reqs');
  const logoEl = document.getElementById('edit-comp-logo');

  if (idEl) idEl.value = job.id;
  if (companyEl) companyEl.value = job.company || "";
  if (titleEl) titleEl.value = job.title || "";
  if (locationEl) locationEl.value = job.location || "";
  if (salaryEl) salaryEl.value = job.salary || "";
  if (gpaEl) gpaEl.value = job.gpa || "";
  if (languagesEl) languagesEl.value = job.languages || "";
  if (otherReqsEl) otherReqsEl.value = job.other_reqs || "";
  if (logoEl) logoEl.value = job.logo || "";

  // Reset logo preview UI
  const previewImg = document.getElementById('edit-logo-preview');
  const iconEl = document.getElementById('edit-logo-icon');
  const uploadStatus = document.getElementById('edit-logo-upload-status');
  if (previewImg) {
    if (job.logo && (job.logo.startsWith('data:image/') || job.logo.startsWith('http'))) {
      previewImg.src = job.logo;
      previewImg.classList.remove('hidden');
      if (iconEl) iconEl.classList.add('hidden');
      if (uploadStatus) uploadStatus.innerHTML = `<span class="text-emerald-400">Logo hiện tại</span>`;
    } else {
      previewImg.src = "";
      previewImg.classList.add('hidden');
      if (iconEl) iconEl.classList.remove('hidden');
      if (uploadStatus) uploadStatus.innerText = "Drag and drop logo, or browse";
    }
  }
  
  let descriptionClean = job.description;
  const reqsIndex = descriptionClean.indexOf("\n\nYÊU CẦU TUYỂN DỤNG CHUẨN");
  if (reqsIndex > -1) {
    descriptionClean = descriptionClean.substring(0, reqsIndex);
  }
  const techIndex = descriptionClean.indexOf("\n\nKey Technologies:");
  if (techIndex > -1) {
    descriptionClean = descriptionClean.substring(0, techIndex);
  }
  if (descEl) descEl.value = descriptionClean;
  
  const modal = document.getElementById('job-edit-modal');
  if (modal) modal.classList.remove('hidden');
  if (window.lucide) window.lucide.createIcons();
}

export function closeJobModal() {
  const modal = document.getElementById('job-edit-modal');
  if (modal) modal.classList.add('hidden');
}

export async function handleJobEditSubmit(event) {
  event.preventDefault();
  const jobId = document.getElementById('edit-job-id').value;
  const company = document.getElementById('edit-job-company').value.trim();
  const title = document.getElementById('edit-job-title').value.trim();
  const location = document.getElementById('edit-job-location').value.trim();
  const salary = document.getElementById('edit-job-salary').value.trim();
  const desc = document.getElementById('edit-job-desc').value.trim();
  
  const gpa = document.getElementById('edit-job-gpa') ? document.getElementById('edit-job-gpa').value.trim() : "";
  const languages = document.getElementById('edit-job-languages') ? document.getElementById('edit-job-languages').value.trim() : "";
  const other_reqs = document.getElementById('edit-job-other-reqs') ? document.getElementById('edit-job-other-reqs').value.trim() : "";
  const logo = document.getElementById('edit-comp-logo') ? document.getElementById('edit-comp-logo').value : "";

  const job = STATE.jobs.find(j => j.id == jobId);
  let descriptionWithTags = desc + (job && job.tags.length > 0 ? "\n\nKey Technologies: " + job.tags.join(', ') : "");
  
  // Format and append requirements block
  let reqsText = "";
  if (gpa || languages || other_reqs) {
    reqsText += "\n\nYÊU CẦU TUYỂN DỤNG CHUẨN";
    if (gpa) reqsText += `\n- Điểm GPA tối thiểu: ${gpa}`;
    if (languages) reqsText += `\n- Yêu cầu ngoại ngữ: ${languages}`;
    if (other_reqs) reqsText += `\n- Yêu cầu khác: ${other_reqs}`;
  }
  descriptionWithTags += reqsText;

  try {
    const response = await fetch(`${BASE_URL}/jobs/${jobId}?email=${encodeURIComponent(STATE.user.email)}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title,
        company,
        salary,
        location,
        description: descriptionWithTags,
        logo,
        gpa,
        languages,
        other_reqs
      })
    });

    if (response.ok) {
      const result = await response.json();
      if (result.success) {
        showToast("Job listing updated successfully!");
        closeJobModal();
        await loadJobsFromBackend();
        
        if (STATE.activeTab === 'job-detail' && STATE.activeJobId == jobId) {
          renderJobDetail(Number(jobId));
        }
      }
    } else {
      const err = await response.json().catch(() => ({}));
      showToast(err.detail || "Failed to update job listing.", "error");
    }
  } catch (e) {
    console.error(e);
    showToast("Connection Error: Unable to save job details.", "error");
  }
}

export function changeEditJobLogo() {
  const fileInput = document.getElementById('edit-logo-input');
  if (fileInput) fileInput.click();
}

export function handleEditJobLogoFileChange(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  if (file.size > 2 * 1024 * 1024) {
    showToast("Kích thước ảnh không được vượt quá 2MB.", "error");
    return;
  }
  
  const reader = new FileReader();
  reader.onload = function(e) {
    const base64Data = e.target.result;
    
    // Set value to hidden input
    const compLogo = document.getElementById('edit-comp-logo');
    if (compLogo) compLogo.value = base64Data;
    
    // Update preview UI
    const previewImg = document.getElementById('edit-logo-preview');
    const iconEl = document.getElementById('edit-logo-icon');
    const statusText = document.getElementById('edit-logo-upload-status');
    
    if (previewImg) {
      previewImg.src = base64Data;
      previewImg.classList.remove('hidden');
    }
    if (iconEl) {
      iconEl.classList.add('hidden');
    }
    if (statusText) {
      statusText.innerHTML = `<span class="text-emerald-400">Chọn logo thành công!</span>`;
    }
  };
  reader.readAsDataURL(file);
}

// Bind to window for HTML inline access
window.renderJobDetail = renderJobDetail;
window.toggleJobStatus = toggleJobStatus;
window.handleDeleteJob = handleDeleteJob;
window.openJobModal = openJobModal;
window.closeJobModal = closeJobModal;
window.handleJobEditSubmit = handleJobEditSubmit;
window.changeEditJobLogo = changeEditJobLogo;
window.handleEditJobLogoFileChange = handleEditJobLogoFileChange;

export async function exportJobApplicantsCSV(jobId) {
  if (!STATE.user.isLoggedIn) return;
  
  try {
    showToast("Đang chuẩn bị xuất danh sách...", "info");
    const response = await fetch(`${BASE_URL}/recruiter/applications?email=${encodeURIComponent(STATE.user.email)}`);
    if (!response.ok) {
      throw new Error("Không thể tải danh sách ứng viên.");
    }
    
    const allApps = await response.json();
    const jobApps = allApps.filter(app => app.job_id == jobId);
    
    if (jobApps.length === 0) {
      showToast("Chưa có ứng viên nào ứng tuyển công việc này để xuất file.", "error");
      return;
    }
    
    const headers = ["Tên ứng viên", "Email", "Chuyên ngành", "Năm học", "Vị trí", "Ngày ứng tuyển", "Trạng thái"];
    const csvRows = [headers.join(",")];
    
    for (const app of jobApps) {
      const row = [
        `"${(app.student_name || '').replace(/"/g, '""')}"`,
        `"${(app.student_email || '').replace(/"/g, '""')}"`,
        `"${(app.student_major || '').replace(/"/g, '""')}"`,
        `"Năm ${app.student_year || 1}"`,
        `"${(app.job_title || '').replace(/"/g, '""')}"`,
        `"${(app.applied_at || '').replace(/"/g, '""')}"`,
        `"${(app.application_status || 'applied').replace(/"/g, '""')}"`
      ];
      csvRows.push(row.join(","));
    }
    
    const csvContent = "\uFEFF" + csvRows.join("\n");
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `danh_sach_ung_vien_job_${jobId}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast("Đã xuất danh sách ứng viên thành công!");
  } catch (error) {
    console.error("Error exporting CSV:", error);
    showToast("Lỗi khi xuất danh sách ứng viên.", "error");
  }
}
window.exportJobApplicantsCSV = exportJobApplicantsCSV;
