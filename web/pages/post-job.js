/**
 * AI-Career Bridge - Post Job Module
 * Handles creating new job listings, managing tech tags, and logo uploads.
 */

import { STATE, BASE_URL, showToast, switchTab, setFieldError, clearAllErrors } from '../app.js';
import { loadJobsFromBackend, resetFiltersWithoutToast } from './jobs.js';

export let formTags = ["React", "Next.js"];

export function handleTagInput(event) {
  if (event.key === 'Enter') {
    event.preventDefault();
    const input = document.getElementById('post-tag-input');
    const tag = input.value.trim();
    
    if (tag && !formTags.includes(tag)) {
      formTags.push(tag);
      renderFormTags();
      input.value = "";
    }
  }
}

export function removeFormTag(idx) {
  formTags.splice(idx, 1);
  renderFormTags();
}

export function renderFormTags() {
  const container = document.getElementById('tags-pills');
  if (!container) return;
  container.innerHTML = formTags.map((tag, idx) => `
    <span class="inline-flex items-center gap-1 bg-cyan-950/60 text-cyan-400 text-xs font-semibold px-2 py-0.5 rounded-lg border border-cyan-500/20">
      ${tag}
      <button type="button" onclick="removeFormTag(${idx})" class="hover:text-red-400"><i data-lucide="x" class="w-3 h-3"></i></button>
    </span>
  `).join('');
  
  // Update hidden input
  const hiddenTags = document.getElementById('post-job-tags-hidden');
  if (hiddenTags) hiddenTags.value = formTags.join(',');
  if (window.lucide) window.lucide.createIcons();
}

export function changeJobLogo() {
  const fileInput = document.getElementById('post-logo-input');
  if (fileInput) fileInput.click();
}

export function handleJobLogoFileChange(event) {
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
    const compLogo = document.getElementById('post-comp-logo');
    if (compLogo) compLogo.value = base64Data;
    
    // Update preview UI
    const previewImg = document.getElementById('post-logo-preview');
    const iconEl = document.getElementById('post-logo-icon');
    const statusText = document.getElementById('logo-upload-status');
    
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

export async function handlePostJobSubmit(event) {
  event.preventDefault();
  clearAllErrors();

  const API_URL = `${BASE_URL}/post-job`;
  
  // Extract form variables
  const company = document.getElementById('post-comp-name').value.trim();
  const title = document.getElementById('post-job-title').value.trim();
  const type = document.getElementById('post-job-type').value;
  const location = document.getElementById('post-job-location').value.trim();
  const salary = document.getElementById('post-job-salary').value.trim();
  const desc = document.getElementById('post-job-desc').value.trim();
  
  // Extract new requirements and logo
  const gpa = document.getElementById('post-job-gpa').value.trim();
  const languages = document.getElementById('post-job-languages').value.trim();
  const other_reqs = document.getElementById('post-job-other-reqs').value.trim();
  const logo = document.getElementById('post-comp-logo').value;

  // 1. Frontend validation check
  let isValid = true;
  
  if (!company) {
    setFieldError('post-comp-name', 'companyError', 'Company Name is required');
    isValid = false;
  } else if (company.length < 2) {
    setFieldError('post-comp-name', 'companyError', 'Company Name must be at least 2 characters');
    isValid = false;
  }

  if (!title) {
    setFieldError('post-job-title', 'titleError', 'Job Title is required');
    isValid = false;
  } else if (title.length < 3) {
    setFieldError('post-job-title', 'titleError', 'Job Title must be at least 3 characters');
    isValid = false;
  }

  if (!location) {
    setFieldError('post-job-location', 'locationError', 'Location is required');
    isValid = false;
  } else if (location.length < 2) {
    setFieldError('post-job-location', 'locationError', 'Location must be at least 2 characters');
    isValid = false;
  }

  // Validate Salary Range: Must not be empty and must contain at least one digit
  const salaryRegex = /[0-9]/;
  if (!salary) {
    setFieldError('post-job-salary', 'salaryError', 'Salary representation is required');
    isValid = false;
  } else if (!salaryRegex.test(salary)) {
    setFieldError('post-job-salary', 'salaryError', 'Salary must contain at least one digit (e.g., $100k or $50/hr)');
    isValid = false;
  }

  if (!desc) {
    setFieldError('post-job-desc', 'descriptionError', 'Description is required');
    isValid = false;
  } else if (desc.length < 10) {
    setFieldError('post-job-desc', 'descriptionError', 'Description must be at least 10 characters');
    isValid = false;
  }

  if (!isValid) {
    showToast("Validation Error: Please check the highlighted fields.", "error");
    return;
  }

  // 2. Set UI loading state
  const submitBtn = document.getElementById('submitBtn');
  if (!submitBtn) return;
  const btnText = submitBtn.querySelector('.btn-text');
  const btnSpinner = submitBtn.querySelector('.btn-spinner');

  submitBtn.disabled = true;
  if (btnText) btnText.textContent = 'Publishing...';
  if (btnSpinner) btnSpinner.classList.remove('hidden');

  // Setup AbortController for network timeout (8 seconds)
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 8000);

  let descriptionWithTags = desc + (formTags.length > 0 ? "\n\nKey Technologies: " + formTags.join(', ') : "");
  
  // Format and append requirements block for PyQt6 desktop app support
  let reqsText = "";
  if (gpa || languages || other_reqs) {
    reqsText += "\n\nYÊU CẦU TUYỂN DỤNG CHUẨN";
    if (gpa) reqsText += `\n- Điểm GPA tối thiểu: ${gpa}`;
    if (languages) reqsText += `\n- Yêu cầu ngoại ngữ: ${languages}`;
    if (other_reqs) reqsText += `\n- Yêu cầu khác: ${other_reqs}`;
  }
  descriptionWithTags += reqsText;

  const payload = {
    title: title,
    company: company,
    salary: salary,
    location: location,
    description: descriptionWithTags,
    posted_by: STATE.user.email,
    logo: logo || "",
    gpa: gpa || "",
    languages: languages || "",
    other_reqs: other_reqs || ""
  };

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (response.ok) {
      const result = await response.json();
      if (result.success) {
        showToast(`Listing for "${title}" published successfully!`);
        
        // Reset form variables
        document.getElementById('post-job-form').reset();
        formTags.length = 0;
        formTags.push("React", "Next.js");
        renderFormTags();
        
        // Reset logo upload preview UI
        const previewImg = document.getElementById('post-logo-preview');
        const iconEl = document.getElementById('post-logo-icon');
        const uploadStatus = document.getElementById('logo-upload-status');
        if (previewImg) {
          previewImg.src = "";
          previewImg.classList.add('hidden');
        }
        if (iconEl) {
          iconEl.classList.remove('hidden');
        }
        if (uploadStatus) {
          uploadStatus.innerText = "Drag and drop logo, or browse";
        }

        // Reset filters so the new job is guaranteed to be visible
        resetFiltersWithoutToast();

        // Refresh jobs from database and switch tab
        await loadJobsFromBackend();
        switchTab('jobs');
      } else {
        showToast(result.message || 'Server rejected the posting.', 'error');
      }
    } else if (response.status === 422) {
      // Pydantic validation errors map back to UI
      const errorData = await response.json();
      if (errorData && Array.isArray(errorData.detail)) {
        errorData.detail.forEach(err => {
          const fieldName = err.loc[err.loc.length - 1];
          let msg = err.msg;

          // Clean Pydantic technical prefix
          if (msg.startsWith('Value error, ')) {
            msg = msg.replace('Value error, ', '');
          }

          if (fieldName === 'title') setFieldError('post-job-title', 'titleError', msg);
          else if (fieldName === 'company') setFieldError('post-comp-name', 'companyError', msg);
          else if (fieldName === 'salary') setFieldError('post-job-salary', 'salaryError', msg);
          else if (fieldName === 'location') setFieldError('post-job-location', 'locationError', msg);
          else if (fieldName === 'description') setFieldError('post-job-desc', 'descriptionError', msg);
        });
        showToast("Validation Error: Check highlighted fields.", "error");
      } else {
        showToast("Unprocessable data submitted.", "error");
      }
    } else {
      const errorData = await response.json().catch(() => ({}));
      const serverMsg = errorData.detail || 'An unexpected server error occurred.';
      showToast(serverMsg, 'error');
    }
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === 'AbortError') {
      showToast("Request Timeout: The server took too long to respond. Please try again.", "error");
    } else {
      console.error('Fetch error:', error);
      showToast("Connection Error: Make sure the FastAPI backend is running.", "error");
    }
  } finally {
    // Reset UI loading state
    submitBtn.disabled = false;
    if (btnText) btnText.textContent = 'Publish Listing';
    if (btnSpinner) btnSpinner.classList.add('hidden');
  }
}

// Bind to window for HTML inline access
window.handleTagInput = handleTagInput;
window.removeFormTag = removeFormTag;
window.renderFormTags = renderFormTags;
window.changeJobLogo = changeJobLogo;
window.handleJobLogoFileChange = handleJobLogoFileChange;
window.handlePostJobSubmit = handlePostJobSubmit;
