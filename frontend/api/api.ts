import { CardPrice, SearchCard } from "../src/app/interfaces/card";
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
  url = "https://marcasoon-webapp.onrender.com/api/plans",
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