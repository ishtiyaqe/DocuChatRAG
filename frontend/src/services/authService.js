
import api from "../utils/axiosConfig";

export async function registerUser(data) {
  const res = await api.post("/api/register/", data);
  return res.data;
}

export async function loginUser(data) {
  const res = await api.post("/api/login/", data);
  return res.data;
}

export async function logoutUser() {
  const res = await api.post("/api/logout/");
  return res.data;
}

export async function getCurrentUser() {
  const res = await api.get("/api/user/");
  return res.data;
}
