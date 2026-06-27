/**
 * AI-Career Bridge - Profile Module
 * Handles company profile editing, rendering, and active postings list.
 */

import { STATE, BASE_URL, showToast, syncAuthNav, t } from '../app.js';

export function renderProfile() {
  if (!STATE.user) return;
  
  const avatarImg = document.getElementById('profile-avatar');
  if (avatarImg) {
    avatarImg.src = STATE.user.avatar || "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=256&auto=format&fit=crop";
  }
  
  const nameEl = document.getElementById('profile-name');
  const titleEl = document.getElementById('profile-title');
  const bioEl = document.getElementById('profile-bio');
  const emailEl = document.getElementById('profile-email');
  const createdAtEl = document.getElementById('profile-created-at');
  
  let bioText = STATE.user.bio || "";
  let expText = "";
  let eduText = "";
  
  if (bioText.startsWith('{"') || bioText.startsWith('{')) {
    try {
      const parsed = JSON.parse(bioText);
      bioText = parsed.bio || "";
      expText = parsed.experience || "";
      eduText = parsed.education || "";
    } catch (e) {
      console.error("Failed to parse bio JSON", e);
    }
  }

  // Set default placeholders for Company if empty
  if (!bioText) {
    bioText = t('profile_bio_placeholder');
  }
  if (!expText) {
    expText = t('profile_exp_placeholder');
  }
  if (!eduText) {
    eduText = t('profile_edu_placeholder');
  }
  
  if (nameEl) nameEl.innerText = STATE.user.name || "";
  if (titleEl) titleEl.innerText = STATE.user.title || "";
  if (bioEl) bioEl.innerText = bioText || "";
  if (emailEl) emailEl.innerText = STATE.user.email || "";
  
  const expContainer = document.getElementById('profile-experience-container');
  if (expContainer) expContainer.innerHTML = renderExperienceHtml(expText);
  
  const eduContainer = document.getElementById('profile-education-container');
  if (eduContainer) eduContainer.innerHTML = renderEducationHtml(eduText);
  
  if (createdAtEl) {
    if (STATE.user.created_at) {
      try {
        const dateStr = STATE.user.created_at.replace(' ', 'T');
        const dateObj = new Date(dateStr);
        if (!isNaN(dateObj.getTime())) {
          createdAtEl.innerText = dateObj.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
          });
        } else {
          createdAtEl.innerText = STATE.user.created_at;
        }
      } catch (e) {
        createdAtEl.innerText = STATE.user.created_at;
      }
    } else {
      createdAtEl.innerText = "N/A";
    }
  }
  
  renderProfileSkills();
  renderMyPostedJobs();
}

export function renderProfileSkills() {
  const container = document.getElementById('profile-skills-container');
  if (!container) return;
  
  if (!STATE.user.skills || STATE.user.skills.length === 0) {
    container.innerHTML = `<p class="text-xs text-slate-500">${t('profile_no_skills')}</p>`;
    return;
  }
  
  container.innerHTML = STATE.user.skills.map(skill => `
    <span class="bg-slate-900 border border-slate-800 text-slate-300 text-xs font-semibold px-3 py-1 rounded-lg hover:border-cyan-500/25 duration-100">${skill}</span>
  `).join('');
}

export function renderMyPostedJobs() {
  const card = document.getElementById('my-posted-jobs-card');
  const container = document.getElementById('my-posted-jobs-list');
  if (!card || !container) return;

  if (!STATE.user.isLoggedIn || !STATE.user.email) {
    card.classList.add('hidden');
    return;
  }

  const myJobs = STATE.jobs.filter(j => j.posted_by === STATE.user.email);
  if (myJobs.length === 0) {
    card.classList.add('hidden');
    return;
  }

  card.classList.remove('hidden');
  container.innerHTML = myJobs.map(job => {
    const hasCustomLogo = job.logo && (job.logo.startsWith('data:image/') || job.logo.startsWith('http'));
    const logoHtml = hasCustomLogo
      ? `<img src="${job.logo}" class="w-9 h-9 rounded-xl object-cover shrink-0 border border-slate-700/60 bg-slate-900/30 shadow-sm">`
      : `<div class="w-9 h-9 rounded-xl flex items-center justify-center font-bold text-xs select-none shrink-0 ${job.logoBg}">${job.logoInitials}</div>`;

    return `
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3.5 rounded-2xl bg-brand-background/45 border border-slate-800/60 hover:border-cyan-500/20 transition-all duration-200">
        <div class="flex items-center gap-3">
          ${logoHtml}
          <div>
            <h4 class="text-xs font-bold text-white">${job.title}</h4>
            <p class="text-[10px] text-slate-400">${job.company} ✦ ${job.location} ✦ <span class="text-emerald-400 font-bold">${job.salary}</span></p>
          </div>
        </div>
        <div class="flex items-center justify-end gap-2 w-full sm:w-auto border-t sm:border-t-0 pt-2 sm:pt-0 border-slate-800/40">
          <button onclick="openJobModal(${job.id})" class="text-cyan-400 hover:text-cyan-300 p-1" title="Edit Listing">
            <i data-lucide="edit-3" class="w-3.5 h-3.5"></i>
          </button>
          <button onclick="handleDeleteJob(${job.id})" class="text-red-400 hover:text-red-300 p-1" title="Delete Listing">
            <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
          </button>
          <button onclick="switchTab('job-detail', { id: ${job.id} })" class="text-slate-400 hover:text-white p-1" title="View details">
            <i data-lucide="chevron-right" class="w-4 h-4"></i>
          </button>
        </div>
      </div>
    `;
  }).join('');

  if (window.lucide) window.lucide.createIcons();
}

export function openProfileModal() {
  let bioText = STATE.user.bio || "";
  let expText = "";
  let eduText = "";
  
  if (bioText.startsWith('{"') || bioText.startsWith('{')) {
    try {
      const parsed = JSON.parse(bioText);
      bioText = parsed.bio || "";
      expText = parsed.experience || "";
      eduText = parsed.education || "";
    } catch (e) {}
  }
  
  if (!bioText) {
    bioText = t('profile_bio_placeholder');
  }
  if (!expText) {
    expText = t('profile_exp_placeholder');
  }
  if (!eduText) {
    eduText = t('profile_edu_placeholder');
  }

  document.getElementById('edit-name').value = STATE.user.name || "";
  document.getElementById('edit-title').value = STATE.user.title || "";
  document.getElementById('edit-bio').value = bioText;
  document.getElementById('edit-experience').value = expText;
  document.getElementById('edit-education').value = eduText;
  document.getElementById('edit-skills').value = STATE.user.skills ? STATE.user.skills.join(', ') : "";
  
  const modal = document.getElementById('profile-edit-modal');
  if (modal) modal.classList.remove('hidden');
  if (window.lucide) window.lucide.createIcons();
}

export function closeProfileModal() {
  const modal = document.getElementById('profile-edit-modal');
  if (modal) modal.classList.add('hidden');
}

export async function handleProfileEditSubmit(event) {
  event.preventDefault();
  const name = document.getElementById('edit-name').value.trim();
  const title = document.getElementById('edit-title').value.trim();
  const bio = document.getElementById('edit-bio').value.trim();
  const experience = document.getElementById('edit-experience').value.trim();
  const education = document.getElementById('edit-education').value.trim();
  const skills = document.getElementById('edit-skills').value.trim();

  const bioJson = JSON.stringify({
    bio: bio,
    experience: experience,
    education: education,
    avatar: STATE.user.avatar
  });

  try {
    const response = await fetch(`${BASE_URL}/update-profile`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: STATE.user.email,
        name: name,
        title: title,
        bio: bioJson,
        skills: skills
      })
    });

    if (response.ok) {
      const result = await response.json();
      if (result.success) {
        STATE.user.name = result.user.name;
        STATE.user.title = result.user.title;
        STATE.user.bio = result.user.bio;
        STATE.user.skills = result.user.skills ? result.user.skills.split(',').map(s => s.trim()).filter(Boolean) : [];
        
        localStorage.setItem('user', JSON.stringify(STATE.user));
        renderProfile();
        syncAuthNav();
        closeProfileModal();
        showToast("Profile details updated successfully.");
      }
    } else {
      showToast("Failed to update profile details", "error");
    }
  } catch (e) {
    console.error(e);
    showToast("Connection Error: Unable to save details.", "error");
  }
}

export function changeProfilePhoto() {
  const fileInput = document.getElementById('profile-avatar-input');
  if (fileInput) fileInput.click();
}

export async function handleAvatarFileChange(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  if (file.size > 2 * 1024 * 1024) {
    showToast("Kích thước ảnh không được vượt quá 2MB.", "error");
    return;
  }
  
  const reader = new FileReader();
  reader.onload = async function(e) {
    const base64Data = e.target.result;
    
    // Update local state
    STATE.user.avatar = base64Data;
    localStorage.setItem('user', JSON.stringify(STATE.user));
    
    // Update UI immediately
    const avatarImg = document.getElementById('profile-avatar');
    if (avatarImg) avatarImg.src = base64Data;
    syncAuthNav();
    
    // Read current bio fields to update
    let bioText = STATE.user.bio || "";
    let expText = "";
    let eduText = "";
    
    if (bioText.startsWith('{"') || bioText.startsWith('{')) {
      try {
        const parsed = JSON.parse(bioText);
        bioText = parsed.bio || "";
        expText = parsed.experience || "";
        eduText = parsed.education || "";
      } catch (err) {}
    }
    
    const bioJson = JSON.stringify({
      bio: bioText,
      experience: expText,
      education: eduText,
      avatar: base64Data
    });
    
    try {
      const response = await fetch(`${BASE_URL}/update-profile`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: STATE.user.email,
          name: STATE.user.name,
          title: STATE.user.title,
          bio: bioJson,
          skills: STATE.user.skills ? STATE.user.skills.join(', ') : ""
        })
      });
      
      if (response.ok) {
        const result = await response.json();
        if (result.success) {
          STATE.user.bio = result.user.bio;
          localStorage.setItem('user', JSON.stringify(STATE.user));
          showToast("Cập nhật ảnh đại diện thành công!");
        }
      } else {
        showToast("Lỗi khi lưu ảnh đại diện lên server.", "error");
      }
    } catch (err) {
      console.error("Error updating avatar:", err);
      showToast("Lỗi kết nối khi cập nhật ảnh đại diện.", "error");
    }
  };
  reader.readAsDataURL(file);
}

function renderExperienceHtml(expText) {
  if (!expText) return "";
  const lines = expText.split('\n').filter(Boolean);
  return lines.map((line, idx) => {
    const dotColor = idx === 0 ? "bg-cyan-400" : "bg-slate-700";
    return `
      <div class="relative pl-6 border-l border-slate-800 dark:border-slate-700/50">
        <div class="absolute -left-1.5 top-1.5 w-3 h-3 rounded-full ${dotColor}"></div>
        <p class="text-sm font-semibold text-slate-200 leading-normal">${line}</p>
      </div>
    `;
  }).join('');
}

function renderEducationHtml(eduText) {
  if (!eduText) return "";
  const lines = eduText.split('\n').filter(Boolean);
  return lines.map(line => {
    let cleanLine = line;
    let icon = "globe";
    if (line.toLowerCase().includes("email:") || line.toLowerCase().includes("@")) {
      icon = "mail";
    } else if (line.toLowerCase().includes("website:") || line.toLowerCase().includes("http")) {
      icon = "globe";
    }
    return `
      <div class="relative pl-6 border-l border-slate-800 dark:border-slate-700/50">
        <div class="absolute -left-1.5 top-1.5 w-3 h-3 rounded-full bg-cyan-400/50"></div>
        <p class="text-sm font-semibold text-slate-200 leading-normal flex items-center gap-2">
          <i data-lucide="${icon}" class="w-3.5 h-3.5 text-slate-500"></i> ${cleanLine}
        </p>
      </div>
    `;
  }).join('');
}

// Bind to window for HTML inline access
window.openProfileModal = openProfileModal;
window.closeProfileModal = closeProfileModal;
window.handleProfileEditSubmit = handleProfileEditSubmit;
window.changeProfilePhoto = changeProfilePhoto;
window.handleAvatarFileChange = handleAvatarFileChange;
window.renderProfile = renderProfile;
