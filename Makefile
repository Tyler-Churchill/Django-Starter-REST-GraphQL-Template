shell:
	docker exec -it django-server bash
start:
	docker-compose -f docker-compose.yml build
	docker-compose -f docker-compose.yml up
clean:
	docker-compose -f ./docker-compose.yml down --remove-orphans
