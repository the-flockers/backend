/**
 * api.js — drop this into your frontend at src/services/api.js
 *
 * Vite proxies /api/* → http://localhost:5000 in dev (see vite.config.js).
 * In production, set VITE_API_BASE to your backend URL.
 */
const BASE = import.meta.env.VITE_API_BASE ?? ""

async function get(path, params = {}) {
  const url = new URL(`${BASE}/api/v1${path}`, window.location.origin)
  Object.entries(params).forEach(([k, v]) => v != null && url.searchParams.set(k, v))

  const res = await fetch(url)
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.message ?? `Request failed: ${res.status}`)
  }
  const json = await res.json()
  return json.data
}

export const api = {
  // News
  getNews: (page = 1, perPage = 10) =>
    get("/news", { page, per_page: perPage }),
  getNewsArticle: (id) =>
    get(`/news/${id}`),

  // Learn
  getLearnArticles: (category = null) =>
    get("/learn", { category }),
  getLearnArticle: (slug) =>
    get(`/learn/${slug}`),
  getLearnCategories: () =>
    get("/learn/categories"),

  // Get Involved
  getInvolvement: (type = null) =>
    get("/get-involved", { type }),
  getInvolvementItem: (id) =>
    get(`/get-involved/${id}`),
}
