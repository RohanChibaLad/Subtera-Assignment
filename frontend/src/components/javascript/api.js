import axios from "axios";

// Create an Axios instance with a base URL from environment variables or default to localhost
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

// Wrapper functions for common HTTP methods that return the response data directly
export const get  = (url, params) => api.get(url, { params }).then(r => r.data);
export const post = (url, body)  => api.post(url, body).then(r => r.data);
export const put  = (url, body) => api.put(url, body).then(r => r.data);
export const del  = (url) => api.delete(url).then(r => r.data);

// Endpoints (Should only need statistic ones))
// --- Author --- \\
export const Authors = {
  list: () => get("/authors"),
  create: (body) => post("/authors", body),
  update: (id, body) => put(`/authors/${id}`, body),
  remove: (id) => del(`/authors/${id}`),
};

// --- Book --- \\
export const Books = {
  list: (params) => get("/books"),
  create: (body) => post("/books", body),
  update: (id, body) => put(`/books/${id}`, body),
  remove: (id) => del(`/books/${id}`),
};

// --- Readers --- \\
export const Readers = {
  list: () => get("/readers"),
  create: (body) => post("/readers", body),
  update: (id, body) => put(`/readers/${id}`, body),
  remove: (id) => del(`/readers/${id}`),
};

// --- Statistics --- \\
export const Stats = {
  popularBooks: (limit=10) => get("/stats/popular-books",  { limit }),
  popularAuthors:(limit=10) => get("/stats/popular-authors",{ limit }),
  userTotal: () => get("/stats/user-total-books"),
  userTopAuthors:(limit=3)  => get("/stats/user-top-authors",{ limit }),
};