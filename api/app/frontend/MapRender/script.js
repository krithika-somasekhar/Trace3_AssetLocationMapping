// Toggle Map Button
document.getElementById("toggleMap").addEventListener("click", function () {
    const mapImage = document.getElementById("mapImage");
    if (mapImage.style.display === "none" || mapImage.classList.contains("hidden")) {
        mapImage.style.display = "block";
        mapImage.classList.remove("hidden");
    } else {
        mapImage.style.display = "none";
        mapImage.classList.add("hidden");
    }
});

// Summary Button
document.addEventListener("DOMContentLoaded", () => {
    // Attach event listener to the "Summary" button
    document.getElementById("dealSummary").addEventListener("click", async function () {
        const mapBuilding = document.getElementById("map_building").value;
        const mapFloor = document.getElementById("map_floor").value;

        if (!mapBuilding || !mapFloor) {
            alert("Please fill in both Building Name and Floor Number.");
            return;
        }

        try {
            // Fetch summary data
            const response = await fetch(`/fetch_deal_summary?map_building=${mapBuilding}&map_floor=${mapFloor}`);
            const result = await response.json();

            if (result.error) {
                alert(result.error || "Data not found.");
                return;
            }

            const data = result.assets;
            if (!data || !Array.isArray(data) || data.length === 0) {
                alert("No data available for the specified building and floor.");
                return;
            }

            // Show the popup with fetched data
            createPopupWithDataTables(data);
        } catch (error) {
            console.error("Error fetching deal summary:", error);
            alert("An error occurred while fetching the deal summary.");
        }
    });
});

/**
 * Dynamically creates and shows a modal styled with DataTables for the deal summary.
 * @param {Array} data - The summary data to display in the modal.
 */
function createPopupWithDataTables(data) {
    const modalHtml = `
        <div class="modal" id="dealSummaryModal">
            <div class="modal-dialog">
                <button class="close" onclick="closeModal()">&times;</button>
                <h3 class="modal-title">Summary</h3>
                <table id="dealSummaryTable" class="display" style="width: 100%;">
                    <thead>
                        <tr>
                            ${Object.keys(data[0]).map(header => `<th>${formatHeader(header)}</th>`).join("")}
                        </tr>
                    </thead>
                    <tbody>
                        ${data.map(row => `
                            <tr>
                                ${Object.values(row).map(value => {
                                    if (typeof value === "string" && value.startsWith("http")) {
                                        return `<td class="image-column"><img src="${value}" alt="Image"></td>`;
                                    }
                                    return `<td>${value}</td>`;
                                }).join("")}
                            </tr>
                        `).join("")}
                    </tbody>
                </table>
                <div class="modal-footer">
                    <button class="btn btn-secondary" onclick="closeModal()">Close</button>
                    <button id="downloadCsv" class="btn btn-primary">Download as CSV</button>
                </div>
            </div>
        </div>
    `;

    // Add modal to the placeholder div
    document.body.insertAdjacentHTML("beforeend", modalHtml);

    // Initialize DataTable after ensuring the JS is loaded
    initializeDataTable();

    // Add download CSV functionality
    document.getElementById("downloadCsv").addEventListener("click", () => downloadCsv(data));
}

/**
 * Initializes the DataTable with required configurations.
 */
function initializeDataTable() {
    $("#dealSummaryTable").DataTable({
        responsive: true,
        paging: true,
        searching: true,
        order: [[0, "asc"]],
        autoWidth: false, // Ensures proper column width handling
        columnDefs: [
            { targets: "image-column", orderable: false } // Disable sorting for image columns
        ]
    });
}

/**
 * Converts the summary data to CSV format and triggers a download.
 * @param {Array} data - The summary data to download as CSV.
 */
function downloadCsv(data) {
    const headers = Object.keys(data[0]).join(",");
    const rows = data.map(row => Object.values(row).join(","));
    const csvContent = [headers, ...rows].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "summary.csv";
    link.style.display = "none";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

/**
 * Closes the modal.
 */
function closeModal() {
    const modal = document.getElementById("dealSummaryModal");
    if (modal) {
        modal.remove();
    }
}

/**
 * Formats header keys to be more human-readable.
 * @param {string} key - The key to format.
 * @returns {string} - The formatted header string.
 */
function formatHeader(key) {
    return key.replace(/_/g, " ").replace(/\b\w/g, char => char.toUpperCase());
}

// Existing Search Button
document.getElementById("searchButton").addEventListener("click", function () {
    const mapBuilding = document.getElementById("map_building").value;
    const mapFloor = document.getElementById("map_floor").value;

    if (!mapBuilding || !mapFloor) {
        alert("Please fill in both Building Name and Floor Number.");
        return;
    }

    fetch(`/fetch_map?map_building=${mapBuilding}&map_floor=${mapFloor}`)
        .then(response => response.json())
        .then(data => {
            if (data.map_url) {
                const mapImage = document.getElementById("mapImage");
                const gridOverlay = document.getElementById("gridOverlay");

                mapImage.src = data.map_url;
                mapImage.style.display = "block";

                const mapContainer = document.querySelector(".map-container");
                gridOverlay.width = mapContainer.clientWidth;
                gridOverlay.height = mapContainer.clientHeight;

                drawGrid(gridOverlay, 20);
                fetchAssetFilters(mapBuilding, mapFloor); // Populate asset filters
                fetchAssets(mapBuilding, mapFloor); // Fetch and render assets
                fetchDepartments(mapBuilding, mapFloor); // Fetch and render department boundaries
            } else {
                alert(data.error || "Map not found.");
            }
        })
        .catch(error => {
            console.error("Error fetching map:", error);
            alert("An error occurred while fetching the map.");
        });
});

document.getElementById("toggleGrid").addEventListener("click", function () {
    const gridOverlay = document.getElementById("gridOverlay");
    gridOverlay.style.display = gridOverlay.style.display === "none" ? "block" : "none";
});


function drawGrid(canvas, gridSize) {
    const ctx = canvas.getContext("2d");

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = "rgba(0, 0, 0, 0.5)";
    ctx.lineWidth = 0.5;

    ctx.font = "8px Arial"; // Smaller font size
    ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
    ctx.textAlign = "center"; // Center align horizontally
    ctx.textBaseline = "middle"; // Center align vertically

    for (let x = 0; x <= canvas.width; x += gridSize) {
        for (let y = 0; y <= canvas.height; y += gridSize) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
            ctx.stroke();

            const gridX = Math.floor(x / gridSize);
            const gridY = Math.floor(y / gridSize);

            // Generate the unique grid ID
            const gridId = `${String(gridX).padStart(2, '0')}${String(gridY).padStart(2, '0')}`;

            // Calculate the center of the grid cell
            const centerX = x + gridSize / 2;
            const centerY = y + gridSize / 2;

            // Draw the grid ID in the center of the cell
            if (x + gridSize <= canvas.width && y + gridSize <= canvas.height) {
                ctx.fillText(gridId, centerX, centerY);
            }
        }
    }
}

function fetchAssetFilters(mapBuilding, mapFloor) {
    fetch(`/fetch_asset_filters?map_building=${mapBuilding}&map_floor=${mapFloor}`)
        .then(response => response.json())
        .then(data => {
            const assetNameFilter = document.getElementById("assetNameFilter");
            const assetTypeFilter = document.getElementById("assetTypeFilter");

            assetNameFilter.innerHTML = '<option value="">Select Asset Name</option>';
            assetTypeFilter.innerHTML = '<option value="">Select Asset Type</option>';

            if (data.assetNames) {
                data.assetNames.forEach(name => {
                    const option = document.createElement("option");
                    option.value = name;
                    option.textContent = name;
                    assetNameFilter.appendChild(option);
                });
            }

            if (data.assetTypes) {
                data.assetTypes.forEach(type => {
                    const option = document.createElement("option");
                    option.value = type;
                    option.textContent = type;
                    assetTypeFilter.appendChild(option);
                });
            }
        })
        .catch(error => console.error("Error fetching filters:", error));
}

function fetchAssets(mapBuilding, mapFloor) {
    const assetName = document.getElementById("assetNameFilter").value;
    const assetType = document.getElementById("assetTypeFilter").value;

    const queryParams = new URLSearchParams({
        map_building: mapBuilding,
        map_floor: mapFloor,
        asset_name: assetName || "",
        asset_type: assetType || ""
    });

    fetch(`/fetch_assets?${queryParams.toString()}`)
        .then(response => response.json())
        .then(data => {
            const assetContainer = document.getElementById("assetContainer");
            assetContainer.innerHTML = ""; // Clear existing assets

            if (data.assets && data.assets.length > 0) {
                renderAssets(data.assets);
            } else {
                alert("No assets found for the selected filters.");
            }
        })
        .catch(error => console.error("Error fetching assets:", error));
}

function renderAssets(assets) {
    const assetContainer = document.getElementById("assetContainer");
    assetContainer.innerHTML = ""; // Clear previous assets

    assets.forEach(asset => {
        const assetDiv = document.createElement("div");
        assetDiv.className = "asset";

        // Assign class based on contract status
        if (asset.is_expired_flag === null) {
            assetDiv.classList.add("blue-border"); // Null -> Blue
        } else if (asset.is_expired_flag) {
            assetDiv.classList.add("red-border"); // Expired -> Red
        } else {
            assetDiv.classList.add("green-border"); // Active -> Green
        }

        assetDiv.style.backgroundImage = `url(${asset.asset_thumb_url})`;

        // Position the asset on the grid
        const gridSize = 20; // Match the grid size used in drawGrid
        assetDiv.style.left = `${asset.gridx * gridSize}px`;
        assetDiv.style.top = `${asset.gridy * gridSize}px`;

        // Add hover event to magnify
        assetDiv.addEventListener("mouseover", function () {
            const infoDiv = document.createElement("div");
            infoDiv.id = "assetInfo";
            infoDiv.className = "asset-info";

            infoDiv.innerHTML = `
                <p><strong>Grid:</strong> ${asset.gridx}, ${asset.gridy}</p>
                <p><strong>Asset Name:</strong> ${asset.asset_name || "N/A"}</p>
                <p><strong>Asset Type:</strong> ${asset.asset_type || "N/A"}</p>
                <p><strong>Department:</strong> ${asset.department_name || "N/A"}</p>
                <p><strong>Contract Status:</strong> ${asset.is_expired_flag === null ? "null" : (asset.is_expired_flag ? "Expired" : "Active")}</p>
            `;

            document.body.appendChild(infoDiv);

            // Position infoDiv near the mouse pointer
            document.addEventListener("mousemove", (event) => {
                infoDiv.style.left = `${event.pageX + 10}px`;
                infoDiv.style.top = `${event.pageY + 10}px`;
            });
        });

        assetDiv.addEventListener("mouseout", function () {
            const infoDiv = document.getElementById("assetInfo");
            if (infoDiv) {
                infoDiv.remove();
            }
        });

        assetDiv.classList.add("animate");

        assetContainer.appendChild(assetDiv);
    });
}


function fetchDepartments(mapBuilding, mapFloor) {
    fetch(`/fetch_departments?map_building=${mapBuilding}&map_floor=${mapFloor}`)
        .then(response => response.json())
        .then(data => {
            if (data.departments && data.departments.length > 0) {
                drawDepartments(data.departments);
            } else {
                console.log("No departments found for this map.");
            }
        })
        .catch(error => {
            console.error("Error fetching departments:", error);
        });
}

function drawDepartments(departments) {
    const gridOverlay = document.getElementById("gridOverlay");
    const ctx = gridOverlay.getContext("2d");

    const gridSize = 20; // Match the grid size used in drawGrid

    // Clear previous department boundaries
    ctx.clearRect(0, 0, gridOverlay.width, gridOverlay.height);

    // Redraw gridlines
    drawGrid(gridOverlay, gridSize);

    departments.forEach(dept => {
        const [x1, y1] = dept.gridxx.split(',').map(Number);
        const [x2, y2] = dept.gridyy.split(',').map(Number);

        // Convert grid coordinates to pixels
        const px1 = x1 * gridSize, py1 = y1 * gridSize;
        const px2 = x2 * gridSize, py2 = y2 * gridSize;

        // Draw department boundary
        ctx.strokeStyle = "rgba(255, 0, 0, 0.8)";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.rect(px1, py1, px2 -    px1, py2 - py1);
        ctx.stroke();

        // Draw department name at the center of the boundary
        ctx.font = "12px Arial";
        ctx.fillStyle = "black";
        ctx.textAlign = "center";
        ctx.fillText(dept.department_name, (px1 + px2) / 2, (py1 + py2) / 2);
    });
}



