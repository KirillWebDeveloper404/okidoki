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

start:
	make build
	make run

restart:
	make stop
	make start


reqs:
	rm requirements.txt
	pipreqs --encoding=utf8 .

ssh:
	ssh root@109.68.213.180