document.getElementById("contractForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form from submitting normally

    // Prepare form data for submission
    const formData = new FormData();
    formData.append("start_date", document.getElementById("start_date").value);
    formData.append("end_date", document.getElementById("end_date").value);
    formData.append("is_expired_flag", document.getElementById("is_expired_flag").value);
    formData.append("asset_id", document.getElementById("asset_id").value);

    // Send data to backend
    fetch("http://127.0.0.1:5000/add_contract", {  // Update URL if different
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById("responseMessage").innerText = data.message;
            document.getElementById("responseMessage").style.color = "green";
            document.getElementById("contractForm").reset(); // Reset form fields
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
