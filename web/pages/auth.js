/**
 * AI-Career Bridge - Authentication Module
 * Handles Recruiter Login, Registration, Password matching, and logout.
 */

import { STATE, BASE_URL, showToast, switchTab, syncAuthNav } from '../app.js';
import { loadJobsFromBackend } from './jobs.js';
import { renderProfile } from './profile.js';
import { chatSocket, initWebSocket } from './chat.js';

export async function handleLoginSubmit(event) {
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

        let avatarUrl = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=256&auto=format&fit=crop";
        if (result.user.bio) {
          try {
            const parsed = JSON.parse(result.user.bio);
            if (parsed.avatar) avatarUrl = parsed.avatar;
          } catch (e) {}
        }
        STATE.user.avatar = avatarUrl;

        localStorage.setItem('user', JSON.stringify(STATE.user));
        
        // Reconnect WebSocket with email parameter
        if (chatSocket) {
          try { chatSocket.close(); } catch(e){}
        } else {
          initWebSocket();
        }
        
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

export async function handleRegisterSubmit(event) {
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
        
        let avatarUrl = "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=256&auto=format&fit=crop";
        if (result.user.bio) {
          try {
            const parsed = JSON.parse(result.user.bio);
            if (parsed.avatar) avatarUrl = parsed.avatar;
          } catch (e) {}
        }
        STATE.user.avatar = avatarUrl;

        localStorage.setItem('user', JSON.stringify(STATE.user));
        
        // Reconnect WebSocket with email parameter
        if (chatSocket) {
          try { chatSocket.close(); } catch(e){}
        } else {
          initWebSocket();
        }
        
        renderProfile();
        syncAuthNav();
        renderJobs();
        showToast(`Welcome to AI-Career Bridge, ${name}! Your Recruiter Portal account has been set up.`);
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

export function validatePasswords() {
  const pass = document.getElementById('reg-pass').value;
  const confirm = document.getElementById('reg-confirm').value;
  const errorText = document.getElementById('password-match-error');

  if (!errorText) return;

  if (confirm && pass !== confirm) {
    errorText.classList.remove('hidden');
  } else {
    errorText.classList.add('hidden');
  }
}

export function logout() {
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
  
  // Reconnect WebSocket in Guest mode (no email)
  if (chatSocket) {
    try { chatSocket.close(); } catch(e){}
  } else {
    initWebSocket();
  }
  
  syncAuthNav();
  renderJobs();
  showToast("Signed out successfully.");
  switchTab('jobs');
}

// Bind to window for HTML inline access
window.handleLoginSubmit = handleLoginSubmit;
window.handleRegisterSubmit = handleRegisterSubmit;
window.validatePasswords = validatePasswords;
window.logout = logout;
