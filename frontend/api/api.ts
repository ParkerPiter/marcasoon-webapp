import { CardPrice, SearchCard } from "../src/app/interfaces/card";
import { SubmitPayload } from "../src/app/interfaces/inputs";
/**
 * GET directo al Admin (HTML). Requiere estar logueado en Django y que CORS permita la petición.
 * Devuelve el HTML de la página del admin.
 */
export async function getPlansFromAdminHTML(
  url = "http://localhost:8000/admin/core/plan/"
): Promise<string> {
  const res = await fetch(url, {
    method: "GET",
    credentials: "include", // envía cookies de sesión del admin
    headers: {
      Accept: "text/html,application/xhtml+xml",
    },
    // mode: "cors" // opcional en navegador
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Admin GET failed (${res.status}): ${text || res.statusText}`);
  }
  return res.text();
}

/**
 * GET recomendado a un endpoint REST que devuelva JSON de planes.
 * Cambia la ruta por tu endpoint real (ej: /api/plans/).
 */
export async function getPlansAPI(
  url = "https://marcasoon-webapp.onrender.com/api/plans/",
  options?: RequestInit
): Promise<CardPrice[]> {
  const res = await fetch(url, {
    method: "GET",
    credentials: "include",
    headers: {
      Accept: "application/json",
    },
    ...(options || {}),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`API GET failed (${res.status}): ${text || res.statusText}`);
  }
  return res.json();
}

// Búsqueda de marcas por nombre (USPTO proxy en backend)
type TrademarkSearchItem = {
  logo?: string;
  liveOrDeadStatus?: "Live" | "Dead" | string;
  correspondenceName?: string;
  transactionDate?: string;
};

type TrademarkSearchResponse = {
  list?: TrademarkSearchItem[];
};

export async function searchTrademarksByName(
  name: string,
  baseUrl = "https://marcasoon-webapp.onrender.com/api/trademark/name-search/"
): Promise<SearchCard[]> {
  const url = `${baseUrl}?name=${encodeURIComponent(name)}`;
  const res = await fetch(url, {
    method: "GET",
    headers: { Accept: "application/json" },
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Trademark search failed (${res.status}): ${text || res.statusText}`);
  }
  const data: TrademarkSearchResponse = await res.json();
  const list = data?.list ?? [];
  // Map a nuestro tipo de tarjeta
  return list.map((item) => ({
    logo: item.logo || "",
    liveOrDeadStatus: (item.liveOrDeadStatus === "Live" ? "Live" : item.liveOrDeadStatus === "Dead" ? "Dead" : "Live") as "Live" | "Dead",
    correspondenceName: item.correspondenceName || "",
    transactionDate: item.transactionDate || "",
  }));
}

// Auth helpers
export async function checkAuthStatus(): Promise<boolean> {
  try {
    // 1) JWT via localStorage
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("access") || sessionStorage.getItem("access");
      if (token) {
        const r = await fetch("/api/auth/me/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (r.ok) return true;
      }
    }
    // 2) Session (DRF login) via cookies
    const r2 = await fetch("/api/auth/me/", { credentials: "include" });
    return r2.ok;
  } catch {
    return false;
  }
}

export async function getAuthLoginPage(): Promise<string> {
  const res = await fetch("/api/auth/login/", { credentials: "include" });
  if (!res.ok) throw new Error(`Login page failed (${res.status})`);
  return res.text();
}

// Registro de usuario (JSON)
export async function registerUserAPI(
  payload: SubmitPayload,
  url = "https://marcasoon-webapp.onrender.com/api/auth/register/"
): Promise<any> {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Register failed (${res.status}): ${text || res.statusText}`);
  }

  // Algunos serializers devuelven el usuario creado; otros 204 No Content.
  // Si no hay JSON válido, devolvemos un objeto vacío.
  try {
    return await res.json();
  } catch {
    return {};
  }
}

// ===== JWT Login & Token storage =====
export type LoginResponse = { access: string; refresh: string; [k: string]: any };

export async function loginJWT(
  creds: { username: string; password: string },
  url = "https://marcasoon-webapp.onrender.com/api/auth/token/"
): Promise<LoginResponse> {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ username: creds.username, password: creds.password }),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Login failed (${res.status}): ${text || res.statusText}`);
  }
  return res.json();
}

// Login simple (endpoint personalizado que puede devolver usuario o estado de sesión)
export async function loginBasic(
  creds: { username: string; password: string },
  url = "https://marcasoon-webapp.onrender.com/api/auth/login/"
): Promise<any> {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(creds),
    credentials: "include", // por si establece cookie de sesión
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Basic login failed (${res.status}): ${text || res.statusText}`);
  }
  try {
    return await res.json();
  } catch {
    return {}; // si el backend responde 204 ó sin JSON
  }
}

export function storeTokens(tokens: { access: string; refresh?: string }, persist: boolean = true) {
  const storage = persist ? localStorage : sessionStorage;
  storage.setItem("access", tokens.access);
  if (tokens.refresh) storage.setItem("refresh", tokens.refresh);
}

export function getStoredAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access") || sessionStorage.getItem("access");
}

export function clearStoredTokens() {
  if (typeof window === "undefined") return;
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  localStorage.removeItem("username");
  sessionStorage.removeItem("access");
  sessionStorage.removeItem("refresh");
}

export async function loginAndStoreToken(creds: { username: string; password: string }, persist: boolean = true) {
  const tokens = await loginJWT(creds);
  storeTokens(tokens, persist);
  return tokens;
}

// Obtener info del usuario autenticado
export async function fetchCurrentUser(
  url = "https://marcasoon-webapp.onrender.com/api/auth/me/",
  token?: string
): Promise<any> {
  const access = token || getStoredAccessToken();
  const res = await fetch(url, {
    method: "GET",
    headers: {
      Accept: "application/json",
      ...(access ? { Authorization: `Bearer ${access}` } : {}),
    },
    credentials: "include",
  });
  if (!res.ok) {
    throw new Error(`Me failed (${res.status})`);
  }
  return res.json();
}

// Logout opcional (si backend expone la ruta); siempre limpiamos tokens localmente
export async function logoutAll(
  url = "https://marcasoon-webapp.onrender.com/api/auth/logout"
) {
  try {
    await fetch(url, { method: "POST", credentials: "include" });
  } catch {}
  clearStoredTokens();
}

// Helpers para username en storage
export function setStoredUsername(username: string, persist: boolean = true) {
  try {
    const storage = persist ? localStorage : sessionStorage;
    storage.setItem("username", username);
  } catch {}
}

export function getStoredUsername(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("username") || sessionStorage.getItem("username");
}

// ===== Payments =====
export type StripeCheckoutResponse = { id: string; url: string };

export async function createStripeCheckoutSession(
  planId: number,
  url = "https://marcasoon-webapp.onrender.com/api/stripe/create-checkout-session/",
  token?: string
): Promise<StripeCheckoutResponse> {
  const access = token || getStoredAccessToken();
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      ...(access ? { Authorization: `Bearer ${access}` } : {}),
    },
    body: JSON.stringify({ plan_id: planId }),
    credentials: "include",
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Stripe session failed (${res.status}): ${text || res.statusText}`);
  }
  return res.json();
}

export type PaypalCreateOrderRequest = {
  plan_id: number;
  redirect: boolean;
  amount: number;
  currency: string;
};

export type PaypalCreateOrderResponse = {
  orderID: string;
  approveUrl: string;
};

export async function createPaypalOrder(
  payload: PaypalCreateOrderRequest,
  url = "https://marcasoon-webapp.onrender.com/api/paypal/create-order/",
  token?: string
): Promise<PaypalCreateOrderResponse> {
  const access = token || getStoredAccessToken();
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      ...(access ? { Authorization: `Bearer ${access}` } : {}),
    },
    body: JSON.stringify(payload),
    credentials: "include",
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`PayPal create-order failed (${res.status}): ${text || res.statusText}`);
  }
  return res.json();
}

// Obtener JWT con SimpleJWT
export async function obtainTokenPair(
  credentials: { username: string; password: string },
  url = "https://marcasoon-webapp.onrender.com/api/auth/token/"
): Promise<{ access: string; refresh: string }> {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(credentials),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Token obtain failed (${res.status}): ${text || res.statusText}`);
  }
  return res.json();
}

// Nota: `storeTokens` ya está definido arriba; se omite duplicado.