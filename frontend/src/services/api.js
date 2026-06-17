const RAW_BASE = import.meta.env.VITE_API_BASE_URL || "";
const API_BASE = RAW_BASE.replace(/\/$/, "");
const ACCESS_KEY = "turkicgrammarai.access";
const REFRESH_KEY = "turkicgrammarai.refresh";

export function getAccessToken() {
  return window.localStorage.getItem(ACCESS_KEY) || "";
}

export function setAuthTokens(tokens) {
  if (tokens?.access) window.localStorage.setItem(ACCESS_KEY, tokens.access);
  if (tokens?.refresh) window.localStorage.setItem(REFRESH_KEY, tokens.refresh);
}

export function clearAuthTokens() {
  window.localStorage.removeItem(ACCESS_KEY);
  window.localStorage.removeItem(REFRESH_KEY);
}

async function refreshAccessToken() {
  const refresh = window.localStorage.getItem(REFRESH_KEY);
  if (!refresh) return "";
  const response = await fetch(`${API_BASE}/api/auth/refresh/`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ refresh }),
  });
  if (!response.ok) {
    clearAuthTokens();
    return "";
  }
  const tokens = await response.json();
  setAuthTokens(tokens);
  return tokens.access || "";
}

async function requestWithAuth(url, options = {}, retry = true) {
  const access = getAccessToken();
  const headers = {
    Accept: "application/json",
    ...(options.headers || {}),
    ...(access ? { Authorization: `Bearer ${access}` } : {}),
  };
  const response = await fetch(url, { ...options, headers });
  if (response.status === 401 && retry) {
    const refreshed = await refreshAccessToken();
    if (refreshed) return requestWithAuth(url, options, false);
  }
  return response;
}

export async function apiGet(path, params = {}) {
  const url = new URL(`${API_BASE}${path}`, window.location.origin);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.set(key, value);
    }
  });
  const response = await requestWithAuth(url.toString());
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with ${response.status}`);
  }
  return response.json();
}

export async function postJson(path, body = {}) {
  const response = await requestWithAuth(`${API_BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with ${response.status}`);
  }
  return response.json();
}

export async function login(email, password) {
  const response = await fetch(`${API_BASE}/api/auth/login/`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Login failed with ${response.status}`);
  }
  const tokens = await response.json();
  setAuthTokens(tokens);
  return tokens;
}

export async function register(payload) {
  const response = await fetch(`${API_BASE}/api/auth/register/`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Registration failed with ${response.status}`);
  }
  return response.json();
}

export async function getProfile() {
  return apiGet("/api/auth/profile/");
}
