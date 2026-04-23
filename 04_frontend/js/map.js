import { API_BASE_URL } from "./config.js";
import { formatTimestamp } from "./formatters.js";

const map = L.map("map", {
  zoomControl: false,
}).setView([25.6, 85.1], 13);

L.control.zoom({ position: "bottomright" }).addTo(map);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
}).addTo(map);

const markersLayer = L.layerGroup().addTo(map);
const reportsById = new Map();
let currentLocationMarker = null;
let currentLocationRadius = null;

function getMarkerColors(report) {
  if (report.status === "fixed") {
    return { color: "#166534", fillColor: "#22c55e" };
  }

  if (report.verified) {
    return { color: "#1d4ed8", fillColor: "#60a5fa" };
  }

  return { color: "#b91c1c", fillColor: "#ef4444" };
}

function createPopupContent(report) {
  const imageUrl = report.image ? `${API_BASE_URL}/images/${report.image}` : null;

  return `
    <div class="popup-report">
      <strong>Pothole Report</strong>
      <div class="popup-meta">
        <span class="popup-status">Status: ${report.status || "reported"}</span>
        <span>Time: ${formatTimestamp(report.timestamp)}</span>
        <span>Verified: ${report.verified ? "Yes" : "No"}</span>
      </div>
      ${imageUrl ? `
        <div class="popup-preview" data-report-id="${report.id}">
          <img src="${imageUrl}" alt="Pothole report evidence" />
          <div class="popup-boxes"></div>
        </div>
      ` : ""}
    </div>
  `;
}

function drawBoundingBoxes(previewElement) {
  const reportId = previewElement.dataset.reportId;
  const report = reportsById.get(reportId);
  const image = previewElement.querySelector("img");
  const boxesLayer = previewElement.querySelector(".popup-boxes");
  const detections = report?.training_data?.detections || report?.detections || [];

  if (!image || !boxesLayer || !detections.length || !image.naturalWidth || !image.naturalHeight) {
    return;
  }

  boxesLayer.innerHTML = "";

  const scaleX = image.clientWidth / image.naturalWidth;
  const scaleY = image.clientHeight / image.naturalHeight;

  detections.forEach((detection, index) => {
    const bbox = detection.bbox?.[0] || detection.bbox || [];
    const [x1, y1, x2, y2] = bbox;

    if ([x1, y1, x2, y2].some(value => typeof value !== "number")) {
      return;
    }

    const box = document.createElement("div");
    box.style.position = "absolute";
    box.style.left = `${x1 * scaleX}px`;
    box.style.top = `${y1 * scaleY}px`;
    box.style.width = `${(x2 - x1) * scaleX}px`;
    box.style.height = `${(y2 - y1) * scaleY}px`;
    box.style.border = "2px solid #22c55e";
    box.style.borderRadius = "4px";
    box.style.boxSizing = "border-box";
    box.style.boxShadow = "0 0 0 1px rgba(255,255,255,0.25) inset";

    const label = document.createElement("div");
    label.textContent = `${index + 1}`;
    label.style.position = "absolute";
    label.style.left = "0";
    label.style.top = "0";
    label.style.transform = "translateY(-100%)";
    label.style.background = "#22c55e";
    label.style.color = "#052e16";
    label.style.fontSize = "10px";
    label.style.fontWeight = "700";
    label.style.padding = "1px 4px";
    label.style.borderRadius = "4px 4px 0 0";

    box.appendChild(label);
    boxesLayer.appendChild(box);
  });
}

map.on("popupopen", event => {
  const previewElement = event.popup.getElement()?.querySelector(".popup-preview");
  const image = previewElement?.querySelector("img");

  if (!previewElement || !image) {
    return;
  }

  if (image.complete) {
    drawBoundingBoxes(previewElement);
  } else {
    image.onload = () => drawBoundingBoxes(previewElement);
  }
});

export function renderReportsOnMap(reports) {
  markersLayer.clearLayers();
  reportsById.clear();

  const bounds = [];

  reports.forEach(report => {
    const lat = report.location?.lat;
    const lon = report.location?.lon;

    if (typeof lat !== "number" || typeof lon !== "number") {
      return;
    }

    reportsById.set(report.id, report);
    const { color, fillColor } = getMarkerColors(report);

    L.circleMarker([lat, lon], {
      radius: 8,
      color,
      fillColor,
      fillOpacity: 0.92,
      weight: 2,
    })
      .addTo(markersLayer)
      .bindPopup(createPopupContent(report));

    bounds.push([lat, lon]);
  });

  if (bounds.length) {
    map.fitBounds(bounds, { padding: [36, 36] });
  }

  markersLayer.eachLayer(layer => {
    if (typeof layer.bringToFront === "function") {
      layer.bringToFront();
    }
  });
}

export function showCurrentLocation(latitude, longitude, accuracy = 0) {
  if (currentLocationMarker) {
    map.removeLayer(currentLocationMarker);
  }

  if (currentLocationRadius) {
    map.removeLayer(currentLocationRadius);
  }

  currentLocationRadius = L.circle([latitude, longitude], {
    radius: Math.max(accuracy, 35),
    color: "#2563eb",
    fillColor: "#60a5fa",
    fillOpacity: 0.16,
    weight: 1.5,
    interactive: false,
  }).addTo(map);

  currentLocationMarker = L.circleMarker([latitude, longitude], {
    radius: 9,
    color: "#ffffff",
    fillColor: "#2563eb",
    fillOpacity: 1,
    weight: 3,
    interactive: false,
  })
    .addTo(map);

  map.flyTo([latitude, longitude], 17, {
    duration: 0.8,
  });

  markersLayer.eachLayer(layer => {
    if (typeof layer.bringToFront === "function") {
      layer.bringToFront();
    }
  });
}
