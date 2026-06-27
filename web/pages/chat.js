/**
 * AI-Career Bridge - Chat & Notification Module
 * Handles WebSockets, Chat messages, and Recruiters Notifications when students apply.
 */

import { STATE, BASE_URL, showToast, switchTab } from '../app.js';
import { loadApplicantsFromBackend } from './applicants.js';

export let chatSocket = null;
export let notificationHistory = [];

export function toggleNotificationDropdown() {
  const dropdown = document.getElementById('notification-dropdown');
  if (dropdown) {
    dropdown.classList.toggle('hidden');
  }
}

export function addNotification(message, applicant = null) {
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

export function updateNotificationUI() {
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

export function handleNotificationClick(idx) {
  const item = notificationHistory[idx];
  if (item && item.applicant) {
    showApplicantDetails(item.applicant);
  }
}

export function clearNotifications() {
  notificationHistory = [];
  updateNotificationUI();
}

export async function loadNotificationsFromBackend() {
  try {
    const emailParam = STATE.user && STATE.user.isLoggedIn && STATE.user.email ? `?email=${encodeURIComponent(STATE.user.email)}` : '';
    const response = await fetch(`${BASE_URL}/notifications${emailParam}`);
    if (response.ok) {
      const data = await response.json();
      notificationHistory = data;
      updateNotificationUI();
    }
  } catch (error) {
    console.error("Failed to load notifications from backend:", error);
  }
}

export function initWebSocket() {
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
  
  const emailParam = STATE.user && STATE.user.isLoggedIn && STATE.user.email ? `?email=${encodeURIComponent(STATE.user.email)}` : '';
  const wsUrl = `${wsProtocol}://${wsHost}/ws${emailParam}`;
  
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
        // Feature 5 optimization: filter notification in client-side or server-side.
        // For absolute robustness, if the job has posted_by === recruiter's email, show toast!
        // We can inspect if data.applicant has job details.
        const isMyJob = !STATE.user.isLoggedIn || !data.applicant || data.applicant.job_company.toLowerCase() === STATE.user.name.toLowerCase();
        
        if (isMyJob) {
          showToast(data.message, 'success', data.applicant);
          addNotification(data.message, data.applicant);
        }
        
        // Refresh applicants table dynamically
        if (STATE.activeTab === 'applicants') {
          loadApplicantsFromBackend();
        }
      } else if (data.type === 'chat') {
        appendChatMessage(data);
      } else if (data.type === 'status_update' || data.type === 'job_status_update') {
        // Trigger page refresh if on active viewing
        if (STATE.activeTab === 'applicants') {
          loadApplicantsFromBackend();
        }
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

export function appendChatMessage(data) {
  const chatMessages = document.getElementById('chat-messages');
  if (!chatMessages) return;

  const isMe = STATE.user.isLoggedIn && data.username === STATE.user.name;
  const username = data.username || "Ẩn danh";
  const initials = username.charAt(0).toUpperCase();

  const messageHtml = isMe ? `
    <div class="flex items-start gap-2.5 max-w-lg ml-auto justify-end animate-fade-in">
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
    <div class="flex items-start gap-2.5 max-w-lg animate-fade-in">
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

export function handleChatSubmit(event) {
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

export function escapeHTML(str) {
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

export function showApplicantDetails(applicant) {
  if (!applicant) return;
  
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
  
  const initials = (applicant.name || "U").charAt(0).toUpperCase();
  document.getElementById('applicant-modal-avatar').innerText = initials;
  
  const modal = document.getElementById('applicant-detail-modal');
  if (modal) {
    modal.classList.remove('hidden');
  }
  if (window.lucide) window.lucide.createIcons();
}

export function closeApplicantModal() {
  const modal = document.getElementById('applicant-detail-modal');
  if (modal) {
    modal.classList.add('hidden');
  }
}

// Bind to window for HTML inline access
window.toggleNotificationDropdown = toggleNotificationDropdown;
window.handleNotificationClick = handleNotificationClick;
window.clearNotifications = clearNotifications;
window.handleChatSubmit = handleChatSubmit;
window.showApplicantDetails = showApplicantDetails;
window.closeApplicantModal = closeApplicantModal;
window.initWebSocket = initWebSocket;
window.loadNotificationsFromBackend = loadNotificationsFromBackend;
