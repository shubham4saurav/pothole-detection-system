export function formatTimestamp(timestamp) {
  if (!timestamp) {
    return "N/A";
  }

  const date = new Date(timestamp);
  if (Number.isNaN(date.getTime())) {
    return timestamp;
  }

  return date.toLocaleString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

export function truncateFileName(name, maxLength = 24) {
  if (!name || name.length <= maxLength) {
    return name || "No file selected";
  }

  return `${name.slice(0, maxLength - 3)}...`;
}
