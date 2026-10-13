install:
	python -m pip install -r requirements.txt

test:
	pytest -q

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t cloudopshub:local .

compose-up:
	docker compose up --build -d

compose-down:
	docker compose down

helm-lint:
	helm lint helm/cloudopshub
