deploy-build:
	docker-compose down
	docker-compose up --build -d

deploy:
	docker-compose down
	docker-compose up -d

docker-up-dev:
	docker-compose up -d redis db

