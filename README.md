# Floor Plan Grid System

A simple Flask application that overlays a grid with coordinate labels on floor plan images or PDFs.

```markdown
# Floor Plan Grid System

Welcome to the **Floor Plan Grid System**, a simple Flask application designed to overlay a coordinate grid on floor plan images. This system is ideal for facilities management, office planning, or any scenario where visualizing floor layouts with grid coordinates is essential.

The system supports uploading floor plan images or PDFs, processes them by adding a grid overlay, and generates a downloadable link to the processed floor plan. This makes it easier for users to manage and interact with floor plans in a structured way.

## Features

- Overlay grid with coordinate labels on floor plan images so that you can specify where your assets are at.
- Dynamic asset thumbnail to represent the asset type and color-coded according to warranty status.
- Provides a downloadable summary table for assets tied to the floor plans.

## Prerequisites

Before you start, ensure you have the following installed:

- **Python** 3.7 or later
- **MySQL** database

## Installation

Follow the steps below to get the system up and running locally.

1. **Clone the repository:**

   ```bash
   git clone [repository URL]
   cd floor_plan_app
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```


## Configuration

1. **Update MySQL credentials in `app/config.py`:**

   Edit the `app/config.py` file to include your MySQL credentials:

   ```python
   class Config:
       # ... other configurations ...
       DB_HOST = 'localhost'
       DB_USER = 'your_mysql_username'
       DB_PASSWORD = 'your_mysql_password'
       DB_NAME = 'your_database_name'
   ```

2. **Create the `uploads` directory:**

   ```bash
   mkdir uploads
   ```

## Running the Application

Once everything is set up, you can start the application by running:

```bash
python3 run.py
```

The app will start on `http://localhost:5000`.

## Testing the API

To interact with the application, use an API client like **Postman** or **Insomnia** to send a POST request.

- **Endpoint:** `http://localhost:3000/process_floor_plan`
- **Method:** POST
- **Body Type:** Multipart Form Data
- **Form Fields:**
  - `file` (File): Upload your floor plan image or PDF.
  - `building_name` (Text): Name of the building.
  - `floor_number` (Text): Floor number.
  - `grid_size` (Text, optional): Grid size in pixels (default is 20).

**Response Example:**

```json
{
  "message": "Floor plan processed successfully",
  "user_id": "generated-uuid",
  "building_name": "Building A",
  "floor_number": "1",
  "floorplan_link": "http://localhost:3000/uploads/generated-uuid.png"
}
```

## Accessing the Processed Image

After processing, you can view or download the processed floor plan by opening the `floorplan_link` URL in a browser.

## Dependencies

Here are the dependencies required for the application:

- **Flask**
- **opencv-python**
- **numpy**
- **pillow**
- **pdf2image**
- **PyMySQL**
- **cryptography**
- **blinker**
- **Flask-Cors**
- **Werkzeug**
- **click**
- **Jinja2**

## Notes

- For security, use a dedicated MySQL user with appropriate privileges instead of the root user.

## Short Summary

1. Install dependencies and configure the application.
2. Run the Flask app locally.
3. Send a POST request with the required fields.
4. Access the processed floor plan via the provided download link.

## Contact

If you have any questions or need further assistance, feel free to reach out at:
<br>bkunnath@umd.edu
<br>balaji@umd.edu
<br>krithi58@umd.edu
<br>sumitp15@umd.edu
<br>jchoong@umd.edu

We’re happy to help!

---

Thank you for using the **Asset Location Mapping System**. We hope this application helps streamline your floor planning tasks.
