import { API_BASE_URL } from "./config.js";

export async function fetchReports() {
  const response = await fetch(`${API_BASE_URL}/reports`);
  const data = await response.json();

  if (!response.ok) {
    throw new Error("Failed to load reports");
  }

  return data;
}

export async function uploadReport({ file, latitude, longitude }) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("latitude", latitude);
  formData.append("longitude", longitude);

  const response = await fetch(`${API_BASE_URL}/detect`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message || "Request failed");
  }

  return data;
}
