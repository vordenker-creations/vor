/**
 * AI-Career Bridge - Recruiter Web Core Controller
 * Serves as the central state coordinator, route manager, and initializer.
 */

// Dynamic API host configuration
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

export const BACKEND_HOST = getBackendHost();
export const BASE_URL = `${window.location.protocol === 'file:' ? 'http:' : window.location.protocol}//${BACKEND_HOST}`;

// Load session from localStorage if exists
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

export const STATE = {
  user: initialUser,
  jobs: [],
  currentSearch: {
    keyword: "",
    location: ""
  },
  minSalary: 50000,
  activeTab: "cvs",
  activeJobId: null,
  lang: localStorage.getItem('lang') || 'vi'
};

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

export function syncThemeIcon() {
  const iconEl = document.getElementById('theme-toggle-icon');
  if (!iconEl) return;
  const isDark = document.documentElement.classList.contains('dark');
  if (isDark) {
    iconEl.setAttribute('data-lucide', 'sun');
  } else {
    iconEl.setAttribute('data-lucide', 'moon');
  }
  if (window.lucide) window.lucide.createIcons();
}

export function toggleTheme() {
  const isDark = document.documentElement.classList.contains('dark');
  if (isDark) {
    document.documentElement.classList.remove('dark');
    localStorage.setItem('theme', 'light');
  } else {
    document.documentElement.classList.add('dark');
    localStorage.setItem('theme', 'dark');
  }
  syncThemeIcon();
  showToast(STATE.lang === 'vi' ? `Đã chuyển sang chế độ ${isDark ? 'Sáng' : 'Tối'}.` : `Switched to ${isDark ? 'Light' : 'Dark'} mode.`);
}

// ==================== LANGUAGE TRANSLATION SYSTEM ====================

export const TRANSLATIONS = {
  vi: {
    // CV Tab & AI Match
    nav_cvs: "CV Sinh viên",
    nav_cvs_mobile: "CV Sinh viên",
    cv_hero_badge: "Đối sánh thông minh AI & Đề xuất",
    cv_hero_title: "Đề xuất ứng viên tối ưu bằng AI",
    cv_hero_subtitle: "Chọn một bài đăng tuyển dụng của bạn để hệ thống tự động lọc, đối sánh GPA, kỹ năng cốt lõi và đề xuất các CV sinh viên xuất sắc nhất từ Desktop client.",
    cv_select_job_placeholder: "Chọn tin đăng của bạn...",
    cv_match_btn: "Đề xuất CV bằng AI",
    cv_list_title: "Danh sách CV Sinh viên",
    cv_req_gpa: "GPA tối thiểu",
    cv_req_lang: "Ngoại ngữ",
    cv_req_skills: "Kỹ năng yêu cầu",
    cv_major_cs: "Khoa học Máy tính / CNTT",
    cv_major_is: "An toàn Thông tin",
    cv_major_ds: "Khoa học Dữ liệu / AI",
    cv_modal_title: "Chi tiết CV Sinh viên",
    cv_modal_skills: "Danh sách kỹ năng",
    cv_ai_report_title: "Báo cáo phân tích đối sánh AI",
    cv_ai_gpa_check: "Tiêu chuẩn GPA",
    cv_ai_skills_check: "Kỹ năng chuyên môn",
    cv_ai_lang_check: "Trình độ Ngoại ngữ",
    cv_ai_verdict: "Đánh giá sự tương thích",
    cv_sync_status: "Desktop App SQLite database",
    cv_sync_connected: "Đã kết nối",
    cv_sync_btn: "Sync Now",
    cv_sync_title: "Nguồn dữ liệu cục bộ",
    cv_hide_filters: "Ẩn bộ lọc",
    cv_show_filters: "Hiện bộ lọc",

    // Header & Navigation
    nav_jobs: "Việc làm",
    nav_post_job: "Đăng tuyển dụng",
    nav_applicants: "Quản lý ứng viên",
    nav_chat: "Thảo luận",
    nav_profile: "Hồ sơ công ty",
    nav_jobs_mobile: "Tìm việc làm",
    nav_post_job_mobile: "Đăng tuyển dụng",
    nav_applicants_mobile: "Quản lý ứng viên",
    nav_profile_mobile: "Hồ sơ công ty",
    nav_chat_mobile: "Thảo luận",
    
    // Auth Nav & Actions
    btn_signin: "Đăng nhập",
    btn_joinnow: "Đăng ký ngay",
    dropdown_recruiter: "Doanh nghiệp",
    dropdown_profile: "Hồ sơ của tôi",
    dropdown_post: "Đăng tuyển dụng",
    dropdown_manage: "Quản lý ứng viên",
    dropdown_logout: "Đăng xuất",
    
    // Hero
    hero_badge: "Hơn 1,240 vị trí Công nghệ đang tuyển dụng",
    hero_title: "Tìm kiếm vị trí <span class=\"bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent\">Lập trình viên</span> mơ ước.",
    hero_subtitle: "Khám phá các vị trí công nghệ lương cao, cơ hội lập trình từ xa được cập nhật hàng ngày với tính minh bạch tuyệt đối.",
    hero_search_btn: "Tìm kiếm",
    hero_recent_searches: "Tìm kiếm gần đây:",
    search_keyword_placeholder: "Tiêu đề công việc, công nghệ, kỹ năng...",
    search_location_placeholder: "Thành phố hoặc Remote",
    
    // Sidebar Filters
    filter_title: "Bộ lọc",
    filter_type: "Loại hình làm việc",
    filter_remote: "Chỉ làm từ xa",
    filter_salary: "Lương tối thiểu ($ / Năm)",
    filter_tech: "Công nghệ cốt lõi",
    filter_clear: "Xóa tất cả bộ lọc",
    
    // Jobs list
    jobs_available: "Tin tuyển dụng hiện có",
    jobs_sortby: "Sắp xếp theo:",
    sort_recent: "Mới nhất",
    sort_salary: "Lương cao nhất",
    job_status_active: "Đang nhận đơn",
    job_status_closed: "Đã đóng nhận đơn",
    job_posted_recently: "Vừa đăng gần đây",
    job_posted_justnow: "Vừa xong",
    btn_view_details: "Xem chi tiết",
    confirm_delete_job: "Bạn có chắc chắn muốn xóa tin tuyển dụng này?",
    
    // Job Detail Sidebar & Header
    detail_back: "Quay lại danh sách",
    detail_status_active: "Hoạt động",
    detail_status_closed: "Đã đóng",
    detail_open_recruitment: "Mở nhận hồ sơ",
    detail_close_recruitment: "Đóng nhận hồ sơ",
    detail_export_csv: "Xuất danh sách ứng viên (CSV)",
    detail_edit_listing: "Chỉnh sửa tin đăng",
    detail_delete_listing: "Xóa tin đăng",
    detail_other_company_job: "Bạn đang xem tin tuyển dụng của công ty khác.",
    
    detail_sidebar_title: "Chi tiết công việc",
    detail_label_location: "Địa điểm làm việc",
    detail_label_salary: "Mức lương cơ bản",
    detail_label_experience: "Kinh nghiệm yêu cầu",
    detail_label_stack: "Công nghệ yêu cầu",
    detail_label_gpa: "Điểm GPA tối thiểu",
    detail_label_languages: "Yêu cầu Ngoại ngữ",
    detail_label_other: "Yêu cầu khác",
    detail_experience_value: "Cấp bậc Senior (5+ năm)",
    
    // Post Job Form
    post_title: "Đăng tuyển vị trí Công nghệ",
    post_subtitle: "Tìm kiếm tài năng kỹ thuật hàng đầu với quy trình tuyển dụng tinh gọn",
    post_sec1: "1. Hồ sơ doanh nghiệp",
    post_company_name: "Tên doanh nghiệp",
    post_website: "Đường dẫn Website",
    post_logo: "Logo công ty",
    post_logo_status: "Kéo thả logo vào đây, hoặc <span class=\"text-cyan-400\">chọn tệp</span>",
    post_logo_info: "Định dạng PNG, JPG tối đa 2MB",
    post_sec2: "2. Chi tiết công việc",
    post_job_title: "Tiêu đề công việc",
    post_job_type: "Hình thức làm việc",
    post_job_location: "Địa điểm",
    post_job_salary: "Mức lương ($ / Năm)",
    post_job_gpa: "Điểm GPA tối thiểu",
    post_job_languages: "Yêu cầu Ngoại ngữ",
    post_job_other: "Yêu cầu khác",
    post_sec3: "3. Công nghệ & Mô tả",
    post_job_tech: "Công nghệ chính (Nhấn Enter để thêm)",
    post_job_desc: "Mô tả công việc * (Hỗ trợ định dạng Markdown)",
    btn_cancel: "Hủy bỏ",
    btn_publish: "Đăng tuyển",
    btn_publishing: "Đang đăng tuyển...",
    
    // Profile Page & Edit Modal
    profile_joined: "Tham gia:",
    profile_edit_details: "Chỉnh sửa thông tin",
    profile_edit_title: "Cập nhật hồ sơ doanh nghiệp",
    profile_edit_subtitle: "Cập nhật thông tin nhận diện doanh nghiệp của bạn",
    profile_edit_name: "Tên Doanh nghiệp",
    profile_edit_domain: "Lĩnh vực hoạt động chính",
    profile_edit_bio: "Giới thiệu doanh nghiệp",
    profile_edit_headquarters: "Trụ sở & Quy mô (Mỗi thông tin 1 dòng)",
    profile_edit_contact: "Website & Liên hệ (Mỗi thông tin 1 dòng)",
    profile_edit_skills: "Công nghệ sử dụng chính (phân cách bằng dấu phẩy)",
    btn_save_changes: "Lưu thay đổi",
    profile_bio_placeholder: "Giới thiệu về doanh nghiệp tuyển dụng của bạn.",
    profile_exp_placeholder: "Trụ sở chính: San Francisco, CA\nQuy mô: 500-1000 nhân viên",
    profile_edu_placeholder: "Website: https://vercel.com\nEmail: contact@vercel.com",
    profile_no_skills: "Chưa cập nhật công nghệ."
  },
  en: {
    // CV Tab & AI Match
    nav_cvs: "Student CVs",
    nav_cvs_mobile: "Student CVs",
    cv_hero_badge: "AI Smart Matching & Recommendations",
    cv_hero_title: "Optimal Candidate Recommendations via AI",
    cv_hero_subtitle: "Select one of your job listings to automatically filter, match GPA, core skills, and recommend the best student CVs from the Desktop client.",
    cv_select_job_placeholder: "Select your job listing...",
    cv_match_btn: "Match CVs with AI",
    cv_list_title: "Student CV Listings",
    cv_req_gpa: "Minimum GPA",
    cv_req_lang: "Foreign Languages",
    cv_req_skills: "Required Stack",
    cv_major_cs: "Computer Science / IT",
    cv_major_is: "Information Security",
    cv_major_ds: "Data Science / AI",
    cv_modal_title: "Student CV Details",
    cv_modal_skills: "Skills Stack",
    cv_ai_report_title: "AI Matching Analysis Report",
    cv_ai_gpa_check: "GPA Standard Check",
    cv_ai_skills_check: "Technical Skills Alignment",
    cv_ai_lang_check: "Language Proficiency",
    cv_ai_verdict: "Match Compatibility Verdict",
    cv_sync_status: "Desktop App SQLite database",
    cv_sync_connected: "Connected",
    cv_sync_btn: "Sync Now",
    cv_sync_title: "Local Client Source",
    cv_hide_filters: "Hide Filters",
    cv_show_filters: "Show Filters",

    // Header & Navigation
    nav_jobs: "Jobs",
    nav_post_job: "Post Job",
    nav_applicants: "Applicants",
    nav_chat: "Discussion",
    nav_profile: "Company Profile",
    nav_jobs_mobile: "Find Jobs",
    nav_post_job_mobile: "Post Job",
    nav_applicants_mobile: "Manage Applicants",
    nav_profile_mobile: "Company Profile",
    nav_chat_mobile: "Discussion",
    
    // Auth Nav & Actions
    btn_signin: "Sign In",
    btn_joinnow: "Join Now",
    dropdown_recruiter: "Recruiter",
    dropdown_profile: "My Profile",
    dropdown_post: "Post Job",
    dropdown_manage: "Manage Applicants",
    dropdown_logout: "Sign Out",
    
    // Hero
    hero_badge: "Over 1,240 Tech Roles Open Today",
    hero_title: "Find the Next <span class=\"bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent\">Developer</span> Masterpiece.",
    hero_subtitle: "Explore high-paying tech jobs, premium SaaS roles, and remote coding opportunities curated daily with absolute visual transparency.",
    hero_search_btn: "Search",
    hero_recent_searches: "Recent searches:",
    search_keyword_placeholder: "Job title, technology, skills...",
    search_location_placeholder: "City or Remote",
    
    // Sidebar Filters
    filter_title: "Filters",
    filter_type: "Employment Type",
    filter_remote: "Remote Only",
    filter_salary: "Min Salary ($ / Year)",
    filter_tech: "Key Technologies",
    filter_clear: "Clear All Filters",
    
    // Jobs list
    jobs_available: "Available Listings",
    jobs_sortby: "Sort by:",
    sort_recent: "Most Recent",
    sort_salary: "Highest Salary",
    job_status_active: "Active",
    job_status_closed: "Closed",
    job_posted_recently: "Posted recently",
    job_posted_justnow: "Just now",
    btn_view_details: "View Details",
    confirm_delete_job: "Are you sure you want to delete this job listing?",
    
    // Job Detail Sidebar & Header
    detail_back: "Back to Jobs",
    detail_status_active: "Active",
    detail_status_closed: "Closed",
    detail_open_recruitment: "Open Recruitment",
    detail_close_recruitment: "Close Recruitment",
    detail_export_csv: "Export Applicants (CSV)",
    detail_edit_listing: "Edit Listing",
    detail_delete_listing: "Delete Listing",
    detail_other_company_job: "You are viewing a job post from another company.",
    
    detail_sidebar_title: "Employment Details",
    detail_label_location: "Location Status",
    detail_label_salary: "Base Salary Range",
    detail_label_experience: "Experience Needed",
    detail_label_stack: "Required Stack",
    detail_label_gpa: "Minimum GPA",
    detail_label_languages: "Foreign Languages",
    detail_label_other: "Other requirements",
    detail_experience_value: "Senior Level (5+ yrs)",
    
    // Post Job Form
    post_title: "Post a Tech Role",
    post_subtitle: "Find top-tier engineering talent with our streamlined developer workflow",
    post_sec1: "1. Company Profile",
    post_company_name: "Company Name",
    post_website: "Website URL",
    post_logo: "Company Logo",
    post_logo_status: "Drag and drop logo, or <span class=\"text-cyan-400\">browse</span>",
    post_logo_info: "PNG, JPG up to 2MB",
    post_sec2: "2. Job Specifications",
    post_job_title: "Job Title",
    post_job_type: "Employment Type",
    post_job_location: "Location",
    post_job_salary: "Salary Range ($ / Year)",
    post_job_gpa: "Minimum GPA",
    post_job_languages: "Foreign Languages",
    post_job_other: "Other requirements",
    post_sec3: "3. Stack & Description",
    post_job_tech: "Key Technologies (Press Enter to add tag)",
    post_job_desc: "Job Description * (Rich Markdown Preview supported)",
    btn_cancel: "Cancel",
    btn_publish: "Publish Listing",
    btn_publishing: "Publishing...",
    
    // Profile Page & Edit Modal
    profile_joined: "Joined:",
    profile_edit_details: "Edit Details",
    profile_edit_title: "Edit Company Profile Details",
    profile_edit_subtitle: "Update your business identity information",
    profile_edit_name: "Company Name",
    profile_edit_domain: "Core Industry",
    profile_edit_bio: "Company Introduction",
    profile_edit_headquarters: "Headquarters & Scale (One info per line)",
    profile_edit_contact: "Website & Contact (One info per line)",
    profile_edit_skills: "Core Technologies (separated by comma)",
    btn_save_changes: "Save Changes",
    profile_bio_placeholder: "Introduction about your recruiting company.",
    profile_exp_placeholder: "Headquarters: San Francisco, CA\nScale: 500-1000 employees",
    profile_edu_placeholder: "Website: https://vercel.com\nEmail: contact@vercel.com",
    profile_no_skills: "No technologies updated."
  }
};

export function t(key) {
  const lang = STATE.lang || 'vi';
  return (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) || key;
}

export function updateLanguageUI() {
  const lang = STATE.lang || 'vi';
  const dict = TRANSLATIONS[lang];
  
  // 1. Translate all static elements with data-i18n attribute
  const elements = document.querySelectorAll('[data-i18n]');
  elements.forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      if (key === 'hero_title' || key === 'post_logo_status' || key === 'post_job_desc') {
        el.innerHTML = dict[key];
      } else {
        el.innerText = dict[key];
      }
    }
  });

  // Translate tooltips / titles
  const titleElements = document.querySelectorAll('[data-i18n-title]');
  titleElements.forEach(el => {
    const key = el.getAttribute('data-i18n-title');
    if (dict[key]) {
      el.setAttribute('title', dict[key]);
    }
  });

  // 2. Translate placeholders
  const searchKeyword = document.getElementById('search-keyword');
  if (searchKeyword) {
    searchKeyword.placeholder = dict.search_keyword_placeholder;
  }
  const searchLocation = document.getElementById('search-location');
  if (searchLocation) {
    searchLocation.placeholder = dict.search_location_placeholder;
  }

  // 3. Update the select sort options manually
  const sortSelect = document.getElementById('sort-select');
  if (sortSelect && sortSelect.options.length >= 2) {
    sortSelect.options[0].text = dict.sort_recent;
    sortSelect.options[1].text = dict.sort_salary;
  }
  
  // 4. Update page title
  document.title = lang === 'vi' 
    ? "AI-Career bridge ✦ Cổng thông tin Tuyển dụng Công nghệ Cao cấp" 
    : "AI-Career bridge ✦ Premium Tech Job Board";
}

export function toggleLanguage() {
  const newLang = STATE.lang === 'vi' ? 'en' : 'vi';
  STATE.lang = newLang;
  localStorage.setItem('lang', newLang);
  
  // Update lang label button
  const label = document.getElementById('current-lang-label');
  if (label) label.innerText = newLang.toUpperCase();
  
  // Trigger update across UI
  updateLanguageUI();
  
  // Reload jobs to update job status badges and lists
  if (window.renderJobs) window.renderJobs();
  if (window.renderCvs) window.renderCvs();
  if (STATE.activeTab === 'job-detail' && STATE.activeJobId && window.renderJobDetail) {
    window.renderJobDetail(STATE.activeJobId);
  }
  if (STATE.activeTab === 'profile' && window.renderProfile) {
    window.renderProfile();
  }
  
  showToast(newLang === 'vi' ? "Đã chuyển sang Tiếng Việt" : "Switched to English");
}

export function toggleMobileMenu() {
  const menu = document.getElementById('mobile-menu');
  if (menu) menu.classList.toggle('hidden');
}

export function toggleNavLabels() {
  const nav = document.querySelector('header nav');
  const icon = document.getElementById('nav-toggle-icon');
  if (!nav) return;

  const isCompact = nav.classList.contains('compact-nav');
  if (isCompact) {
    nav.classList.remove('compact-nav');
    localStorage.setItem('navCompact', 'false');
    if (icon) icon.setAttribute('data-lucide', 'chevrons-left');
  } else {
    nav.classList.add('compact-nav');
    localStorage.setItem('navCompact', 'true');
    if (icon) icon.setAttribute('data-lucide', 'chevrons-right');
  }
  if (window.lucide) window.lucide.createIcons();
}

export function showToast(message, type = 'success', applicant = null) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  
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
  if (applicant && window.showApplicantDetails) {
    clickClass = ' cursor-pointer hover:border-cyan-400/50 hover:shadow-glow-cyan/30 transition-all duration-300';
    toast.onclick = () => {
      window.showApplicantDetails(applicant);
    };
  }

  toast.className = `glass-card border px-4 py-3 rounded-xl flex items-center gap-2.5 shadow-lg transform transition-all duration-300 translate-y-2 opacity-0 pointer-events-auto ${typeStyle}${clickClass}`;
  toast.innerHTML = `
    <i data-lucide="${icon}" class="w-4 h-4 shrink-0"></i>
    <p class="text-xs font-semibold">${message}</p>
  `;
  
  container.appendChild(toast);
  if (window.lucide) window.lucide.createIcons();

  setTimeout(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
  }, 50);

  setTimeout(() => {
    toast.classList.add('translate-y-[-10px]', 'opacity-0');
    setTimeout(() => {
      toast.remove();
    }, 300);
  }, 12000);
}

export function setFieldError(inputId, errorId, message) {
  const inputEl = document.getElementById(inputId);
  const errorEl = document.getElementById(errorId);
  if (inputEl) inputEl.classList.add('input-error');
  if (errorEl) errorEl.textContent = message;
}

export function clearFieldError(inputId, errorId) {
  const inputEl = document.getElementById(inputId);
  const errorEl = document.getElementById(errorId);
  if (inputEl) inputEl.classList.remove('input-error');
  if (errorEl) errorEl.textContent = '';
}

export function clearAllErrors() {
  clearFieldError('post-comp-name', 'companyError');
  clearFieldError('post-job-title', 'titleError');
  clearFieldError('post-job-location', 'locationError');
  clearFieldError('post-job-salary', 'salaryError');
  clearFieldError('post-job-desc', 'descriptionError');
}

export function syncAuthNav() {
  const guestNav = document.getElementById('auth-nav-guest');
  const userNav = document.getElementById('auth-nav-user');
  const recruiterLinks = document.querySelectorAll('.recruiter-link');
  
  if (STATE.user.isLoggedIn) {
    if (guestNav) guestNav.classList.add('hidden');
    if (userNav) userNav.classList.remove('hidden');
    
    const navUsername = document.getElementById('navbar-username');
    const navAvatar = document.getElementById('navbar-avatar');
    const navDropdownEmail = document.getElementById('navbar-dropdown-email');
    
    if (navUsername) navUsername.innerText = STATE.user.name;
    if (navAvatar) navAvatar.src = STATE.user.avatar;
    if (navDropdownEmail) navDropdownEmail.innerText = STATE.user.email;
    
    // Show recruiter-specific navigation tabs
    recruiterLinks.forEach(link => link.classList.remove('hidden'));
  } else {
    if (guestNav) guestNav.classList.remove('hidden');
    if (userNav) userNav.classList.add('hidden');
    
    // Hide recruiter-specific navigation tabs
    recruiterLinks.forEach(link => link.classList.add('hidden'));
  }
}

export function toggleUserDropdown() {
  const dropdown = document.getElementById('user-menu-dropdown');
  if (dropdown) {
    dropdown.classList.toggle('hidden');
  }
}
window.toggleUserDropdown = toggleUserDropdown;

// Close dropdowns on clicking outside
window.addEventListener('click', (e) => {
  // 1. User profile dropdown
  const userDropdown = document.getElementById('user-menu-dropdown');
  if (userDropdown && !userDropdown.classList.contains('hidden')) {
    const btn = userDropdown.previousElementSibling;
    const target = e.target;
    if (!userDropdown.contains(target) && (!btn || !btn.contains(target))) {
      userDropdown.classList.add('hidden');
    }
  }

  // 2. Notifications dropdown
  const notifDropdown = document.getElementById('notification-dropdown');
  if (notifDropdown && !notifDropdown.classList.contains('hidden')) {
    const btn = notifDropdown.previousElementSibling;
    const target = e.target;
    if (!notifDropdown.contains(target) && (!btn || !btn.contains(target))) {
      notifDropdown.classList.add('hidden');
    }
  }
});

// ==================== ROUTING SYSTEM (Tab switcher) ====================
export function switchTab(tabName, additionalParams = {}) {
  // Authorization check
  if ((tabName === 'profile' || tabName === 'post-job' || tabName === 'applicants') && !STATE.user.isLoggedIn) {
    showToast("Vui lòng đăng ký/đăng nhập tài khoản Doanh nghiệp để truy cập trang này.", "error");
    switchTab('login');
    return;
  }

  STATE.activeTab = tabName;
  
  // Update UI active views
  const views = ['cvs', 'jobs', 'job-detail', 'login', 'register', 'post-job', 'profile', 'chat', 'applicants'];
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
  const navLinks = ['cvs', 'jobs', 'post-job', 'applicants', 'chat'];
  navLinks.forEach(link => {
    const el = document.getElementById(`nav-${link}`);
    if (el) {
      const isRecruiter = el.classList.contains('recruiter-link');
      const isHidden = el.classList.contains('hidden');
      
      let baseClasses = "text-xs font-semibold uppercase tracking-wider transition-all duration-200 flex items-center gap-1.5 px-3.5 py-1.5 rounded-full whitespace-nowrap";
      if (isRecruiter) baseClasses += " recruiter-link";
      if (isHidden) baseClasses += " hidden";
      
      if (link === tabName) {
        el.className = `${baseClasses} border border-cyan-500/20 bg-cyan-500/10 text-cyan-400 shadow-sm shadow-cyan-500/5`;
      } else {
        el.className = `${baseClasses} border border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-900/30`;
      }
    }
  });

  // Handle specific tab entries
  if (tabName === 'job-detail') {
    const jobId = additionalParams.id;
    STATE.activeJobId = jobId;
    if (window.renderJobDetail) window.renderJobDetail(jobId);
  }
  
  if (tabName === 'profile') {
    if (window.renderProfile) window.renderProfile();
  }

  if (tabName === 'applicants') {
    if (window.loadApplicantsFromBackend) window.loadApplicantsFromBackend();
  }

  if (tabName === 'cvs') {
    if (window.initCvsView) window.initCvsView();
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
  setTimeout(() => { if (window.lucide) window.lucide.createIcons(); }, 30);
}

// Bind navigation events globally
window.switchTab = switchTab;
window.toggleTheme = toggleTheme;
window.toggleMobileMenu = toggleMobileMenu;
window.toggleLanguage = toggleLanguage;
window.toggleNavLabels = toggleNavLabels;
window.t = t;

// Import child modules to ensure they bind window-level handlers
import './pages/jobs.js';
import './pages/job-detail.js';
import './pages/post-job.js';
import './pages/profile.js';
import './pages/auth.js';
import './pages/chat.js';
import './pages/applicants.js';
import './pages/cvs.js';

// ==================== APP BOOTSTRAP ====================
window.addEventListener('DOMContentLoaded', async () => {
  syncAuthNav();
  syncThemeIcon();
  
  // Initialize language label and UI texts
  const langLabel = document.getElementById('current-lang-label');
  if (langLabel) langLabel.innerText = STATE.lang.toUpperCase();
  updateLanguageUI();

  // Restore compact nav state
  const isCompact = localStorage.getItem('navCompact') === 'true';
  const nav = document.querySelector('header nav');
  const icon = document.getElementById('nav-toggle-icon');
  if (isCompact && nav) {
    nav.classList.add('compact-nav');
    if (icon) icon.setAttribute('data-lucide', 'chevrons-right');
  } else if (icon) {
    icon.setAttribute('data-lucide', 'chevrons-left');
  }
  
  if (window.loadJobsFromBackend) await window.loadJobsFromBackend();
  if (window.initCvsView) window.initCvsView();
  if (window.loadNotificationsFromBackend) await window.loadNotificationsFromBackend();
  if (window.renderProfile) window.renderProfile();
  if (window.loadRecentSearches) window.loadRecentSearches();
  if (window.initWebSocket) window.initWebSocket();

  // Setup filter change listeners
  const ftCheckbox = document.getElementById('filter-fulltime');
  const ctCheckbox = document.getElementById('filter-contract');
  const rmCheckbox = document.getElementById('filter-remote');
  if (ftCheckbox && window.renderJobs) ftCheckbox.addEventListener('change', window.renderJobs);
  if (ctCheckbox && window.renderJobs) ctCheckbox.addEventListener('change', window.renderJobs);
  if (rmCheckbox && window.renderJobs) rmCheckbox.addEventListener('change', window.renderJobs);

  const salarySlider = document.getElementById('filter-salary');
  if (salarySlider && window.renderJobs) salarySlider.addEventListener('input', window.renderJobs);

  // Setup field input watchers for clearing errors
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

  const salaryVal = document.getElementById('salary-min-val');
  if (salaryVal) salaryVal.innerText = "Any";
  if (window.lucide) window.lucide.createIcons();
});
