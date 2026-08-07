import apiClient from "./client";

export async function runCode(data, token) {
  const response = await apiClient.post(
    "/code/run",
    data,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
}