# Delivery Estimation Service

The Delivery Estimation Service is a FastAPI-based application designed to calculate the optimal delivery route between two locations using the Haversine formula. This API provides real-time delivery estimations by computing the shortest distance over the Earth's surface.

## Features

-   **FastAPI Backend:** Provides a RESTful API to estimate delivery distances.
-   **Haversine Distance Calculation:** Uses the Haversine formula to determine the shortest path between two geographical points.
-   **Optimal Route Estimation:** Calculates the most efficient delivery route based on computed distances.
-   **Interactive API Docs:** Automatically generated API documentation available via Swagger UI.

## Assumptions

-   **Spherical Earth Model:** Assumes Earth is a perfect sphere for distance calculations, which may introduce minor inaccuracies due to Earth's ellipsoidal shape.
-   **Direct Path:** Considers a direct path between two points without accounting for real-world obstacles like buildings or terrain.
-   **Static Locations:** Assumes fixed coordinates for delivery points without considering dynamic factors such as moving vehicles or temporary restrictions.

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/Jordy51/DeliveryEstimationService.git
    ```

2. **Navigate to the Project Directory:**

    ```bash
    cd DeliveryEstimationService
    ```

3. **Install Dependencies:**
   Ensure you have Python installed, then install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the API Server

Start the FastAPI server by executing:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

This will launch the API on `http://127.0.0.1:8000/`.

### API Endpoints

#### 1. Calculate Distance

-   **Endpoint:** `GET /distance`
-   **Description:** Calculates the Haversine distance between two locations.
-   **Query Parameters:**
    -   `lat1` (float): Latitude of the first location
    -   `lon1` (float): Longitude of the first location
    -   `lat2` (float): Latitude of the second location
    -   `lon2` (float): Longitude of the second location
-   **Example Request:**
    ```bash
    curl "http://127.0.0.1:8000/distance?lat1=40.7128&lon1=-74.0060&lat2=34.0522&lon2=-118.2437"
    ```
-   **Example Response:**
    ```json
    {
    	"distance_km": 3940.07
    }
    ```

#### 2. Find Optimal Route

-   **Endpoint:** `GET /optimal-route`
-   **Description:** Returns the optimal route for delivery between two locations.
-   **Query Parameters:**
    -   `start` (string): Name or coordinates of the starting location
    -   `end` (string): Name or coordinates of the destination
-   **Example Request:**
    ```bash
    curl "http://127.0.0.1:8000/optimal-route?start=New York&end=Los Angeles"
    ```
-   **Example Response:**
    ```json
    {
    	"route": ["New York", "Chicago", "Denver", "Las Vegas", "Los Angeles"],
    	"total_distance_km": 4500.5
    }
    ```

### API Documentation

FastAPI provides automatic interactive documentation at:

-   Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
-   Redoc UI: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Testing

A `test_and_result.txt` file is provided to showcase test cases and expected outcomes. Run tests using:

```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

_Note: This README is based on the project's structure and standard practices. For specific details, refer to the actual implementation._
