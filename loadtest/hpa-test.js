import http from 'k6/http';
import { check, sleep } from 'k6';
export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '90s', target: 40 },
    { duration: '30s', target: 0 },
  ],
};
export default function () {
  const response = http.get(
    'http://host.docker.internal:8000/api/v1/items'
  );
  check(response, {
    'HTTP 200 returned': (r) => r.status === 200,
  });
  sleep(0.2);
}
