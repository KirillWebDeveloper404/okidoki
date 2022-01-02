build:
	docker build -t kirillwebdev404/okidoki .

push:
	docker push kirillwebdev404/okidoki

rm:
	docker image rm kirillwebdev404/okidoki

run:
	docker run --rm --name okidoki -p 8000:8000 -d -e PYTHONUNBUFFERED=1 kirillwebdev404/okidoki

log:
	docker logs okidoki

stop:
	docker stop okidoki
	docker image rm kirillwebdev404/okidoki

start:
	make build
	make run

restart:
	make stop
	make start