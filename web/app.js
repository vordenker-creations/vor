/**
 * AI-Career Bridge - Premium Recruiter Web Controller
 * Handles client-side state, tab routing, search filters, profile editing,
 * inline validation display, loading indicator, and FastAPI integration.
 */

// Initialize theme on script load to prevent light mode flash
const initTheme = () => {
  const currentTheme = localStorage.getItem('theme') || 'dark';
  if (currentTheme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
};
initTheme();

// Dynamic API & WebSocket host configuration
const getBackendHost = () => {
  const rawHost = window.location.host;
  if (!rawHost || rawHost.includes('file://') || rawHost.includes('localhost:5500') || rawHost.includes('127.0.0.1:5500')) {
    return '127.0.0.1:8000';
  }
  if (rawHost.includes(':5500')) {
    return rawHost.replace(':5500', ':8000');
  }
  return rawHost;
};

const BACKEND_HOST = getBackendHost();
const BASE_URL = `${window.location.protocol === 'file:' ? 'http:' : window.location.protocol}//${BACKEND_HOST}`;

function syncThemeIcon() {
  const iconEl = document.getElementById('theme-toggle-icon');
  if (!iconEl) return;
  const isDark = document.documentElement.classList.contains('dark');
  if (isDark) {
    iconEl.setAttribute('data-lucide', 'sun');
  } else {
    iconEl.setAttribute('data-lucide', 'moon');
  }
  lucide.createIcons();
}

function toggleTheme() {
  const isDark = document.documentElement.classList.contains('dark');
  if (isDark) {
    document.documentElement.classList.remove('dark');
    localStorage.setItem('theme', 'light');
  } else {
    document.documentElement.classList.add('dark');
    localStorage.setItem('theme', 'dark');
  }
  syncThemeIcon();
  showToast(`Switched to ${isDark ? 'Light' : 'Dark'} mode.`);
}

// Salary filter slider change handler
function handleSalarySliderInput(val) {
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

// Helper to parse min salary from strings (like "$160k - $210k" or "$1,200 - $2,000")
function parseMinSalary(salaryStr) {
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

// Recent Searches logic
function loadRecentSearches() {
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

function saveSearchHistory(term) {
  if (!term) return;
  let history = JSON.parse(localStorage.getItem('recentSearches') || '[]');
  history = history.filter(t => t !== term);
  history.unshift(term);
  if (history.length > 3) history.pop();
  localStorage.setItem('recentSearches', JSON.stringify(history));
  loadRecentSearches();
}

function applyRecentSearch(term) {
  const input = document.getElementById('search-keyword');
  if (input) input.value = term;
  STATE.currentSearch.keyword = term.toLowerCase().trim();
  renderJobs();
}

// Load session from localStorage if exists to prevent logout on reload
const savedUser = localStorage.getItem('user');
const initialUser = savedUser ? JSON.parse(savedUser) : {
  isLoggedIn: false,
  name: "",
  title: "",
  email: "",
  avatar: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?q=80&w=256&auto=format&fit=crop",
  skills: [],
  bio: "",
  appliedJobIds: [],
  created_at: ""
};

const STATE = {
  user: initialUser,
  jobs: [
    {
      id: 1,
      title: "Staff Frontend Architect",
      company: "Vercel",
      logo: "V",
      logoBg: "bg-black text-white",
      location: "San Francisco, CA (Remote)",
      salary: "$160k - $210k",
      type: "Full-Time",
      tags: ["Next.js", "React", "TypeScript", "TailwindCSS"],
      postedTime: "2 hours ago",
      description: "We are looking for an exceptional Staff Frontend Architect to lead the future of web deployment UI. You will work on optimizing rendering paths, improving component design models, and shaping next-generation SaaS features.\n\n### Requirements:\n- 7+ years of building web applications\n- Expertise in React internals and Next.js routers\n- Passion for micro-interactions and performance optimization\n- Strong experience writing clean CSS animations"
    },
    {
      id: 2,
      title: "Rust Systems Engineer",
      company: "Anthropic",
      logo: "A",
      logoBg: "bg-amber-950/80 text-amber-300 border border-amber-800/40",
      location: "San Francisco, CA (Onsite)",
      salary: "$180k - $240k",
      type: "Full-Time",
      tags: ["Rust", "WASM", "Distributed Systems", "AI"],
      postedTime: "4 hours ago",
      description: "Anthropic is looking for a Rust systems engineer to lead core latency reduction teams. You will work directly at the interface of CUDA pipelines, compiler tooling, and web clients to ensure fast, real-time responses.\n\n### Key Tasks:\n- Build low-latency interfaces in native Rust\n- Integrate WebAssembly backends into the browser UI\n- Optimize memory models and core algorithms"
    },
    {
      id: 3,
      title: "DevOps & Cloud Engineer",
      company: "Stripe",
      logo: "S",
      logoBg: "bg-indigo-600 text-white",
      location: "Dublin, Ireland (Remote)",
      salary: "$140k - $175k",
      type: "Full-Time",
      tags: ["Kubernetes", "AWS", "Terraform", "Go"],
      postedTime: "1 day ago",
      description: "Join Stripe's Core Infrastructure team to engineer resilient cloud pipelines. This role handles large scaling configurations, automated validation loops, and ensures absolute site reliability for millions of transactions.\n\n### Your Profile:\n- Strong knowledge of AWS cloud services and Terraform configurations\n- Competence in writing production shell files and Go scripts\n- Deep commitment to cloud security best practices"
    },
    {
      id: 4,
      title: "Product Engineer",
      company: "Linear",
      logo: "L",
      logoBg: "bg-slate-900 text-slate-100 border border-slate-700/60",
      location: "Remote (Global)",
      salary: "$130k - $160k",
      type: "Contract",
      tags: ["React", "TypeScript", "GraphQL", "Electron"],
      postedTime: "2 days ago",
      description: "We are seeking a senior designer/engineer hybrid to craft smooth project management flows. Linear's interface is celebrated for its low latency, high utility, and beautiful typography. You will build core client interactions.\n\n### Specifications:\n- Outstanding mastery of React, CSS variables, and layout systems\n- Deep visual styling eye: spacing, font scale, micro-interactions\n- Ability to work autonomously in global teams"
    },
    {
      id: 5,
      title: "Systems Engineer (Node/TS)",
      company: "Supabase",
      logo: "B",
      logoBg: "bg-emerald-950 text-emerald-400 border border-emerald-800/40",
      location: "Singapore (Hybrid)",
      salary: "$110k - $145k",
      type: "Full-Time",
      tags: ["Node.js", "Postgres", "TypeScript", "Deno"],
      postedTime: "3 days ago",
      description: "Supabase seeks systems devs to work on PostgreSQL client libraries and serverless functions infrastructure. Help open source developers launch products in minutes with reliable server templates and instant API backends."
    },
    {
      id: 6,
      title: "Interactive UI/UX Designer",
      company: "Figma",
      logo: "F",
      logoBg: "bg-rose-500 text-white",
      location: "New York, NY (Hybrid)",
      salary: "$150k - $185k",
      type: "Full-Time",
      tags: ["Figma Design", "React", "CSS Animation", "WASM"],
      postedTime: "5 days ago",
      description: "Help build the canvas of the web. Figma is recruiting creative engineers to push the boundaries of multiplayer design systems. Experience in web canvas, matrix operations, and rich gesture animations is strongly preferred."
    }
  ],
  currentSearch: {
    keyword: "",
    location: ""
  },
  minSalary: 50000,
  activeTab: "jobs",
  activeJobId: null
};

// ==================== APP BOOTSTRAP ====================
window.addEventListener('DOMContentLoaded', async () => {
  syncAuthNav();
  await loadJobsFromBackend();
  await syncUserApplications();
  await loadNotificationsFromBackend();
  renderProfile();
  syncThemeIcon();
  loadRecentSearches();
  initWebSocket();
  const salaryVal = document.getElementById('salary-min-val');
  if (salaryVal) salaryVal.innerText = "Any";
  lucide.createIcons();

  // Setup filter checkboxes change listeners for real-time reactivity
  const ftCheckbox = document.getElementById('filter-fulltime');
  const ctCheckbox = document.getElementById('filter-contract');
  const rmCheckbox = document.getElementById('filter-remote');
  if (ftCheckbox) ftCheckbox.addEventListener('change', renderJobs);
  if (ctCheckbox) ctCheckbox.addEventListener('change', renderJobs);
  if (rmCheckbox) rmCheckbox.addEventListener('change', renderJobs);

  const salarySlider = document.getElementById('filter-salary');
  if (salarySlider) salarySlider.addEventListener('input', renderJobs);

  // Setup input key listeners to clear warnings dynamically
  setupWarningClearers();
});

// ==================== ROUTING SYSTEM (Tab switcher) ====================
function switchTab(tabName, additionalParams = {}) {
  // Authorization check
  if ((tabName === 'profile' || tabName === 'post-job') && !STATE.user.isLoggedIn) {
    showToast("Please sign in to access this page.", "error");
    switchTab('login');
    return;
  }

  STATE.activeTab = tabName;
  
  // Update UI active views
  const views = ['jobs', 'job-detail', 'login', 'register', 'post-job', 'profile', 'chat'];
  views.forEach(v => {
    const el = document.getElementById(`view-${v}`);
    if (el) {
      if (v === tabName) {
        el.classList.remove('hidden');
        el.classList.add('block');
      } else {
        el.classList.remove('block');
        el.classList.add('hidden');
      }
    }
  });

  // Update Nav Link Highlights
  const navLinks = ['jobs', 'post-job', 'profile', 'chat'];
  navLinks.forEach(link => {
    const el = document.getElementById(`nav-${link}`);
    if (el) {
      if (link === tabName) {
        el.classList.add('text-cyan-400');
        el.classList.remove('text-slate-300');
      } else {
        el.classList.remove('text-cyan-400');
        el.classList.add('text-slate-300');
      }
    }
  });

  // Handle specific tab entries
  if (tabName === 'job-detail') {
    const jobId = additionalParams.id;
    STATE.activeJobId = jobId;
    renderJobDetail(jobId);
  }
  
  // Render/update items
  if (tabName === 'profile') {
    renderProfile();
  }

  // Scroll to top
  window.scrollTo({ top: 0, behavior: 'smooth' });
  
  // Re-create icons dynamically
  setTimeout(() => { lucide.createIcons(); }, 30);
}

// Toggle Mobile Burger Navigation Drawer
function toggleMobileMenu() {
  const menu = document.getElementById('mobile-menu');
  menu.classList.toggle('hidden');
}

// ==================== TOAST NOTIFICATION HELPERS ====================
function showToast(message, type = 'success', applicant = null) {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  
  // Setup styling based on type
  let typeStyle = 'border-cyan-500/30 bg-slate-950/90 text-slate-100';
  let icon = 'info';
  if (type === 'success') {
    typeStyle = 'border-emerald-500/30 bg-emerald-950/80 text-emerald-300';
    icon = 'check-circle-2';
  } else if (type === 'error') {
    typeStyle = 'border-red-500/30 bg-red-950/80 text-red-300';
    icon = 'alert-triangle';
  }

  let clickClass = '';
  if (applicant) {
    clickClass = ' cursor-pointer hover:border-cyan-400/50 hover:shadow-glow-cyan/30 transition-all duration-300';
    toast.onclick = () => {
      showApplicantDetails(applicant);
    };
  }

  toast.className = `glass-card border px-4 py-3 rounded-xl flex items-center gap-2.5 shadow-lg transform transition-all duration-300 translate-y-2 opacity-0 pointer-events-auto ${typeStyle}${clickClass}`;
  toast.innerHTML = `
    <i data-lucide="${icon}" class="w-4 h-4 shrink-0"></i>
    <p class="text-xs font-semibold">${message}</p>
  `;
  
  container.appendChild(toast);
  lucide.createIcons();

  // Trigger animation
  setTimeout(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
  }, 50);

  // Auto dismiss after 12 seconds
  setTimeout(() => {
    toast.classList.add('translate-y-[-10px]', 'opacity-0');
    setTimeout(() => {
      toast.remove();
    }, 300);
  }, 12000);
}

// ==================== FIELD VALIDATION HELPERS ====================
function setFieldError(inputId, errorId, message) {
  const inputEl = document.getElementById(inputId);
  const errorEl = document.getElementById(errorId);
  if (inputEl) inputEl.classList.add('input-error');
  if (errorEl) errorEl.textContent = message;
}

function clearFieldError(inputId, errorId) {
  const inputEl = document.getElementById(inputId);
  const errorEl = document.getElementById(errorId);
  if (inputEl) inputEl.classList.remove('input-error');
  if (errorEl) errorEl.textContent = '';
}

function clearAllErrors() {
  clearFieldError('post-comp-name', 'companyError');
  clearFieldError('post-job-title', 'titleError');
  clearFieldError('post-job-location', 'locationError');
  clearFieldError('post-job-salary', 'salaryError');
  clearFieldError('post-job-desc', 'descriptionError');
}

function setupWarningClearers() {
  const fields = [
    { id: 'post-comp-name', errId: 'companyError' },
    { id: 'post-job-title', errId: 'titleError' },
    { id: 'post-job-location', errId: 'locationError' },
    { id: 'post-job-salary', errId: 'salaryError' },
    { id: 'post-job-desc', errId: 'descriptionError' }
  ];

  fields.forEach(field => {
    const el = document.getElementById(field.id);
    if (el) {
      el.addEventListener('input', () => clearFieldError(field.id, field.errId));
    }
  });
}

// ==================== AUTHENTICATION ACTIONS ====================
function syncAuthNav() {
  const guestNav = document.getElementById('auth-nav-guest');
  const userNav = document.getElementById('auth-nav-user');
  
  if (STATE.user.isLoggedIn) {
    guestNav.classList.add('hidden');
    userNav.classList.remove('hidden');
    
    // Populate User Info
    document.getElementById('navbar-username').innerText = STATE.user.name;
    document.getElementById('navbar-avatar').src = STATE.user.avatar;
  } else {
    guestNav.classList.remove('hidden');
    userNav.classList.add('hidden');
  }
}

async function handleLoginSubmit(event) {
  event.preventDefault();
  const email = document.getElementById('login-email').value.trim();
  const pass = document.getElementById('login-password').value;

  try {
    const response = await fetch(`${BASE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password: pass })
    });

    if (response.ok) {
      const result = await response.json();
      if (result.success) {
        STATE.user.isLoggedIn = true;
        STATE.user.name = result.user.name;
        STATE.user.title = result.user.title;
        STATE.user.email = result.user.email;
        STATE.user.bio = result.user.bio || "";
        STATE.user.skills = result.user.skills ? result.user.skills.split(',').map(s => s.trim()).filter(Boolean) : [];
        STATE.user.created_at = result.user.created_at || "";
        STATE.user.avatar = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=256&auto=format&fit=crop";

        localStorage.setItem('user', JSON.stringify(STATE.user));
        await syncUserApplications();
        renderProfile();
        syncAuthNav();
        renderJobs();
        showToast(`Welcome back, ${STATE.user.name}!`);
        switchTab('jobs');
        document.getElementById('login-form').reset();
      }
    } else {
      const err = await response.json();
      showToast(err.detail || "Invalid credentials", "error");
    }
  } catch (e) {
    console.error(e);
    showToast("Connection Error: Unable to authenticate.", "error");
  }
}

async function handleRegisterSubmit(event) {
  event.preventDefault();
  const name = document.getElementById('reg-name').value.trim();
  const title = document.getElementById('reg-title').value.trim();
  const email = document.getElementById('reg-email').value.trim();
  const pass = document.getElementById('reg-pass').value;
  const confirm = document.getElementById('reg-confirm').value;

  if (pass !== confirm) {
    showToast("Validation Error: Passwords do not match.", "error");
    return;
  }

  try {
    const response = await fetch(`${BASE_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, title, email, password: pass })
    });

    if (response.ok) {
      const result = await response.json();
      if (result.success) {
        STATE.user.isLoggedIn = true;
        STATE.user.name = result.user.name;
        STATE.user.title = result.user.title;
        STATE.user.email = result.user.email;
        STATE.user.bio = result.user.bio || "";
        STATE.user.skills = result.user.skills ? result.user.skills.split(',').map(s => s.trim()).filter(Boolean) : [];
        STATE.user.created_at = result.user.created_at || "";
        STATE.user.avatar = "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=256&auto=format&fit=crop";

        localStorage.setItem('user', JSON.stringify(STATE.user));
        await syncUserApplications();
        renderProfile();
        syncAuthNav();
        renderJobs();
        showToast(`Welcome to AI-Career bridge, ${name}! Your account has been set up.`);
        switchTab('jobs');
        document.getElementById('register-form').reset();
      }
    } else {
      const err = await response.json();
      showToast(err.detail || "Registration failed", "error");
    }
  } catch (e) {
    console.error(e);
    showToast("Connection Error: Unable to register.", "error");
  }
}

function validatePasswords() {
  const pass = document.getElementById('reg-pass').value;
  const confirm = document.getElementById('reg-confirm').value;
  const errorText = document.getElementById('password-match-error');

  if (confirm && pass !== confirm) {
    errorText.classList.remove('hidden');
  } else {
    errorText.classList.add('hidden');
  }
}

function logout() {
  STATE.user = {
    isLoggedIn: false,
    name: "",
    title: "",
    email: "",
    avatar: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?q=80&w=256&auto=format&fit=crop",
    skills: [],
    bio: "",
    appliedJobIds: [],
    created_at: ""
  };
  localStorage.removeItem('user');
  syncAuthNav();
  renderJobs();
  showToast("Signed out successfully.");
  switchTab('jobs');
}

// ==================== SEARCH & FILTERS ====================
let activeTechFilters = [];

function toggleQuickTech(tech) {
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

function triggerSearch() {
  const keyword = document.getElementById('search-keyword').value.trim();
  STATE.currentSearch.keyword = keyword.toLowerCase();
  STATE.currentSearch.location = document.getElementById('search-location').value.toLowerCase().trim();
  if (keyword) {
    saveSearchHistory(keyword);
  }
  renderJobs();
}

function clearFilters() {
  activeTechFilters = [];
  document.getElementById('search-keyword').value = "";
  document.getElementById('search-location').value = "";
  STATE.currentSearch.keyword = "";
  STATE.currentSearch.location = "";
  document.getElementById('filter-fulltime').checked = true;
  document.getElementById('filter-contract').checked = false;
  document.getElementById('filter-remote').checked = false;
  
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

function resetFiltersWithoutToast() {
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

// ==================== RENDER LISTINGS ====================
function renderJobs() {
  const container = document.getElementById('jobs-grid-container');
  if (!container) return;
  const sortVal = document.getElementById('sort-select').value;
  
  // Filter State Checkboxes
  const fullTimeChecked = document.getElementById('filter-fulltime').checked;
  const contractChecked = document.getElementById('filter-contract').checked;
  const remoteChecked = document.getElementById('filter-remote').checked;

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
  document.getElementById('job-count-badge').innerText = `${filtered.length} ${filtered.length === 1 ? 'job' : 'jobs'}`;

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="col-span-full py-12 flex flex-col items-center justify-center text-slate-500">
        <i data-lucide="inbox" class="w-10 h-10 text-slate-600 mb-2"></i>
        <p class="text-sm font-semibold">No listing results match your filters.</p>
        <button onclick="clearFilters()" class="text-xs text-cyan-400 mt-2 font-bold hover:underline">Reset Search</button>
      </div>
    `;
    lucide.createIcons();
    return;
  }

  // Render Cards
  container.innerHTML = filtered.map(job => {
    const skillsString = job.tags.map(t => `<span class="bg-slate-900/65 text-slate-300 text-[10px] font-semibold px-2.5 py-1 rounded-md border border-slate-800/80">${t}</span>`).join('');
    const isApplied = STATE.user.isLoggedIn && STATE.user.appliedJobIds.includes(job.id);
    const appliedBadge = isApplied ? `
      <span class="inline-flex items-center gap-1 rounded-full bg-emerald-500/10 px-2 py-0.5 text-[9px] font-bold text-emerald-400 border border-emerald-500/20 mr-1.5 animate-pulse">
        <span class="h-1 w-1 rounded-full bg-emerald-400"></span> Applied
      </span>
    ` : '';

    return `
      <article class="glass-card rounded-3xl p-6 shadow-md border border-slate-800/60 flex flex-col justify-between transition-all duration-300 hover:-translate-y-1.5 hover:shadow-glow-cyan hover:border-cyan-500/30 group">
        <div>
          
          <!-- Card Header -->
          <div class="flex items-start justify-between gap-4 mb-4">
            <div class="flex items-center gap-3">
              <div class="w-11 h-11 rounded-xl flex items-center justify-center font-bold text-sm select-none shrink-0 ${job.logoBg}">
                ${job.logo}
              </div>
              <div>
                <h3 class="text-base font-bold text-white group-hover:text-cyan-400 duration-200 transition-colors">${job.title}</h3>
                <p class="text-xs text-slate-400">${job.company} ✦ <span class="text-[10px] uppercase font-semibold text-slate-500 tracking-wide">${job.type}</span></p>
              </div>
            </div>
            <div class="flex flex-col items-end gap-1.5">
              <span class="text-[10px] text-slate-500 font-medium">${job.postedTime}</span>
              ${appliedBadge}
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
                <i data-lucide="edit-3" class="w-3.5 h-3.5"></i> Edit
              </button>
              <span class="text-slate-700">|</span>
              <button onclick="handleDeleteJob(${job.id})" class="text-red-400 hover:text-red-300 text-xs font-bold flex items-center gap-1.5 transition-colors duration-200">
                <i data-lucide="trash-2" class="w-3.5 h-3.5"></i> Delete
              </button>
            ` : '<div></div>'}
          </div>
          <button onclick="switchTab('job-detail', { id: ${job.id} })" class="rounded-xl border border-slate-800/80 bg-slate-900/10 hover:bg-cyan-500/5 hover:border-cyan-500/20 text-slate-300 hover:text-cyan-400 text-xs font-bold px-4 py-2 transition-all duration-200">
            View Details
          </button>
        </div>
      </article>
    `;
  }).join('');

  lucide.createIcons();
}

// ==================== DETAILED JOB PAGE RENDERER ====================
function renderJobDetail(jobId) {
  const detailContainer = document.getElementById('job-detail-content');
  if (!detailContainer) return;
  
  const job = STATE.jobs.find(j => j.id === jobId);
  if (!job) {
    detailContainer.innerHTML = `<p class="text-center text-slate-500 col-span-full">Job not found.</p>`;
    return;
  }

  // Check if user already applied or is owner
  const isOwner = STATE.user.isLoggedIn && job.posted_by === STATE.user.email;
  const alreadyApplied = STATE.user.appliedJobIds.includes(jobId);
  
  let applyBtnText = "Apply to Job";
  let applyBtnClass = "bg-gradient-to-r from-cyan-400 to-blue-500 hover:from-cyan-300 hover:to-blue-400 text-slate-950 shadow-glow-cyan hover:shadow-glow-cyan-hover transform hover:scale-[1.01]";
  let applyBtnDisabled = false;
  
  if (isOwner) {
    applyBtnText = "Your Listing";
    applyBtnClass = "bg-slate-800 border border-slate-700/60 text-slate-400 cursor-not-allowed";
    applyBtnDisabled = true;
  } else if (alreadyApplied) {
    applyBtnText = "Applied Successful";
    applyBtnClass = "bg-slate-800 border border-slate-700/60 text-slate-400 cursor-not-allowed";
    applyBtnDisabled = true;
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
          <div class="w-14 h-14 rounded-2xl flex items-center justify-center font-extrabold text-lg shrink-0 ${job.logoBg}">
            ${job.logo}
          </div>
          <div>
            <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">${job.title}</h2>
            <p class="text-sm text-cyan-400 font-bold mt-1">${job.company}</p>
            <div class="flex flex-wrap gap-2.5 mt-3">
              <span class="rounded-lg bg-slate-900 border border-slate-800/80 px-2.5 py-1 text-xs text-slate-300 font-semibold">${job.type}</span>
              <span class="rounded-lg bg-slate-900 border border-slate-800/80 px-2.5 py-1 text-xs text-emerald-400 font-bold">${job.salary}</span>
              <span class="rounded-lg bg-slate-900 border border-slate-800/80 px-2.5 py-1 text-xs text-slate-400 font-medium">${job.location}</span>
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
        <h3 class="text-xs font-bold tracking-wider text-slate-400 uppercase">Employment Details</h3>
        
        <div class="space-y-3.5 text-xs text-slate-300">
          <div class="flex justify-between pb-2.5 border-b border-slate-800/40">
            <span class="text-slate-500">Location Status</span>
            <span class="font-semibold text-right">${job.location}</span>
          </div>
          <div class="flex justify-between pb-2.5 border-b border-slate-800/40">
            <span class="text-slate-500">Base Salary Range</span>
            <span class="font-semibold text-emerald-400">${job.salary}</span>
          </div>
          <div class="flex justify-between pb-2.5 border-b border-slate-800/40">
            <span class="text-slate-500">Experience Needed</span>
            <span class="font-semibold text-right">Senior Level (5+ yrs)</span>
          </div>
          <div class="flex justify-between pb-2.5 border-b border-slate-800/40">
            <span class="text-slate-500">Required Stack</span>
            <span class="font-semibold text-right text-cyan-400">${job.tags.join(', ')}</span>
          </div>
        </div>

        <button onclick="applyToActiveJob(${job.id})" id="apply-btn-element" ${applyBtnDisabled ? "disabled" : ""} class="w-full rounded-xl py-3 text-xs font-bold transition-all duration-300 ${applyBtnClass}">
          ${applyBtnText}
        </button>
        
        ${STATE.user.isLoggedIn && job.posted_by === STATE.user.email ? `
          <button onclick="openJobModal(${job.id})" class="w-full rounded-xl py-3 border border-cyan-500/30 bg-cyan-500/5 hover:bg-cyan-500/10 text-cyan-400 hover:text-cyan-300 text-xs font-bold transition-all duration-300 mt-2 flex items-center justify-center gap-1.5">
            <i data-lucide="edit-3" class="w-4 h-4"></i> Edit Listing
          </button>
          <button onclick="handleDeleteJob(${job.id})" class="w-full rounded-xl py-3 border border-red-500/30 bg-red-500/5 hover:bg-red-500/10 text-red-400 hover:text-red-300 text-xs font-bold transition-all duration-300 mt-2 flex items-center justify-center gap-1.5">
            <i data-lucide="trash-2" class="w-4 h-4"></i> Delete Listing
          </button>
        ` : ''}
        
        <p class="text-[10px] text-center text-slate-500">Applying shares your profile resume info with ${job.company}.</p>
      </div>
    </div>
  `;

  lucide.createIcons();
}

async function applyToActiveJob(jobId) {
  if (!STATE.user.isLoggedIn) {
    showToast("Please sign in to apply for job opportunities.", "error");
    switchTab('login');
    return;
  }

  const btn = document.getElementById('apply-btn-element');
  if (btn) {
    btn.innerText = "Applying...";
    btn.disabled = true;
  }

  try {
    const response = await fetch(`${BASE_URL}/apply`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: STATE.user.email,
        job_id: jobId
      })
    });
    
    if (response.ok) {
      if (!STATE.user.appliedJobIds.includes(jobId)) {
        STATE.user.appliedJobIds.push(jobId);
      }
      localStorage.setItem('user', JSON.stringify(STATE.user));
      showToast("Application submitted successfully!");
      renderJobDetail(jobId);
    } else {
      showToast("Failed to submit job application.", "error");
      if (btn) {
        btn.innerText = "Apply to Job";
        btn.disabled = false;
      }
    }
  } catch (error) {
    console.error("Error applying to job:", error);
    showToast("Connection Error: Unable to submit application.", "error");
    if (btn) {
      btn.innerText = "Apply to Job";
      btn.disabled = false;
    }
  }
}

async function handleDeleteJob(jobId) {
  if (!confirm("Are you sure you want to delete this job listing?")) return;
  
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

// ==================== TAGS LOGIC ====================
let formTags = ["React", "Next.js"];

function handleTagInput(event) {
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

function removeFormTag(idx) {
  formTags.splice(idx, 1);
  renderFormTags();
}

function renderFormTags() {
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
  lucide.createIcons();
}

// Trigger tags render initially
setTimeout(() => { renderFormTags(); }, 100);

function simulateLogoUpload() {
  const status = document.getElementById('logo-upload-status');
  const progress = document.getElementById('upload-progress-bar');
  const fill = document.getElementById('upload-progress-fill');

  status.innerText = "Uploading company logo...";
  progress.classList.remove('hidden');
  fill.style.width = "0%";

  let percent = 0;
  const interval = setInterval(() => {
    percent += 25;
    fill.style.width = `${percent}%`;
    
    if (percent >= 100) {
      clearInterval(interval);
      status.innerHTML = `<span class="text-emerald-400 flex items-center gap-1"><i data-lucide="check" class="w-4 h-4"></i> Logo uploaded successfully!</span>`;
      document.getElementById('post-comp-logo').value = "UPLOADED";
      lucide.createIcons();
    }
  }, 200);
}

// ==================== ASYNC POST JOB INTEGRATION ====================
async function handlePostJobSubmit(event) {
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
  const btnText = submitBtn.querySelector('.btn-text');
  const btnSpinner = submitBtn.querySelector('.btn-spinner');

  submitBtn.disabled = true;
  if (btnText) btnText.textContent = 'Publishing...';
  if (btnSpinner) btnSpinner.classList.remove('hidden');

  // Setup AbortController for network timeout (8 seconds)
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 8000);

  const descriptionWithTags = desc + (formTags.length > 0 ? "\n\nKey Technologies: " + formTags.join(', ') : "");

  const payload = {
    title: title,
    company: company,
    salary: salary,
    location: location,
    description: descriptionWithTags,
    posted_by: STATE.user.email
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
        formTags = ["React", "Next.js"];
        renderFormTags();
        const uploadProgress = document.getElementById('upload-progress-bar');
        if (uploadProgress) uploadProgress.classList.add('hidden');
        const uploadStatus = document.getElementById('logo-upload-status');
        if (uploadStatus) uploadStatus.innerText = "Drag and drop logo, or browse";

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

// ==================== PROFILE LOGIC ====================
function renderProfile() {
  if (!STATE.user) return;
  
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

  // Set default placeholders if empty
  if (!expText) {
    expText = "Staff Frontend Architect\nVercel ✦ 2022 - Present\nLead development of core responsive layout components and modern dashboard dashboards.\n\nSenior React Engineer\nLinear ✦ 2020 - 2022\nRefactored workspace lists for premium loading animations and low latency page states.";
  }
  if (!eduText) {
    eduText = "B.S. in Computer Science\nStanford University ✦ Class of 2017";
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
  renderAppliedJobs();
  renderMyPostedJobs();
}

function renderProfileSkills() {
  const container = document.getElementById('profile-skills-container');
  if (!container) return;
  container.innerHTML = STATE.user.skills.map(skill => `
    <span class="bg-slate-900 border border-slate-800 text-slate-300 text-xs font-semibold px-3 py-1 rounded-lg hover:border-cyan-500/25 duration-100">${skill}</span>
  `).join('');
}

function renderAppliedJobs() {
  const container = document.getElementById('applied-jobs-list');
  if (!container) return;
  
  if (STATE.user.appliedJobIds.length === 0) {
    container.innerHTML = `<p class="text-xs text-slate-500">You haven't applied to any roles yet.</p>`;
    return;
  }

  const appliedList = STATE.jobs.filter(j => STATE.user.appliedJobIds.includes(j.id));
  
  container.innerHTML = appliedList.map(job => `
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3.5 rounded-2xl bg-brand-background/45 border border-slate-800/60 hover:border-cyan-500/20 transition-all duration-200">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl flex items-center justify-center font-bold text-xs select-none shrink-0 ${job.logoBg}">
          ${job.logo}
        </div>
        <div>
          <h4 class="text-xs font-bold text-white">${job.title}</h4>
          <p class="text-[10px] text-slate-400">${job.company} ✦ ${job.location}</p>
        </div>
      </div>
      <div class="flex items-center justify-between sm:justify-end gap-2 w-full sm:w-auto border-t sm:border-t-0 pt-2 sm:pt-0 border-slate-800/40">
        <span class="inline-flex items-center gap-1 rounded-full bg-emerald-500/10 px-2 py-0.5 text-[10px] font-bold text-emerald-400 border border-emerald-500/20">
          <span class="h-1.5 w-1.5 rounded-full bg-emerald-400"></span> Applied
        </span>
        <button onclick="switchTab('job-detail', { id: ${job.id} })" class="text-slate-400 hover:text-white p-1" title="View details">
          <i data-lucide="chevron-right" class="w-4 h-4"></i>
        </button>
      </div>
    </div>
  `).join('');
  
  lucide.createIcons();
}

function openProfileModal() {
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
  
  if (!expText) {
    expText = "Staff Frontend Architect\nVercel ✦ 2022 - Present\nLead development of core responsive layout components and modern dashboard dashboards.\n\nSenior React Engineer\nLinear ✦ 2020 - 2022\nRefactored workspace lists for premium loading animations and low latency page states.";
  }
  if (!eduText) {
    eduText = "B.S. in Computer Science\nStanford University ✦ Class of 2017";
  }

  document.getElementById('edit-name').value = STATE.user.name || "";
  document.getElementById('edit-title').value = STATE.user.title || "";
  document.getElementById('edit-bio').value = bioText;
  document.getElementById('edit-experience').value = expText;
  document.getElementById('edit-education').value = eduText;
  document.getElementById('edit-skills').value = STATE.user.skills ? STATE.user.skills.join(', ') : "";
  
  document.getElementById('profile-edit-modal').classList.remove('hidden');
  setTimeout(() => { lucide.createIcons(); }, 10);
}

function closeProfileModal() {
  document.getElementById('profile-edit-modal').classList.add('hidden');
}

async function handleProfileEditSubmit(event) {
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
    education: education
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

async function syncUserApplications() {
  if (!STATE.user.isLoggedIn || !STATE.user.email) return;
  try {
    const response = await fetch(`${BASE_URL}/applications?email=${encodeURIComponent(STATE.user.email)}`);
    if (response.ok) {
      const appliedJobIds = await response.json();
      STATE.user.appliedJobIds = appliedJobIds || [];
    }
  } catch (error) {
    console.error("Failed to load user applications:", error);
  }
}

function openJobModal(jobId) {
  const job = STATE.jobs.find(j => j.id === jobId);
  if (!job) return;
  
  document.getElementById('edit-job-id').value = job.id;
  document.getElementById('edit-job-company').value = job.company || "";
  document.getElementById('edit-job-title').value = job.title || "";
  document.getElementById('edit-job-location').value = job.location || "";
  document.getElementById('edit-job-salary').value = job.salary || "";
  
  let descriptionClean = job.description;
  const techIndex = descriptionClean.indexOf("\n\nKey Technologies:");
  if (techIndex > -1) {
    descriptionClean = descriptionClean.substring(0, techIndex);
  }
  document.getElementById('edit-job-desc').value = descriptionClean;
  
  document.getElementById('job-edit-modal').classList.remove('hidden');
  setTimeout(() => { lucide.createIcons(); }, 10);
}

function closeJobModal() {
  document.getElementById('job-edit-modal').classList.add('hidden');
}

async function handleJobEditSubmit(event) {
  event.preventDefault();
  const jobId = document.getElementById('edit-job-id').value;
  const company = document.getElementById('edit-job-company').value.trim();
  const title = document.getElementById('edit-job-title').value.trim();
  const location = document.getElementById('edit-job-location').value.trim();
  const salary = document.getElementById('edit-job-salary').value.trim();
  const desc = document.getElementById('edit-job-desc').value.trim();
  
  const job = STATE.jobs.find(j => j.id == jobId);
  const tagsStr = job && job.tags.length > 0 ? "\n\nKey Technologies: " + job.tags.join(', ') : "";
  const descriptionWithTags = desc + tagsStr;

  try {
    const response = await fetch(`${BASE_URL}/jobs/${jobId}?email=${encodeURIComponent(STATE.user.email)}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title,
        company,
        salary,
        location,
        description: descriptionWithTags
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

async function loadJobsFromBackend() {
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
        const logo = job.company.charAt(0).toUpperCase();
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

        let postedTime = "Just now";
        if (job.created_at) {
          postedTime = "Posted recently";
        }

        return {
          id: job.id,
          title: job.title,
          company: job.company,
          logo: logo,
          logoBg: logoBg,
          location: job.location,
          salary: job.salary,
          type: type,
          tags: tags,
          postedTime: postedTime,
          description: job.description,
          posted_by: job.posted_by || "system"
        };
      });

      renderJobs();
    }
  } catch (error) {
    console.error("Failed to load jobs from backend:", error);
  }
}

// loadDefaultUserProfile function removed

function changeProfilePhoto() {
  const avatarUrl = prompt("Enter a new image URL for your avatar:", STATE.user.avatar);
  if (avatarUrl) {
    STATE.user.avatar = avatarUrl;
    document.getElementById('profile-avatar').src = avatarUrl;
    syncAuthNav();
    showToast("Avatar image updated.");
  }
}

function renderMyPostedJobs() {
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
  container.innerHTML = myJobs.map(job => `
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3.5 rounded-2xl bg-brand-background/45 border border-slate-800/60 hover:border-cyan-500/20 transition-all duration-200">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl flex items-center justify-center font-bold text-xs select-none shrink-0 ${job.logoBg}">
          ${job.logo}
        </div>
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
  `).join('');

  lucide.createIcons();
}

function renderExperienceHtml(expText) {
  if (!expText) return "";
  const blocks = expText.split('\n\n').filter(Boolean);
  return blocks.map((block, idx) => {
    const lines = block.split('\n').filter(Boolean);
    const title = lines[0] || "Role Title";
    const companyDate = lines[1] || "";
    const description = lines.slice(2).join('\n') || "";
    const dotColor = idx === 0 ? "bg-cyan-400" : "bg-slate-700";
    
    return `
      <div class="relative pl-6 border-l border-slate-800 dark:border-slate-700/50">
        <div class="absolute -left-1.5 top-1.5 w-3 h-3 rounded-full ${dotColor}"></div>
        <h4 class="text-sm font-bold text-white">${title}</h4>
        <p class="text-xs text-slate-400">${companyDate}</p>
        ${description ? `<p class="text-xs text-slate-300 mt-1">${description}</p>` : ''}
      </div>
    `;
  }).join('');
}

function renderEducationHtml(eduText) {
  if (!eduText) return "";
  const blocks = eduText.split('\n\n').filter(Boolean);
  return blocks.map(block => {
    const lines = block.split('\n').filter(Boolean);
    const degree = lines[0] || "Degree";
    const schoolDate = lines[1] || "";
    
    return `
      <div class="relative pl-6 border-l border-slate-800 dark:border-slate-700/50">
        <div class="absolute -left-1.5 top-1.5 w-3 h-3 rounded-full bg-cyan-400/50"></div>
        <h4 class="text-sm font-bold text-white">${degree}</h4>
        <p class="text-xs text-slate-400">${schoolDate}</p>
      </div>
    `;
  }).join('');
}

// ==================== WEBSOCKET GENERAL CHAT & NOTIFICATIONS ====================
let chatSocket = null;
let notificationHistory = [];

function toggleNotificationDropdown() {
  const dropdown = document.getElementById('notification-dropdown');
  if (dropdown) {
    dropdown.classList.toggle('hidden');
  }
}

// Close notification dropdown when clicking outside
window.addEventListener('click', (e) => {
  const dropdown = document.getElementById('notification-dropdown');
  if (!dropdown) return;
  const btn = dropdown.previousElementSibling;
  const target = e.target;
  if (!dropdown.classList.contains('hidden') && !dropdown.contains(target) && (!btn || !btn.contains(target))) {
    dropdown.classList.add('hidden');
  }
});

function addNotification(message, applicant = null) {
  notificationHistory.unshift({
    message: message,
    timestamp: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }),
    applicant: applicant
  });
  
  if (notificationHistory.length > 10) {
    notificationHistory.pop();
  }
  
  updateNotificationUI();
}

function updateNotificationUI() {
  const badge = document.getElementById('notification-badge');
  const list = document.getElementById('notification-list');
  if (!list) return;
  
  if (notificationHistory.length > 0) {
    if (badge) badge.classList.remove('hidden');
    list.innerHTML = notificationHistory.map((n, idx) => {
      const clickableClass = n.applicant ? ' cursor-pointer hover:border-cyan-400/50 hover:bg-slate-900/80 transition duration-150' : '';
      const clickAttr = n.applicant ? ` onclick="handleNotificationClick(${idx})"` : '';
      return `
        <div class="p-2.5 rounded-xl bg-slate-900/45 border border-slate-800/60 flex flex-col gap-1${clickableClass}"${clickAttr}>
          <p class="text-slate-300 leading-normal font-medium">${n.message}</p>
          <span class="text-[9px] text-slate-500 self-end">${n.timestamp}</span>
        </div>
      `;
    }).join('');
  } else {
    if (badge) badge.classList.add('hidden');
    list.innerHTML = `<p class="text-center py-4 text-slate-500">Chưa có thông báo nào mới.</p>`;
  }
}

function handleNotificationClick(idx) {
  const item = notificationHistory[idx];
  if (item && item.applicant) {
    showApplicantDetails(item.applicant);
  }
}

function clearNotifications() {
  notificationHistory = [];
  updateNotificationUI();
}

async function loadNotificationsFromBackend() {
  try {
    const response = await fetch(`${BASE_URL}/notifications`);
    if (response.ok) {
      const data = await response.json();
      notificationHistory = data;
      updateNotificationUI();
    }
  } catch (error) {
    console.error("Failed to load notifications from backend:", error);
  }
}

function initWebSocket() {
  const wsProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
  const rawHost = window.location.host;
  let wsHost = '127.0.0.1:8000';
  if (rawHost && !rawHost.includes('file://')) {
    if (rawHost.includes(':5500')) {
      wsHost = rawHost.replace(':5500', ':8000');
    } else {
      wsHost = rawHost;
    }
  }
  const wsUrl = `${wsProtocol}://${wsHost}/ws`;
  
  console.log("Connecting to WebSocket:", wsUrl);
  chatSocket = new WebSocket(wsUrl);

  chatSocket.onopen = () => {
    console.log("WebSocket connected successfully.");
    const statusDot = document.getElementById('chat-status-dot');
    const statusText = document.getElementById('chat-status-text');
    if (statusDot) {
      statusDot.className = "flex h-2 w-2 rounded-full bg-emerald-400 animate-pulse";
    }
    if (statusText) {
      statusText.innerText = "Trực tuyến";
      statusText.className = "text-emerald-400 text-xs font-semibold";
    }
  };

  chatSocket.onmessage = async (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.type === 'notification') {
        showToast(data.message, 'success', data.applicant);
        addNotification(data.message, data.applicant);
        await syncUserApplications();
        if (STATE.activeTab === 'profile') {
          renderProfile();
        }
      } else if (data.type === 'chat') {
        appendChatMessage(data);
      }
    } catch (e) {
      console.error("Failed to parse incoming WebSocket message:", e);
    }
  };

  chatSocket.onclose = () => {
    console.log("WebSocket disconnected. Reconnecting in 3 seconds...");
    const statusDot = document.getElementById('chat-status-dot');
    const statusText = document.getElementById('chat-status-text');
    if (statusDot) {
      statusDot.className = "flex h-2 w-2 rounded-full bg-red-400 animate-pulse";
    }
    if (statusText) {
      statusText.innerText = "Ngoại tuyến (Kết nối lại...)";
      statusText.className = "text-red-400 text-xs font-semibold";
    }
    setTimeout(initWebSocket, 3000);
  };

  chatSocket.onerror = (err) => {
    console.error("WebSocket connection error:", err);
  };
}

function appendChatMessage(data) {
  const chatMessages = document.getElementById('chat-messages');
  if (!chatMessages) return;

  const isMe = STATE.user.isLoggedIn && data.username === STATE.user.name;
  const username = data.username || "Ẩn danh";
  const initials = username.charAt(0).toUpperCase();

  const messageHtml = isMe ? `
    <div class="flex items-start gap-2.5 max-w-lg ml-auto justify-end">
      <div class="space-y-1 text-right">
        <div class="flex items-center gap-2 justify-end">
          <span class="text-[9px] text-slate-500">${data.timestamp || ''}</span>
          <span class="text-xs font-bold text-cyan-400">${username}</span>
        </div>
        <div class="rounded-2xl rounded-tr-none p-3.5 bg-cyan-950/60 border border-cyan-500/30 text-xs text-cyan-100 leading-relaxed text-left">
          ${escapeHTML(data.message)}
        </div>
      </div>
      <div class="w-8 h-8 rounded-lg bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 flex items-center justify-center font-bold text-xs shrink-0 select-none">${initials}</div>
    </div>
  ` : `
    <div class="flex items-start gap-2.5 max-w-lg">
      <div class="w-8 h-8 rounded-lg bg-slate-800 text-slate-300 border border-slate-700 flex items-center justify-center font-bold text-xs shrink-0 select-none">${initials}</div>
      <div class="space-y-1">
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold text-slate-200">${username}</span>
          <span class="text-[9px] text-slate-500">${data.timestamp || ''}</span>
        </div>
        <div class="rounded-2xl rounded-tl-none p-3.5 bg-slate-900/60 border border-slate-800 text-xs text-slate-300 leading-relaxed">
          ${escapeHTML(data.message)}
        </div>
      </div>
    </div>
  `;

  chatMessages.insertAdjacentHTML('beforeend', messageHtml);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function handleChatSubmit(event) {
  event.preventDefault();
  const chatInput = document.getElementById('chat-input');
  if (!chatInput || !chatSocket || chatSocket.readyState !== WebSocket.OPEN) return;

  const msg = chatInput.value.trim();
  if (!msg) return;

  const username = STATE.user.isLoggedIn ? STATE.user.name : "Ẩn danh";
  chatSocket.send(JSON.stringify({
    type: 'chat',
    username: username,
    message: msg
  }));

  chatInput.value = '';
}

function escapeHTML(str) {
  return str.replace(/[&<>'"]/g, 
    tag => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[tag] || tag)
  );
}

function showApplicantDetails(applicant) {
  if (!applicant) return;
  
  // Set text fields
  document.getElementById('applicant-modal-name').innerText = applicant.name || "Candidate Name";
  document.getElementById('applicant-modal-email').innerText = applicant.email || "candidate@email.com";
  document.getElementById('applicant-modal-major').innerText = applicant.major || "Chưa cập nhật";
  
  let yearText = "Năm 1";
  if (applicant.student_year) {
    yearText = `Năm ${applicant.student_year}`;
  }
  document.getElementById('applicant-modal-year').innerText = yearText;
  document.getElementById('applicant-modal-job').innerText = applicant.job_title || "Software Engineer";
  document.getElementById('applicant-modal-company').innerText = applicant.job_company || "Vercel";
  
  // Set initials
  const initials = (applicant.name || "U").charAt(0).toUpperCase();
  document.getElementById('applicant-modal-avatar').innerText = initials;
  
  // Display modal
  const modal = document.getElementById('applicant-detail-modal');
  if (modal) {
    modal.classList.remove('hidden');
  }
  
  lucide.createIcons();
}

function closeApplicantModal() {
  const modal = document.getElementById('applicant-detail-modal');
  if (modal) {
    modal.classList.add('hidden');
  }
}
