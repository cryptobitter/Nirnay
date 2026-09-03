// Default to localhost if the environment variable is not set
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Module-level token storage so API calls can access it automatically.
// This is updated by the AuthContext when a user logs in or out.
let authToken = null;
export const setApiToken = (token) => {
  authToken = token;
};

/**
 * Core fetch wrapper that automatically handles headers, JSON serialization, 
 * multipart/form-data, and unified error throwing.
 */
async function apiCall(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  const headers = { ...options.headers };

  // Attach Authorization header if we have a token and it's not a public route
  const isPublicRoute = endpoint.startsWith('/auth/') || endpoint.startsWith('/verify/');
  if (authToken && !isPublicRoute) {
    headers['Authorization'] = `Bearer ${authToken}`;
  }

  // Handle JSON vs FormData
  if (options.body && !(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(options.body);
  }
  // Note: We intentionally DO NOT set Content-Type for FormData. 
  // The browser MUST set it automatically to include the correct multipart boundary.

  try {
    const response = await fetch(url, { ...options, headers });

    if (!response.ok) {
      let errorMessage = 'An unexpected error occurred.';
      try {
        const errorData = await response.json();
        // FastAPI uses "detail" for error messages by default
        errorMessage = errorData.detail || errorData.message || errorMessage;
      } catch (parseError) {
        // Fallback if the response isn't JSON
        errorMessage = await response.text();
      }
      
      throw { status: response.status, message: errorMessage };
    }

    return await response.json();
  } catch (error) {
    // If it's already our custom error object, rethrow it
    if (error.status) throw error;
    // Otherwise, it's a network/fetch error (e.g. server is down)
    throw { status: 0, message: 'Network error. Please check your connection to the backend.' };
  }
}

// --- Auth Endpoints ---

export async function signup(userData) {
  // userData: { email, password, name, role, institution_name }
  return apiCall('/auth/signup', {
    method: 'POST',
    body: userData,
  });
}

export async function login(email, password) {
  return apiCall('/auth/login', {
    method: 'POST',
    body: { email, password },
  });
}

// --- Document Endpoints ---

export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  return apiCall('/documents/upload', {
    method: 'POST',
    body: formData,
  });
}

export async function listDocuments() {
  return apiCall('/documents', {
    method: 'GET',
  });
}

// --- Q&A and History Endpoints ---

export async function askQuestion(question) {
  return apiCall('/qa/ask', {
    method: 'POST',
    body: { question },
  });
}

export async function getHistory() {
  return apiCall('/history', {
    method: 'GET',
  });
}

// --- Admin Endpoints ---

export async function getAuditLog() {
  return apiCall('/audit', {
    method: 'GET',
  });
}

// --- Public Endpoints ---

export async function verifyRecord(identifier) {
  return apiCall(`/verify/${identifier}`, {
    method: 'GET',
  });
}