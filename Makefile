deploy-local:
	docker stack deploy icarus --compose-file docker-compose.yml

build-local:
	docker-compose build

destroy-local:
	docker stack rm icarus

run-demo:
	python demos.py
