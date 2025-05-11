document.getElementById("assetForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append("asset_name", document.getElementById("asset_name").value);
    formData.append("asset_type", document.getElementById("asset_type").value);

    const assetThumbId = document.getElementById("asset_thumb_id").value;
    const roomId = document.getElementById("room_id").value;
    const gridX = document.getElementById("gridx").value;
    const gridY = document.getElementById("gridy").value;

    if (assetThumbId) formData.append("asset_thumb_id", assetThumbId);
    if (roomId) formData.append("room_id", roomId);
    if (gridX) formData.append("gridx", gridX);
    if (gridY) formData.append("gridy", gridY);

    fetch("http://127.0.0.1:5000/add_assets", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const responseMessage = document.getElementById("responseMessage");

        if (data.message) {
            responseMessage.innerText = data.message;
            responseMessage.classList.add("success");
            responseMessage.classList.remove("error");
            document.getElementById("assetForm").reset();
        } else if (data.error) {
            responseMessage.innerText = data.error;
            responseMessage.classList.add("error");
            responseMessage.classList.remove("success");
        } else {
            responseMessage.innerText = "Unknown error occurred.";
            responseMessage.classList.add("error");
            responseMessage.classList.remove("success");
        }
    })
    .catch(error => {
        const responseMessage = document.getElementById("responseMessage");
        responseMessage.innerText = "An error occurred.";
        responseMessage.classList.add("error");
        responseMessage.classList.remove("success");
        console.error("Error:", error);
    });
});
