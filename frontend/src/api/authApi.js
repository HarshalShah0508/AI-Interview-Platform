import apiClient from "./client";

export const signup = async (userData) => {
  const response = await apiClient.post("/signup", userData);
  return response.data;
};

export const login = async ({ email, password }) => {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const response = await apiClient.post("/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  return response.data;
};

export const getMe = async (token) => {
  const response = await apiClient.get("/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};