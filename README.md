# Delivery Estimation Service

The Delivery Estimation Service is a FastAPI-based application designed to calculate the optimal delivery route between multiple locations using the Haversine formula. This API provides real-time delivery estimations by computing the shortest distance over the Earth's surface.

## Features

-   **FastAPI Backend:** Provides a RESTful API for estimating delivery distances.
-   **Haversine Distance Calculation:** Uses the Haversine formula to determine the shortest path between two geographical points with an average speed of 20km/hr.
-   **Optimal Route Estimation:** Computes the most efficient delivery route based on distance calculations.
-   **Interactive API Docs:** Automatically generated API documentation available via Swagger UI and ReDoc.

## Assumptions

-   **Spherical Earth Model:** Assumes the Earth is a perfect sphere, leading to minor inaccuracies due to its ellipsoidal shape.
-   **Direct Path:** Considers a direct path between two points without factoring in obstacles such as buildings or terrain.
-   **Static Locations:** Uses fixed coordinates for delivery points, without accounting for dynamic factors like traffic or road closures.

## Installation

### Prerequisites

-   Ensure Docker is installed on your system.

### Steps

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/Jordy51/DeliveryEstimationService.git
    ```
2. **Navigate to the Project Directory:**
    ```bash
    cd DeliveryEstimationService
    ```
3. **Start the Service with Docker:**
    ```bash
    docker compose up
    ```

## Usage

### Running the API Server (Without Docker)

If you prefer to run the FastAPI server manually:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://127.0.0.1:8000/`.

### API Endpoints

#### 1. Find Optimal Route

-   **Endpoint:** `POST /optimal-route`
-   **Description:** Determines the optimal delivery route and estimated delivery time.
-   **Request Body:**
    ```json
    {
    	"deliveryExecLocation": {
    		"latitude": 12.9352,
    		"longitude": 77.6245
    	},
    	"orders": [
    		{ "restaurantId": "R3", "consumerId": "C2" },
    		{ "restaurantId": "R4", "consumerId": "C6" },
    		{ "restaurantId": "R5", "consumerId": "C5" }
    	]
    }
    ```
-   **Example Response:**
    ```json
    {
    	"optimalRoute": ["R5", "R3", "C2", "C5", "R4", "C6"],
    	"estimatedTime": "2h 6m"
    }
    ```

#### 2. Create Restaurant

-   **Endpoint:** `POST /restaurant`
-   **Description:** Registers a new restaurant with location and preparation time data.
-   **Request Body:**
    ```json
    {
    	"name": "McD",
    	"latitude": 12.963,
    	"longitude": 77.648,
    	"avgPreparationTime": 55
    }
    ```
-   **Example Response:**
    ```json
    {
    	"name": "McD",
    	"latitude": 12.963,
    	"longitude": 77.648,
    	"avgPreparationTime": 55,
    	"id": "R7"
    }
    ```

#### 3. Get Restaurants

-   **Endpoint:** `GET /restaurant`
-   **Description:** Retrieves a list of registered restaurants.
-   **Example Request:**
    ```bash
    curl "http://127.0.0.1:8000/restaurant"
    ```
-   **Example Response:**
    ```json
    [
    	{ "id": "R1", "name": "Bakery" },
    	{ "id": "R7", "name": "McD" }
    ]
    ```

#### 4. Create Consumer

-   **Endpoint:** `POST /consumer`
-   **Description:** Registers a new consumer with location data.
-   **Request Body:**
    ```json
    {
    	"name": "Aditya",
    	"latitude": 12.941,
    	"longitude": 77.425
    }
    ```
-   **Example Response:**
    ```json
    {
    	"name": "Aditya",
    	"latitude": 12.941,
    	"longitude": 77.425,
    	"id": "C7"
    }
    ```

#### 5. Get Consumers

-   **Endpoint:** `GET /consumer`
-   **Description:** Retrieves a list of registered consumers.
-   **Example Request:**
    ```bash
    curl "http://127.0.0.1:8000/consumer"
    ```
-   **Example Response:**
    ```json
    [
    	{ "id": "C1", "name": "Aman" },
    	{ "id": "C7", "name": "Aditya" }
    ]
    ```

### API Documentation

FastAPI provides automatic interactive documentation at:

-   **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
-   **ReDoc UI:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
