#
# ( Use only if you are not working with devcontainers )
# File with a few utility commands for Docker
#

run-start-environment:
	docker compose up -d

run-stop-environment:
	docker compose down -v

run-ingest-db:
	docker exec -it cis /bin/bash -c "python ./src/ingest.py"

run-chat:
	docker exec -it cis /bin/bash -c "python ./src/chat.py"