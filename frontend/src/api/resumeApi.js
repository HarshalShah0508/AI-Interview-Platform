import apiClient from "./client";

export const uploadResume = async (file, token) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await apiClient.post("/resume/upload", formData, {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const getResumes = async (token) => {
  const response = await apiClient.get("/resume", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};