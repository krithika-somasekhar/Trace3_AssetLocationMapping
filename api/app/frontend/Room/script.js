document.getElementById("roomForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form from submitting normally

    // Prepare form data for submission
    const formData = new FormData();
    formData.append("room_name", document.getElementById("room_name").value);
    formData.append("room_floor_no", document.getElementById("room_floor_no").value);
    formData.append("room_shape", document.getElementById("room_shape").value);
    formData.append("gridxx", document.getElementById("gridxx").value);
    formData.append("gridxy", document.getElementById("gridxy").value);
    formData.append("gridyx", document.getElementById("gridyx").value);
    formData.append("gridyy", document.getElementById("gridyy").value);

    const mapId = document.getElementById("map_id").value;
    if (mapId) formData.append("map_id", mapId);

    // Send data to backend
    fetch("http://127.0.0.1:5000/add_room", { // Update URL if different
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const responseMessage = document.getElementById("responseMessage");
        if (data.message) {
            responseMessage.innerText = data.message;
            responseMessage.style.color = "green";
            document.getElementById("roomForm").reset(); // Reset form fields
        } else {
            responseMessage.innerText = data.error || "Error occurred!";
            responseMessage.style.color = "red";
        }
    })
    .catch(error => {
        const responseMessage = document.getElementById("responseMessage");
        responseMessage.innerText = "An error occurred.";
        responseMessage.style.color = "red";
        console.error("Error:", error);
    });
});
