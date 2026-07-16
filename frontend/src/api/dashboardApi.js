import apiClient from "./client";

export const getDashboard = async (token) => {
  const response = await apiClient.get("/dashboard", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};