import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
	stages: [
		{ duration: "30s", target: 1000 }, // Ramp-up to 10 users over 30 seconds
		{ duration: "1m", target: 1000 }, // Stay at 10 users for 1 minute
		{ duration: "30s", target: 0 }, // Ramp-down to 0 users over 30 seconds
	],
	thresholds: {
		http_req_duration: ["p(95)<500"], // 95% of requests should be below 500ms
	},
};

export default function () {
	// Example GET request
	let res = http.get("http://localhost:8000/restaurant"); // Replace with actual endpoint
	check(res, {
		"GET /estimate status is 200": (r) => r.status === 200,
		"GET /estimate response time < 500ms": (r) => r.timings.duration < 500,
	});

	// Example POST request
	res = http.post(
		"http://localhost:8000/optimal-route",
		JSON.stringify({
			deliveryExecLocation: {
				latitude: 12.9352,
				longitude: 77.6245,
			},
			orders: [
				{
					restaurantId: "R3",
					consumerId: "C2",
				},
				{
					restaurantId: "R4",
					consumerId: "C6",
				},
				{
					restaurantId: "R5",
					consumerId: "C5",
				},
			],
		}),
		{
			headers: { "Content-Type": "application/json" },
		}
	);
	check(res, {
		"POST /estimate status is 200": (r) => r.status === 200,
		"POST /estimate response time < 500ms": (r) => r.timings.duration < 500,
	});

	// Add more requests for other endpoints as needed

	sleep(1); // Simulate user think time
}
