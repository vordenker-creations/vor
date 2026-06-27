/**
 * AI-Career Bridge - Job Board Module
 * Handles loading, rendering, searching, filtering, and sorting jobs.
 */

import { STATE, BASE_URL, showToast, switchTab, t } from '../app.js';

export async function loadJobsFromBackend() {
  try {
    const response = await fetch(`${BASE_URL}/jobs`);
    if (response.ok) {
      const dbJobs = await response.json();
      
      const techKeywords = ["React", "Next.js", "TypeScript", "Rust", "Node.js", "GraphQL", "TailwindCSS", "Framer Motion", "Kubernetes", "AWS", "Terraform", "Go", "Postgres", "Deno", "Figma Design", "WASM"];
      const colors = [
        "bg-black text-white border border-slate-700/60",
        "bg-indigo-600 text-white",
        "bg-rose-500 text-white",
        "bg-emerald-950 text-emerald-400 border border-emerald-800/40",
        "bg-slate-900 text-slate-100 border border-slate-700/60",
        "bg-amber-950/80 text-amber-300 border border-amber-800/40"
      ];

      STATE.jobs = dbJobs.map(job => {
        const logoInitials = job.company.charAt(0).toUpperCase();
        let hash = 0;
        for (let i = 0; i < job.company.length; i++) {
          hash = job.company.charCodeAt(i) + ((hash << 5) - hash);
        }
        const logoBg = colors[Math.abs(hash) % colors.length];

        let tags = [];
        const searchPool = (job.title + " " + job.description).toLowerCase();
        techKeywords.forEach(keyword => {
          if (searchPool.includes(keyword.toLowerCase())) {
            tags.push(keyword);
          }
        });
        if (tags.length === 0) tags = ["Tech", "Engineering"];

        let type = "Full-Time";
        if (searchPool.includes("contract")) type = "Contract";
        else if (searchPool.includes("part-time")) type = "Part-Time";

        let postedTime = t('job_posted_justnow');
        if (job.created_at) {
          postedTime = t('job_posted_recently');
        }

        return {
          id: job.id,
          title: job.title,
          company: job.company,
          logo: job.logo || "",
          logoInitials: logoInitials,
          logoBg: logoBg,
          location: job.location,
          salary: job.salary,
          type: type,
          tags: tags,
          postedTime: postedTime,
          description: job.description,
          posted_by: job.posted_by || "system",
          status: job.status || "active",
          gpa: job.gpa || "",
          languages: job.languages || "",
          other_reqs: job.other_reqs || ""
        };
      });

      renderJobs();
    }
  } catch (error) {
    console.error("Failed to load jobs from backend:", error);
  }
}

export let activeTechFilters = [];

export function toggleQuickTech(tech) {
  const idx = activeTechFilters.indexOf(tech);
  if (idx > -1) {
    activeTechFilters.splice(idx, 1);
  } else {
    activeTechFilters.push(tech);
  }
  
  // Update UI active styling on pills
  const pills = document.querySelectorAll('.tag-pill');
  pills.forEach(pill => {
    if (pill.innerText === tech) {
      pill.classList.toggle('border-cyan-500/40');
      pill.classList.toggle('bg-cyan-950/45');
      pill.classList.toggle('text-cyan-400');
    }
  });

  renderJobs();
}

export function triggerSearch() {
  const keyword = document.getElementById('search-keyword').value.trim();
  STATE.currentSearch.keyword = keyword.toLowerCase();
  STATE.currentSearch.location = document.getElementById('search-location').value.toLowerCase().trim();
  if (keyword) {
    saveSearchHistory(keyword);
  }
  renderJobs();
}

export function clearFilters() {
  activeTechFilters = [];
  const keywordEl = document.getElementById('search-keyword');
  const locEl = document.getElementById('search-location');
  if (keywordEl) keywordEl.value = "";
  if (locEl) locEl.value = "";
  STATE.currentSearch.keyword = "";
  STATE.currentSearch.location = "";
  
  const ftCheckbox = document.getElementById('filter-fulltime');
  const ctCheckbox = document.getElementById('filter-contract');
  const rmCheckbox = document.getElementById('filter-remote');
  if (ftCheckbox) ftCheckbox.checked = true;
  if (ctCheckbox) ctCheckbox.checked = true;
  if (rmCheckbox) rmCheckbox.checked = false;
  
  const salarySlider = document.getElementById('filter-salary');
  if (salarySlider) salarySlider.value = 50000;
  STATE.minSalary = 50000;
  const salaryVal = document.getElementById('salary-min-val');
  if (salaryVal) salaryVal.innerText = "Any";
  
  // Remove visual highlights
  const pills = document.querySelectorAll('.tag-pill');
  pills.forEach(pill => {
    pill.className = "tag-pill text-xs font-medium px-2.5 py-1 rounded-lg border border-slate-800 bg-brand-background/40 text-slate-300 hover:border-cyan-500/40 hover:text-cyan-400 duration-150";
  });

  renderJobs();
  showToast("Filters reset successfully.");
}

export function resetFiltersWithoutToast() {
  activeTechFilters = [];
  const keywordEl = document.getElementById('search-keyword');
  const locEl = document.getElementById('search-location');
  if (keywordEl) keywordEl.value = "";
  if (locEl) locEl.value = "";
  STATE.currentSearch.keyword = "";
  STATE.currentSearch.location = "";
  
  const ftCheckbox = document.getElementById('filter-fulltime');
  const ctCheckbox = document.getElementById('filter-contract');
  const rmCheckbox = document.getElementById('filter-remote');
  
  if (ftCheckbox) ftCheckbox.checked = true;
  if (ctCheckbox) ctCheckbox.checked = true;
  if (rmCheckbox) rmCheckbox.checked = false;
  
  const salarySlider = document.getElementById('filter-salary');
  if (salarySlider) salarySlider.value = 50000;
  STATE.minSalary = 50000;
  const salaryVal = document.getElementById('salary-min-val');
  if (salaryVal) salaryVal.innerText = "Any";
  
  const pills = document.querySelectorAll('.tag-pill');
  pills.forEach(pill => {
    pill.className = "tag-pill text-xs font-medium px-2.5 py-1 rounded-lg border border-slate-800 bg-brand-background/40 text-slate-300 hover:border-cyan-500/40 hover:text-cyan-400 duration-150";
  });
}

export function handleSalarySliderInput(val) {
  STATE.minSalary = parseInt(val) || 50000;
  const displayVal = document.getElementById('salary-min-val');
  if (displayVal) {
    if (STATE.minSalary === 50000) {
      displayVal.innerText = "Any";
    } else {
      displayVal.innerText = `$${Math.round(STATE.minSalary / 1000)}k`;
    }
  }
  renderJobs();
}

export function parseMinSalary(salaryStr) {
  if (!salaryStr) return 0;
  const clean = salaryStr.toLowerCase().replace(/[$,\s]/g, '');
  const match = clean.match(/^(\d+)(k)?/);
  if (match) {
    let val = parseInt(match[1]);
    if (match[2] === 'k') {
      val = val * 1000;
    } else if (val < 1000) {
      val = val * 12; // convert monthly to annual approximately
    }
    return val;
  }
  return 0;
}

export function loadRecentSearches() {
  const container = document.getElementById('recent-searches-container');
  const list = document.getElementById('recent-searches-list');
  if (!container || !list) return;

  const history = JSON.parse(localStorage.getItem('recentSearches') || '[]');
  if (history.length === 0) {
    container.classList.add('hidden');
    return;
  }

  container.classList.remove('hidden');
  list.innerHTML = history.map(term => `
    <button onclick="applyRecentSearch('${term}')" class="px-2 py-0.5 rounded-md bg-slate-900/65 dark:bg-slate-800/40 text-slate-300 hover:text-cyan-400 border border-slate-800 dark:border-slate-700/50 hover:border-cyan-500/35 duration-100 transition-colors font-medium">
      ${term}
    </button>
  `).join('');
}

export function saveSearchHistory(term) {
  if (!term) return;
  let history = JSON.parse(localStorage.getItem('recentSearches') || '[]');
  history = history.filter(t => t !== term);
  history.unshift(term);
  if (history.length > 3) history.pop();
  localStorage.setItem('recentSearches', JSON.stringify(history));
  loadRecentSearches();
}

export function applyRecentSearch(term) {
  const input = document.getElementById('search-keyword');
  if (input) input.value = term;
  STATE.currentSearch.keyword = term.toLowerCase().trim();
  renderJobs();
}

export function renderJobs() {
  const container = document.getElementById('jobs-grid-container');
  if (!container) return;
  const sortSelect = document.getElementById('sort-select');
  const sortVal = sortSelect ? sortSelect.value : 'recent';
  
  // Filter State Checkboxes
  const ftCheckbox = document.getElementById('filter-fulltime');
  const ctCheckbox = document.getElementById('filter-contract');
  const rmCheckbox = document.getElementById('filter-remote');
  const fullTimeChecked = ftCheckbox ? ftCheckbox.checked : true;
  const contractChecked = ctCheckbox ? ctCheckbox.checked : true;
  const remoteChecked = rmCheckbox ? rmCheckbox.checked : false;

  // Filter logic
  let filtered = STATE.jobs.filter(job => {
    // Keyword Search match
    if (STATE.currentSearch.keyword) {
      const matchTitle = job.title.toLowerCase().includes(STATE.currentSearch.keyword);
      const matchCompany = job.company.toLowerCase().includes(STATE.currentSearch.keyword);
      const matchTags = job.tags.some(tag => tag.toLowerCase().includes(STATE.currentSearch.keyword));
      if (!matchTitle && !matchCompany && !matchTags) return false;
    }

    // Location Search match
    if (STATE.currentSearch.location) {
      const matchLoc = job.location.toLowerCase().includes(STATE.currentSearch.location);
      if (!matchLoc) return false;
    }

    // Job Type Checkboxes
    if (job.type === 'Full-Time' && !fullTimeChecked) return false;
    if (job.type === 'Contract' && !contractChecked) return false;
    
    // Remote check
    if (remoteChecked && !job.location.toLowerCase().includes('remote')) return false;

    // Tech tag filters
    if (activeTechFilters.length > 0) {
      const matchAllTech = activeTechFilters.every(tech => job.tags.includes(tech));
      if (!matchAllTech) return false;
    }

    // Salary Range match
    if (STATE.minSalary && STATE.minSalary > 50000) {
      const jobMinSalary = parseMinSalary(job.salary);
      if (jobMinSalary && jobMinSalary < STATE.minSalary) return false;
    }

    return true;
  });

  // Sort logic
  if (sortVal === 'salary') {
    filtered.sort((a, b) => {
      const valA = parseInt(a.salary.replace(/[^0-9]/g, '')) || 0;
      const valB = parseInt(b.salary.replace(/[^0-9]/g, '')) || 0;
      return valB - valA;
    });
  } else {
    filtered.sort((a, b) => b.id - a.id);
  }

  // Update badge
  const countBadge = document.getElementById('job-count-badge');
  if (countBadge) {
    countBadge.innerText = `${filtered.length} ${filtered.length === 1 ? 'job' : 'jobs'}`;
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="col-span-full py-12 flex flex-col items-center justify-center text-slate-500">
        <i data-lucide="inbox" class="w-10 h-10 text-slate-600 mb-2"></i>
        <p class="text-sm font-semibold">No listing results match your filters.</p>
        <button onclick="clearFilters()" class="text-xs text-cyan-400 mt-2 font-bold hover:underline">Reset Search</button>
      </div>
    `;
    if (window.lucide) window.lucide.createIcons();
    return;
  }

  // Render Cards
  container.innerHTML = filtered.map(job => {
    const skillsString = job.tags.map(t => `<span class="bg-slate-900/65 text-slate-300 text-[10px] font-semibold px-2.5 py-1 rounded-md border border-slate-800/80">${t}</span>`).join('');
    
    // Feature 3: Job Status badge
    const statusBadge = job.status === 'closed' ? `
      <span class="inline-flex items-center gap-1 rounded-full bg-red-500/10 px-2 py-0.5 text-[9px] font-bold text-red-400 border border-red-500/20 mr-1.5">
        Đã đóng nhận đơn
      </span>
    ` : `
      <span class="inline-flex items-center gap-1 rounded-full bg-cyan-500/10 px-2 py-0.5 text-[9px] font-bold text-cyan-400 border border-cyan-500/20 mr-1.5">
        Đang nhận đơn
      </span>
    `;

    return `
      <article class="glass-card rounded-3xl p-6 shadow-md border border-slate-800/60 flex flex-col justify-between transition-all duration-300 hover:-translate-y-1.5 hover:shadow-glow-cyan hover:border-cyan-500/30 group">
        <div>
          
          <!-- Card Header -->
          <div class="flex items-start justify-between gap-4 mb-4">
            <div class="flex items-center gap-3">
              ${job.logo && (job.logo.startsWith('data:image/') || job.logo.startsWith('http')) 
                ? `<img src="${job.logo}" class="w-11 h-11 rounded-xl object-cover shrink-0 border border-slate-700/60 bg-slate-900/30 shadow-sm">`
                : `<div class="w-11 h-11 rounded-xl flex items-center justify-center font-bold text-sm select-none shrink-0 ${job.logoBg}">${job.logoInitials}</div>`
              }
              <div>
                <h3 class="text-base font-bold text-white group-hover:text-cyan-400 duration-200 transition-colors">${job.title}</h3>
                <p class="text-xs text-slate-400">${job.company} ✦ <span class="text-[10px] uppercase font-semibold text-slate-500 tracking-wide">${job.type}</span></p>
              </div>
            </div>
            <div class="flex flex-col items-end gap-1.5">
              <span class="text-[10px] text-slate-500 font-medium">${job.postedTime}</span>
              ${job.status === 'closed' ? `
                <span class="inline-flex items-center gap-1 rounded-full bg-red-500/10 px-2 py-0.5 text-[9px] font-bold text-red-400 border border-red-500/20 mr-1.5">
                  ${t('job_status_closed')}
                </span>
              ` : `
                <span class="inline-flex items-center gap-1 rounded-full bg-cyan-500/10 px-2 py-0.5 text-[9px] font-bold text-cyan-400 border border-cyan-500/20 mr-1.5">
                  ${t('job_status_active')}
                </span>
              `}
            </div>
          </div>
          
          <!-- Meta Row -->
          <div class="flex flex-wrap gap-y-1 gap-x-3.5 mb-5 text-xs text-slate-300">
            <span class="flex items-center gap-1.5 font-medium"><i data-lucide="map-pin" class="w-3.5 h-3.5 text-slate-500"></i> ${job.location}</span>
            <span class="flex items-center gap-1.5 font-bold text-emerald-400"><i data-lucide="dollar-sign" class="w-3.5 h-3.5 text-slate-500"></i> ${job.salary}</span>
          </div>
 
          <!-- Tags list -->
          <div class="flex flex-wrap gap-1.5">
            ${skillsString}
          </div>
 
        </div>
 
        <!-- View Action button -->
        <div class="mt-6 pt-4 border-t border-slate-800/40 flex justify-between items-center">
          <div class="flex items-center gap-2">
            ${STATE.user.isLoggedIn && job.posted_by === STATE.user.email ? `
              <button onclick="openJobModal(${job.id})" class="text-cyan-400 hover:text-cyan-300 text-xs font-bold flex items-center gap-1.5 transition-colors duration-200">
                <i data-lucide="edit-3" class="w-3.5 h-3.5"></i> ${t('detail_edit_listing')}
              </button>
              <span class="text-slate-700">|</span>
              <button onclick="handleDeleteJob(${job.id})" class="text-red-400 hover:text-red-300 text-xs font-bold flex items-center gap-1.5 transition-colors duration-200">
                <i data-lucide="trash-2" class="w-3.5 h-3.5"></i> ${t('detail_delete_listing')}
              </button>
            ` : '<div></div>'}
          </div>
          <button onclick="switchTab('job-detail', { id: ${job.id} })" class="rounded-xl border border-slate-800/80 bg-slate-900/10 hover:bg-cyan-500/5 hover:border-cyan-500/20 text-slate-300 hover:text-cyan-400 text-xs font-bold px-4 py-2 transition-all duration-200">
            ${t('btn_view_details')}
          </button>
        </div>
      </article>
    `;
  }).join('');
 
  if (window.lucide) window.lucide.createIcons();
}

// Bind to window for HTML inline access
window.toggleQuickTech = toggleQuickTech;
window.triggerSearch = triggerSearch;
window.clearFilters = clearFilters;
window.handleSalarySliderInput = handleSalarySliderInput;
window.applyRecentSearch = applyRecentSearch;
window.renderJobs = renderJobs;
window.loadJobsFromBackend = loadJobsFromBackend;
window.loadRecentSearches = loadRecentSearches;
