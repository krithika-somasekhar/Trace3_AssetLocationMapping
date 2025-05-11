document.getElementById("mapForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append("map_building", document.getElementById("map_building").value);
    formData.append("map_floor", document.getElementById("map_floor").value);
    formData.append("file", document.getElementById("map_file").files[0]);

    const mapId = document.getElementById("map_id").value;
    if (mapId) formData.append("map_id", mapId);

    fetch("http://127.0.0.1:5000/add_map", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            const responseMessage = document.getElementById("responseMessage");

            if (data.message) {
                responseMessage.innerText = data.message;
                responseMessage.style.color = "green";
                document.getElementById("mapForm").reset();
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
