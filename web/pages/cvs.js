/**
 * AI-Career Bridge - Student CV Recommendation Module
 * Manages rendering, filtering, sorting, and AI-matching preview of candidate CVs.
 */

import { STATE, showToast, t, switchTab } from '../app.js';

export let lastEvaluatedCvs = [];
export let candidatesList = [];

export const MOCK_CVS = [
  {
    id: 10001,
    name: "Nguyễn Văn A",
    major: "CNTT",
    university: "Đại học Bách Khoa",
    gpa: 3.8,
    skills: ["React", "TypeScript", "Next.js", "Node.js", "TailwindCSS"],
    languages: "Tiếng Anh (IELTS 7.0)",
    bio: "Đam mê phát triển ứng dụng Web, có kinh nghiệm làm các dự án React và Next.js. Mong muốn tìm vị trí thực tập hoặc Junior Frontend.",
    avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=150&auto=format&fit=crop",
    certificates: []
  },
  {
    id: 10002,
    name: "Trần Thị B",
    major: "KHDL",
    university: "Đại học Khoa học Tự nhiên",
    gpa: 3.6,
    skills: ["Python", "PyTorch", "SQL", "Pandas", "AWS"],
    languages: "Tiếng Anh (IELTS 6.5)",
    bio: "Đam mê nghiên cứu xử lý dữ liệu và xây dựng mô hình AI, có kinh nghiệm triển khai các dự án deep learning về Computer Vision.",
    avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=150&auto=format&fit=crop",
    certificates: []
  },
  {
    id: 10003,
    name: "Lê Hoàng C",
    major: "ATTT",
    university: "Học viện Bưu chính Viễn thông",
    gpa: 3.2,
    skills: ["Linux", "Docker", "AWS", "Go", "Kubernetes"],
    languages: "Tiếng Anh (TOEIC 750)",
    bio: "Sinh viên chuyên ngành An toàn thông tin, yêu thích DevOps và bảo mật hệ thống. Có chứng chỉ AWS Cloud Practitioner.",
    avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=150&auto=format&fit=crop",
    certificates: []
  }
];

export let activeCvFilter = {
  gpa: 0.0,
  majors: ["CNTT", "ATTT", "KHDL"],
  skillQuery: ""
};

export async function fetchCvs() {
  try {
    const res = await fetch('/cvs');
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        candidatesList = data.map(cv => {
          let skillsArr = [];
          if (Array.isArray(cv.skills)) {
            skillsArr = cv.skills;
          } else if (typeof cv.skills === 'string') {
            skillsArr = cv.skills.split(',').map(s => s.trim()).filter(Boolean);
          }
          
          let certsArr = [];
          if (cv.certificates) {
            try {
              certsArr = typeof cv.certificates === 'string' ? JSON.parse(cv.certificates) : cv.certificates;
            } catch (e) {
              console.error("Failed to parse certificates:", e);
            }
          }
          
          return {
            id: cv.id,
            name: cv.name,
            email: cv.email,
            major: cv.major,
            university: cv.university,
            gpa: parseFloat(cv.gpa) || 0.0,
            skills: skillsArr,
            languages: cv.languages || "English",
            bio: cv.bio || "",
            avatar: cv.avatar ? `data:image/png;base64,${cv.avatar}` : "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=150&auto=format&fit=crop",
            certificates: certsArr
          };
        });
      }
    }
  } catch (e) {
    console.error("Failed to fetch CVs from backend:", e);
  }
}

export async function initCvsView() {
  populateRecruiterJobsDropdown();
  await fetchCvs();
  renderCvs();
  
  const majorCheckboxes = document.querySelectorAll('input[name="filter-major"]');
  majorCheckboxes.forEach(cb => {
    cb.addEventListener('change', () => {
      activeCvFilter.majors = Array.from(majorCheckboxes)
        .filter(c => c.checked)
        .map(c => c.value);
      renderCvs();
    });
  });

  const skillInput = document.getElementById('filter-cv-skills');
  if (skillInput) {
    skillInput.addEventListener('input', (e) => {
      activeCvFilter.skillQuery = e.target.value.toLowerCase().trim();
      renderCvs();
    });
  }
}

export async function syncDesktopData() {
  const syncBtn = document.getElementById('desktop-sync-btn');
  const syncIcon = document.getElementById('desktop-sync-icon');
  if (!syncIcon || !syncBtn) return;

  syncIcon.classList.add('animate-spin');
  syncBtn.disabled = true;

  showToast(
    STATE.lang === 'vi'
      ? "Đang đồng bộ hồ sơ CV ứng viên trực tuyến..."
      : "Syncing candidate CV profiles online...",
    "info"
  );

  try {
    await fetchCvs();
    showToast(
      STATE.lang === 'vi'
        ? `Đồng bộ thành công! Đã tải ${candidatesList.length || 3} CV sinh viên từ server.`
        : `Sync completed! Loaded ${candidatesList.length || 3} student CVs from backend server.`
    );
  } catch (e) {
    showToast("Sync failed. Check backend status.", "error");
  } finally {
    syncIcon.classList.remove('animate-spin');
    syncBtn.disabled = false;
    renderCvs();
  }
}

export function populateRecruiterJobsDropdown() {
  const selector = document.getElementById('cv-job-selector');
  if (!selector) return;

  const placeholder = selector.firstElementChild;
  selector.innerHTML = "";
  if (placeholder) selector.appendChild(placeholder);

  if (!STATE.user.isLoggedIn || !STATE.user.email) return;

  const myJobs = STATE.jobs.filter(j => j.posted_by === STATE.user.email);
  myJobs.forEach(job => {
    const opt = document.createElement('option');
    opt.value = job.id;
    opt.innerText = `${job.title} (${job.company})`;
    selector.appendChild(opt);
  });
}

export function handleCvGpaSliderInput(val) {
  activeCvFilter.gpa = parseFloat(val) || 0.0;
  const valEl = document.getElementById('cv-gpa-val');
  if (valEl) {
    valEl.innerText = activeCvFilter.gpa === 0.0 ? "0.0 (Any)" : activeCvFilter.gpa.toFixed(1);
  }
  renderCvs();
}

export function clearCvFilters() {
  activeCvFilter = {
    gpa: 0.0,
    majors: ["CNTT", "ATTT", "KHDL"],
    skillQuery: ""
  };
  
  lastEvaluatedCvs = [];
  const selector = document.getElementById('cv-job-selector');
  if (selector) selector.value = "";
  handleJobRecommendationChange("");
  
  const gpaSlider = document.getElementById('filter-cv-gpa');
  if (gpaSlider) gpaSlider.value = 0.0;
  
  const valEl = document.getElementById('cv-gpa-val');
  if (valEl) valEl.innerText = "0.0 (Any)";
  
  const checkboxes = document.querySelectorAll('input[name="filter-major"]');
  checkboxes.forEach(cb => cb.checked = true);
  
  const skillInput = document.getElementById('filter-cv-skills');
  if (skillInput) skillInput.value = "";

  renderCvs();
}

export function handleJobRecommendationChange(jobId) {
  const job = STATE.jobs.find(j => j.id == jobId);
  const reqPanel = document.getElementById('selected-job-reqs');
  
  if (!job) {
    if (reqPanel) reqPanel.classList.add('hidden');
    return;
  }

  if (reqPanel) reqPanel.classList.remove('hidden');

  const gpaVal = document.getElementById('req-gpa-val');
  const langVal = document.getElementById('req-lang-val');
  const skillsVal = document.getElementById('req-skills-val');

  if (gpaVal) gpaVal.innerText = job.gpa || "Không yêu cầu";
  if (langVal) langVal.innerText = job.languages || "Không yêu cầu";
  
  if (skillsVal) {
    skillsVal.innerText = job.tags && job.tags.length > 0 ? job.tags.join(', ') : "Không yêu cầu";
  }
}

export function runAiMatching() {
  const jobId = document.getElementById('cv-job-selector').value;
  if (!jobId) {
    showToast(STATE.lang === 'vi' ? "Vui lòng chọn một tin tuyển dụng để đối sánh AI!" : "Please select a job listing for AI matching!", "error");
    return;
  }

  const grid = document.getElementById('cv-grid-container');
  if (!grid) return;

  grid.innerHTML = `
    <div class="col-span-full py-16 flex flex-col items-center justify-center text-center">
      <div class="relative w-16 h-16 mb-4">
        <div class="absolute inset-0 rounded-full border-4 border-cyan-500/10 border-t-cyan-400 animate-spin"></div>
        <div class="absolute inset-2 rounded-full border-4 border-blue-500/10 border-b-blue-400 animate-spin" style="animation-direction: reverse; animation-duration: 1s;"></div>
        <i data-lucide="sparkles" class="absolute inset-0 m-auto w-6 h-6 text-cyan-400 animate-pulse"></i>
      </div>
      <p class="text-sm font-bold text-cyan-400 uppercase tracking-widest animate-pulse">AI Agent Matching Candidates...</p>
      <p class="text-xs text-slate-500 mt-1.5 max-w-sm">Đang tải và so sánh tiêu chuẩn kỹ năng, học bạ GPA, ngoại ngữ và dự án từ cơ sở dữ liệu Desktop client...</p>
    </div>
  `;
  if (window.lucide) window.lucide.createIcons();

  setTimeout(() => {
    calculateAndRenderMatchingCvs(jobId);
    showToast(STATE.lang === 'vi' ? "Đã đối sánh AI và đề xuất ứng viên tốt nhất!" : "AI matching completed! Best candidates recommended.");
  }, 1200);
}

function calculateAndRenderMatchingCvs(jobId) {
  const job = STATE.jobs.find(j => j.id == jobId);
  if (!job) return;

  const source = candidatesList.length > 0 ? candidatesList : MOCK_CVS;

  const evaluatedCvs = source.map(cv => {
    let score = 55;
    let gpaCheck = { status: "met", desc: "" };
    let skillsCheck = { status: "failed", desc: "" };
    let langCheck = { status: "met", desc: "" };

    if (job.gpa) {
      const jobGpa = parseFloat(job.gpa.match(/[\d\.]+/));
      if (!isNaN(jobGpa)) {
        if (cv.gpa >= jobGpa) {
          score += 15;
          gpaCheck = {
            status: "met",
            desc: STATE.lang === 'vi'
              ? `Điểm GPA thực tế (${cv.gpa.toFixed(2)}) đạt yêu cầu tuyển dụng (>= ${jobGpa.toFixed(1)})`
              : `Actual GPA (${cv.gpa.toFixed(2)}) satisfies the job criteria (>= ${jobGpa.toFixed(1)})`
          };
        } else if (cv.gpa >= jobGpa - 0.3) {
          score += 8;
          gpaCheck = {
            status: "warning",
            desc: STATE.lang === 'vi'
              ? `GPA thực tế (${cv.gpa.toFixed(2)}) hơi thấp so với yêu cầu (${jobGpa.toFixed(1)}) nhưng vẫn trong ngưỡng cân cân nhắc`
              : `Actual GPA (${cv.gpa.toFixed(2)}) is slightly lower than requested (${jobGpa.toFixed(1)}) but acceptable`
          };
        } else {
          gpaCheck = {
            status: "failed",
            desc: STATE.lang === 'vi'
              ? `GPA thực tế (${cv.gpa.toFixed(2)}) chưa đạt yêu cầu tối thiểu (${jobGpa.toFixed(1)})`
              : `Actual GPA (${cv.gpa.toFixed(2)}) does not meet the minimum requirement (${jobGpa.toFixed(1)})`
          };
        }
      }
    } else {
      score += 10;
      gpaCheck = {
        status: "met",
        desc: STATE.lang === 'vi' ? "Tin tuyển dụng này không yêu cầu GPA tối thiểu" : "This job listing does not require a minimum GPA"
      };
    }

    const matchedSkills = cv.skills.filter(s => {
      const isTag = job.tags ? job.tags.some(t => t.toLowerCase() === s.toLowerCase()) : false;
      const isInDesc = job.description ? job.description.toLowerCase().includes(s.toLowerCase()) : false;
      return isTag || isInDesc;
    });

    if (matchedSkills.length > 0) {
      score += Math.min(25, matchedSkills.length * 8);
      skillsCheck = {
        status: "met",
        desc: STATE.lang === 'vi'
          ? `Trùng khớp ${matchedSkills.length} kỹ năng yêu cầu: ${matchedSkills.join(', ')}`
          : `Matches ${matchedSkills.length} requested skills: ${matchedSkills.join(', ')}`
      };
    } else {
      skillsCheck = {
        status: "failed",
        desc: STATE.lang === 'vi'
          ? "Chưa phát hiện kỹ năng cốt lõi nào trùng khớp trực tiếp"
          : "No matching core technical skills found"
      };
    }

    if (job.languages) {
      const hasEnglish = job.languages.toLowerCase().includes('anh') || job.languages.toLowerCase().includes('english') || job.languages.toLowerCase().includes('ielts') || job.languages.toLowerCase().includes('toeic');
      if (hasEnglish) {
        if (cv.languages.toLowerCase().includes('anh') || cv.languages.toLowerCase().includes('ielts') || cv.languages.toLowerCase().includes('toeic')) {
          score += 10;
          langCheck = {
            status: "met",
            desc: STATE.lang === 'vi'
              ? `Chứng chỉ ngoại ngữ (${cv.languages}) đạt tiêu chuẩn tin tuyển dụng`
              : `Language certification (${cv.languages}) matches requirements`
          };
        } else {
          langCheck = {
            status: "failed",
            desc: STATE.lang === 'vi'
              ? `Yêu cầu chứng chỉ ngoại ngữ nhưng thông tin CV chưa tương thích`
              : `Language certification required, candidate profile mismatch`
          };
        }
      } else {
        score += 5;
        langCheck = {
          status: "met",
          desc: STATE.lang === 'vi' ? "Tin tuyển dụng không yêu cầu kỹ năng ngoại ngữ cụ thể" : "This job listing does not specify a language requirement"
        };
      }
    } else {
      score += 5;
      langCheck = {
        status: "met",
        desc: STATE.lang === 'vi' ? "Không có yêu cầu ngoại ngữ bắt buộc" : "No mandatory foreign language requirement"
      };
    }

    score = Math.min(99, score);

    let verdict = "";
    if (score >= 85) {
      verdict = STATE.lang === 'vi'
        ? "Ứng viên cực kỳ tiềm năng! Các kỹ năng cốt lõi và GPA tương thích hoàn hảo. Rất khuyến nghị tiến hành liên hệ phỏng vấn trực tiếp."
        : "Highly promising candidate! Core technical skills and GPA align perfectly. Highly recommended to schedule a direct interview.";
    } else if (score >= 70) {
      verdict = STATE.lang === 'vi'
        ? "Ứng viên khá phù hợp. Có kiến thức nền tảng tốt và đáp ứng hầu hết tiêu chí tuyển dụng. Nên xem xét tuyển dụng thử thách."
        : "A solid match. Good technical foundation and meets most recruitment criteria. Recommended to contact for evaluation.";
    } else {
      verdict = STATE.lang === 'vi'
        ? "Độ tương thích trung bình. Cần đào tạo thêm hoặc kiểm tra kỹ hơn về các mảng kỹ năng còn thiếu thông qua bài test kỹ thuật."
        : "Average compatibility. Candidate may need training or closer evaluation on missing skillsets via technical tests.";
    }

    return {
      ...cv,
      matchScore: score,
      gpaCheck,
      skillsCheck,
      langCheck,
      verdict
    };
  });

  evaluatedCvs.sort((a, b) => b.matchScore - a.matchScore);
  lastEvaluatedCvs = evaluatedCvs;
  renderCvsList(evaluatedCvs, true);
}

export function renderCvs() {
  const source = candidatesList.length > 0 ? candidatesList : MOCK_CVS;
  const filtered = source.filter(cv => {
    if (cv.gpa < activeCvFilter.gpa) return false;
    if (!activeCvFilter.majors.includes(cv.major)) return false;

    if (activeCvFilter.skillQuery) {
      const query = activeCvFilter.skillQuery;
      const matchSkill = cv.skills.some(s => s.toLowerCase().includes(query));
      const matchName = cv.name.toLowerCase().includes(query);
      const matchUniv = cv.university.toLowerCase().includes(query);
      if (!matchSkill && !matchName && !matchUniv) return false;
    }

    return true;
  });

  renderCvsList(filtered, false);
}

function renderCvsList(cvs, isAiSorted) {
  const container = document.getElementById('cv-grid-container');
  const countBadge = document.getElementById('cv-count-badge');
  if (!container) return;

  if (countBadge) {
    countBadge.innerText = `${cvs.length} ${cvs.length === 1 ? 'CV' : 'CVs'}`;
  }

  if (cvs.length === 0) {
    container.innerHTML = `
      <div class="col-span-full py-12 flex flex-col items-center justify-center text-slate-500">
        <i data-lucide="inbox" class="w-10 h-10 text-slate-600 mb-2"></i>
        <p class="text-sm font-semibold">${STATE.lang === 'vi' ? 'Không tìm thấy CV sinh viên phù hợp.' : 'No matching student CVs found.'}</p>
        <button onclick="clearCvFilters()" class="text-xs text-cyan-400 mt-2 font-bold hover:underline">Reset Filters</button>
      </div>
    `;
    if (window.lucide) window.lucide.createIcons();
    return;
  }

  container.innerHTML = cvs.map(cv => {
    const skillsHtml = cv.skills.map(s => `<span class="bg-slate-900/65 text-slate-300 text-[10px] font-semibold px-2 py-0.5 rounded-md border border-slate-800/80">${s}</span>`).join('');
    const matchScoreHtml = isAiSorted 
      ? `<div class="absolute top-4 right-4 flex items-center gap-1 text-[10px] font-bold text-cyan-400 bg-cyan-950/80 border border-cyan-500/30 px-2.5 py-1 rounded-full shadow-glow-cyan animate-pulse">
           <i data-lucide="sparkles" class="w-3 h-3"></i> ${cv.matchScore}% Match
         </div>`
      : '';

    const viewDetailsLabel = STATE.lang === 'vi' ? 'Xem CV Chi tiết' : 'View CV Details';
    const contactLabel = STATE.lang === 'vi' ? 'Tuyển dụng' : 'Contact';

    return `
      <article class="glass-card rounded-3xl p-5 shadow-md border border-slate-800/60 flex flex-col justify-between transition-all duration-300 hover:-translate-y-1.5 hover:shadow-glow-cyan hover:border-cyan-500/30 group relative">
        ${matchScoreHtml}
        <div>
          <div class="flex items-center gap-3.5 mb-4">
            <img src="${cv.avatar}" class="w-12 h-12 rounded-2xl object-cover shrink-0 border border-cyan-500/20">
            <div>
              <h3 class="text-sm font-bold text-white group-hover:text-cyan-400 transition-colors duration-200">${cv.name}</h3>
              <p class="text-xs text-slate-400 font-semibold">${cv.university}</p>
              <p class="text-[10px] text-cyan-400 font-bold uppercase tracking-wider mt-0.5">${cv.major} ✦ GPA: ${cv.gpa.toFixed(2)}</p>
            </div>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed mb-4 line-clamp-3">${cv.bio}</p>
          
          <div class="flex flex-wrap gap-1.5 mb-2">
            ${skillsHtml}
          </div>
        </div>

        <div class="mt-5 pt-3.5 border-t border-slate-800/40 flex justify-between items-center gap-3">
          <button onclick="openCvDetail(${cv.id})" class="rounded-xl border border-slate-800/80 bg-slate-900/10 hover:bg-cyan-500/5 hover:border-cyan-500/20 text-slate-300 hover:text-cyan-400 text-xs font-bold px-3.5 py-2 transition-all duration-200 flex-1">
            ${viewDetailsLabel}
          </button>
          <button onclick="contactCandidate('${cv.name}')" class="rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 text-xs font-bold px-4 py-2 transition-all duration-200">
            ${contactLabel}
          </button>
        </div>
      </article>
    `;
  }).join('');

  if (window.lucide) window.lucide.createIcons();
}

export function openCvDetail(cvId) {
  const source = candidatesList.length > 0 ? candidatesList : MOCK_CVS;
  const cv = source.find(c => c.id === cvId);
  if (!cv) return;

  const evaluatedCv = lastEvaluatedCvs.find(c => c.id === cvId);

  const avatarImg = document.getElementById('cv-modal-avatar');
  if (avatarImg) avatarImg.src = cv.avatar;

  const modalName = document.getElementById('cv-modal-name');
  if (modalName) modalName.innerText = cv.name;

  const modalMajorGpa = document.getElementById('cv-modal-major-gpa');
  if (modalMajorGpa) {
    modalMajorGpa.innerText = `${cv.major} ✦ GPA: ${cv.gpa.toFixed(2)}`;
  }

  const modalUniv = document.getElementById('cv-modal-univ');
  if (modalUniv) modalUniv.innerText = cv.university;

  const modalLanguages = document.getElementById('cv-modal-languages');
  if (modalLanguages) modalLanguages.innerText = cv.languages;

  const modalBio = document.getElementById('cv-modal-bio');
  if (modalBio) modalBio.innerText = cv.bio;

  const skillsContainer = document.getElementById('cv-modal-skills-container');
  if (skillsContainer) {
    skillsContainer.innerHTML = cv.skills.map(s => 
      `<span class="bg-slate-900/65 text-slate-300 text-[10px] font-semibold px-2 py-0.5 rounded-md border border-slate-800/80">${s}</span>`
    ).join('');
  }

  // Populate Certificates
  const certsContainer = document.getElementById('cv-modal-certs-container');
  if (certsContainer) {
    if (cv.certificates && cv.certificates.length > 0) {
      certsContainer.innerHTML = cv.certificates.map(c => {
        const imgHtml = c.image_base64 
          ? `<img src="data:image/png;base64,${c.image_base64}" class="w-12 h-8 rounded object-cover border border-slate-800 cursor-pointer" onclick="window.open(this.src)" title="Xem chứng chỉ cỡ lớn">`
          : '';
        return `
          <div class="flex items-center justify-between p-2 rounded-xl bg-slate-900/50 border border-slate-800/80">
            <div>
              <p class="text-xs font-bold text-slate-200">${c.name}</p>
              <p class="text-[10px] text-slate-500 font-semibold">${c.year}</p>
            </div>
            ${imgHtml}
          </div>
        `;
      }).join('');
    } else {
      certsContainer.innerHTML = `<p class="text-[11px] text-slate-500 italic">Chưa có chứng chỉ.</p>`;
    }
  }

  const aiActive = document.getElementById('cv-modal-ai-active');
  const aiInactive = document.getElementById('cv-modal-ai-inactive');

  if (evaluatedCv) {
    if (aiActive) aiActive.classList.remove('hidden');
    if (aiInactive) aiInactive.classList.add('hidden');

    const scoreEl = document.getElementById('cv-modal-ai-score');
    if (scoreEl) scoreEl.innerText = `${evaluatedCv.matchScore}% Match`;

    const progressEl = document.getElementById('cv-modal-ai-progress');
    if (progressEl) progressEl.style.width = `${evaluatedCv.matchScore}%`;

    const getCheckIconHtml = (status) => {
      if (status === 'met') {
        return `<i data-lucide="check-circle" class="w-4 h-4 text-emerald-400"></i>`;
      } else if (status === 'warning') {
        return `<i data-lucide="alert-circle" class="w-4 h-4 text-yellow-400"></i>`;
      } else {
        return `<i data-lucide="x-circle" class="w-4 h-4 text-red-400"></i>`;
      }
    };

    const gpaIcon = document.getElementById('cv-modal-gpa-check-icon');
    if (gpaIcon) {
      gpaIcon.innerHTML = getCheckIconHtml(evaluatedCv.gpaCheck.status);
    }
    const gpaDesc = document.getElementById('cv-modal-gpa-check-desc');
    if (gpaDesc) gpaDesc.innerText = evaluatedCv.gpaCheck.desc;

    const skillsIcon = document.getElementById('cv-modal-skills-check-icon');
    if (skillsIcon) {
      skillsIcon.innerHTML = getCheckIconHtml(evaluatedCv.skillsCheck.status);
    }
    const skillsDesc = document.getElementById('cv-modal-skills-check-desc');
    if (skillsDesc) skillsDesc.innerText = evaluatedCv.skillsCheck.desc;

    const langIcon = document.getElementById('cv-modal-lang-check-icon');
    if (langIcon) {
      langIcon.innerHTML = getCheckIconHtml(evaluatedCv.langCheck.status);
    }
    const langDesc = document.getElementById('cv-modal-lang-check-desc');
    if (langDesc) langDesc.innerText = evaluatedCv.langCheck.desc;

    const verdictEl = document.getElementById('cv-modal-ai-verdict');
    if (verdictEl) verdictEl.innerText = evaluatedCv.verdict;

  } else {
    if (aiActive) aiActive.classList.add('hidden');
    if (aiInactive) aiInactive.classList.remove('hidden');
  }

  const modal = document.getElementById('cv-detail-modal');
  if (modal) modal.classList.remove('hidden');
  if (window.lucide) window.lucide.createIcons();
}

export function closeCvDetail() {
  const modal = document.getElementById('cv-detail-modal');
  if (modal) modal.classList.add('hidden');
}

export function contactCandidate(name) {
  switchTab('chat');
  
  const chatInput = document.getElementById('chat-input');
  if (chatInput) {
    chatInput.value = STATE.lang === 'vi' 
      ? `Chào ${name}, mình liên hệ từ phía doanh nghiệp khi xem CV của bạn trên hệ thống...`
      : `Hi ${name}, I am contacting you on behalf of our company after reviewing your CV...`;
  }
}

export function toggleCvSidebar() {
  const sidebar = document.getElementById('cv-filter-sidebar');
  const btnText = document.getElementById('cv-toggle-filter-text');
  const btnIcon = document.getElementById('cv-toggle-filter-icon');
  if (!sidebar) return;

  const isCollapsed = sidebar.classList.contains('collapsed');
  if (isCollapsed) {
    sidebar.classList.remove('collapsed');
    if (btnText) btnText.setAttribute('data-i18n', 'cv_hide_filters');
    if (btnIcon) btnIcon.setAttribute('data-lucide', 'sliders');
  } else {
    sidebar.classList.add('collapsed');
    if (btnText) btnText.setAttribute('data-i18n', 'cv_show_filters');
    if (btnIcon) btnIcon.setAttribute('data-lucide', 'sliders-horizontal');
  }

  if (window.updateLanguageUI) window.updateLanguageUI();
  if (window.lucide) window.lucide.createIcons();
}

window.handleCvGpaSliderInput = handleCvGpaSliderInput;
window.clearCvFilters = clearCvFilters;
window.handleJobRecommendationChange = handleJobRecommendationChange;
window.runAiMatching = runAiMatching;
window.openCvDetail = openCvDetail;
window.closeCvDetail = closeCvDetail;
window.syncDesktopData = syncDesktopData;
window.renderCvs = renderCvs;
window.toggleCvSidebar = toggleCvSidebar;
window.contactCandidate = contactCandidate;
window.initCvsView = initCvsView;
