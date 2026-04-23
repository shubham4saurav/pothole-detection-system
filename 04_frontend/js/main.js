import { fetchReports, uploadReport } from "./api.js";
import { renderReportsOnMap, showCurrentLocation } from "./map.js";
import { renderRecentReports, setStatus, setUploading, showPreview, updateStats } from "./ui.js";

const fileInput = document.getElementById("imageInput");
const uploadButton = document.getElementById("uploadButton");
const locateButton = document.getElementById("locateButton");

async function refreshDashboard(successMessage = null) {
  const reports = await fetchReports();
  renderReportsOnMap(reports);
  updateStats(reports);
  renderRecentReports(reports);

  if (successMessage) {
    setStatus(successMessage, "success");
  } else if (reports.length) {
    setStatus(`Loaded ${reports.length} pothole reports across the dashboard.`, "idle");
  } else {
    setStatus("No saved pothole reports yet. Upload the first one to begin.", "idle");
  }
}

async function handleUpload() {
  const file = fileInput.files[0];
  if (!file) {
    setStatus("Please select an image before uploading.", "error");
    return;
  }

  setUploading(true);
  setStatus("Requesting location and analyzing the uploaded image...", "loading");

  navigator.geolocation.getCurrentPosition(
    async position => {
      try {
        const response = await uploadReport({
          file,
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        });

        if (response.report_saved) {
          await refreshDashboard(response.message || "Pothole reported successfully.");
        } else {
          setStatus(response.message || "Upload finished, but no report was saved.", "error");
        }
      } catch (error) {
        console.error(error);
        setStatus(`Upload failed: ${error.message}`, "error");
      } finally {
        setUploading(false);
      }
    },
    () => {
      setUploading(false);
      setStatus("Location access denied. Please allow location access and try again.", "error");
    }
  );
}

fileInput.addEventListener("change", () => {
  showPreview(fileInput.files[0]);
});

uploadButton.addEventListener("click", handleUpload);
locateButton.addEventListener("click", () => {
  setStatus("Finding your current location on the map...", "loading");

  navigator.geolocation.getCurrentPosition(
    position => {
      showCurrentLocation(
        position.coords.latitude,
        position.coords.longitude,
        position.coords.accuracy
      );
      setStatus("Current location pinned on the map.", "success");
    },
    () => {
      setStatus("Could not access your location. Please enable location permission.", "error");
    }
  );
});

setStatus("Loading dashboard...", "loading");
refreshDashboard().catch(error => {
  console.error(error);
  setStatus(`Could not load reports: ${error.message}`, "error");
});
