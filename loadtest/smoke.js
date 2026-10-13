import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 5,
  duration: "20s",
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<500"],
  },
};

export default function () {
  const base = __ENV.BASE_URL || "http://localhost:8000";

  const health = http.get(`${base}/health`);
  check(health, {
    "health is 200": (r) => r.status === 200,
  });

  const info = http.get(`${base}/api/v1/info`);
  check(info, {
    "info is 200": (r) => r.status === 200,
  });

  const items = http.get(`${base}/api/v1/items`);
  check(items, {
    "items is 200": (r) => r.status === 200,
  });

  sleep(1);
}
