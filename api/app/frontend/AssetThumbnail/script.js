document.getElementById("assetThumbnailForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form from submitting normally

    // Prepare form data for submission
    const formData = new FormData();
    formData.append("asset_thumb_name", document.getElementById("asset_thumb_name").value);
    
    const assetThumbId = document.getElementById("asset_thumb_id").value;
    const file = document.getElementById("file").files[0];

    // Append optional fields if they have values
    if (assetThumbId) formData.append("asset_thumb_id", assetThumbId);
    if (file) formData.append("file", file);

    // Send data to backend
    fetch("http://127.0.0.1:5000/add_asset_thumbnail", {  // Update URL if different
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById("responseMessage").innerText = data.message;
            document.getElementById("responseMessage").style.color = "green";
            document.getElementById("assetThumbnailForm").reset(); // Reset form fields
        } else {
            document.getElementById("responseMessage").innerText = data.error || "Error occurred!";
            document.getElementById("responseMessage").style.color = "red";
        }
    })
    .catch(error => {
        document.getElementById("responseMessage").innerText = "An error occurred.";
        document.getElementById("responseMessage").style.color = "red";
        console.error("Error:", error);
    });
});
