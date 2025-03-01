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
   Ensure you have Docker installed, then run:
    ```bash
    docker compose up
    ```

## Usage

### Running the API Server

Start the FastAPI server by executing:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

This will launch the API on `http://127.0.0.1:8000/`.

### API Endpoints

#### 1. Find Optimal Route

-   **Endpoint:** `POST /optimal-route`
-   **Description:** Returns the optimal route for delivery between orders and estimated time.
-   **Request Parameters:**

    -   `name` (string): Restaurant name
    -   `latitude` (float): Latitude of the consumer
    -   `longitude` (float): Longitude of the consumer

-   **Example Request Body:**

    ```json
    {
    	"deliveryExecLocation": {
    		"latitude": 12.9352,
    		"longitude": 77.6245
    	},
    	"orders": [
    		{
    			"restaurantId": "R3",
    			"consumerId": "C2"
    		},
    		{
    			"restaurantId": "R4",
    			"consumerId": "C6"
    		},
    		{
    			"restaurantId": "R5",
    			"consumerId": "C5"
    		}
    	]
    }
    ```

    ```

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
-   **Description:** Create restaurant and store location & preparation time data
-   **Query Parameters:**

    -   `name` (string): Restaurant name
    -   `latitude` (float): Latitude of the restaurant
    -   `longitude` (float): Longitude of the restaurant
    -   `avgPreparationTime` (int): Average preparation time of the restaurant in minutes

-   **Example Request Body:**

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
-   **Description:** List restaurants
-   **Example Request:**
    ```bash
    curl "http://127.0.0.1:8000/restaurant
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
-   **Description:** Create consumer and store location data
-   **Request Parameters:**

    -   `name` (string): Restaurant name
    -   `latitude` (float): Latitude of the consumer
    -   `longitude` (float): Longitude of the consumer

-   **Example Request Body:**

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
-   **Description:** List consumers
-   **Example Request:**
    ```bash
    curl "http://127.0.0.1:8000/consumer
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

-   Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
-   Redoc UI: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
