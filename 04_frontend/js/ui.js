import { formatTimestamp, truncateFileName } from "./formatters.js";

const statusBox = document.getElementById("statusMessage");
const statusPill = document.getElementById("statusPill");
const uploadButton = document.getElementById("uploadButton");
const previewCard = document.getElementById("previewCard");
const imagePreview = document.getElementById("imagePreview");
const fileName = document.getElementById("fileName");
const fileMeta = document.getElementById("fileMeta");
const recentReports = document.getElementById("recentReports");

const totalReports = document.getElementById("totalReports");
const verifiedReports = document.getElementById("verifiedReports");
const fixedReports = document.getElementById("fixedReports");
const openReports = document.getElementById("openReports");

export function setStatus(message, state = "idle") {
  statusBox.textContent = message;
  statusPill.textContent = state.charAt(0).toUpperCase() + state.slice(1);
  statusPill.className = `status-pill ${state}`;
}

export function setUploading(isUploading) {
  uploadButton.disabled = isUploading;
  uploadButton.textContent = isUploading ? "Analyzing..." : "Report Pothole";
}

export function showPreview(file) {
  if (!file) {
    previewCard.classList.add("hidden");
    imagePreview.removeAttribute("src");
    fileName.textContent = "No file selected";
    fileMeta.textContent = "Waiting for upload";
    return;
  }

  previewCard.classList.remove("hidden");
  imagePreview.src = URL.createObjectURL(file);
  fileName.textContent = truncateFileName(file.name);
  fileMeta.textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB`;
}

export function updateStats(reports) {
  totalReports.textContent = reports.length;
  verifiedReports.textContent = reports.filter(report => report.verified).length;
  fixedReports.textContent = reports.filter(report => report.status === "fixed").length;
  openReports.textContent = reports.filter(report => report.status !== "fixed").length;
}

export function renderRecentReports(reports) {
  if (!reports.length) {
    recentReports.innerHTML = `<div class="recent-item"><strong>No reports yet</strong><span>Upload the first field image to start tracking potholes.</span></div>`;
    return;
  }

  recentReports.innerHTML = reports
    .slice()
    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
    .slice(0, 5)
    .map(report => `
      <div class="recent-item">
        <strong>${report.status === "fixed" ? "Fixed pothole" : "Active pothole"}</strong>
        <span>${formatTimestamp(report.timestamp)}</span>
        <span>${report.verified ? "Verified report" : "Awaiting verification"}</span>
      </div>
    `)
    .join("");
}
