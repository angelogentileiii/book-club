function expandDescription(bookId) {
    var fullDesc = document.getElementById("description-" + bookId);
    var truncatedDesc = document.getElementById("trunc-description-" + bookId);
    var expandLink = document.getElementById("expand-" + bookId);

    // Ensure this function is only called if there is a truncated description
    if (!truncatedDesc || !fullDesc || !expandLink) {
        return; // Return if no truncated description exists
    }

    // If the full description is currently hidden, show it
    if (fullDesc.style.display === "none") {
        fullDesc.style.display = "inline"; // Show full description
        truncatedDesc.style.display = "none"; // Hide truncated description
        expandLink.innerHTML =
            "<a href='javascript:void(0);' onclick='expandDescription(\"" +
            bookId +
            "\")'>[Read Less]</a>"; // Change to "Read less"
    } else {
        fullDesc.style.display = "none"; // Hide full description
        truncatedDesc.style.display = "inline"; // Show truncated description
        expandLink.innerHTML =
            "<a href='javascript:void(0);' onclick='expandDescription(\"" +
            bookId +
            "\")'>[Read More]</a>"; // Revert back to "Read more"
    }
}
