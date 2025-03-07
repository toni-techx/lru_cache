test:
	docker-compose exec web sh -c "export CACHE_CAPACITY=2 && python -m pytest -svv"

up:
	docker-compose up -d

down:
	docker-compose down