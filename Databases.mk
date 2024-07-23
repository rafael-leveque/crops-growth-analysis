.DEFAULT_GOAL := all

.PHONY: start-postgres

start-postgres:
	$(info ### Start postgres ###)
	@docker pull postgres
	@docker run --name postgres-netcarbon -e POSTGRES_PASSWORD=netcarbon -d postgres

.PHONY: stop-postgres

stop-postgres:
	$(info ### Stop postgres ###)
	@docker stop postgres-netcarbon
	@docker rm postgres-netcarbon

.PHONY: start-mongo

start-mongo:
	$(info ### Start mongo ###)
	@docker pull mongo
	@docker run --name mongo-netcarbon -d mongo

.PHONY: stop-mongo

stop-mongo:
	$(info ### Stop mongo ###)
	@docker stop mongo-netcarbon
	@docker rm mongo-netcarbon

.PHONY: start-minio

start-minio:
	$(info ### Start minio ###)
	@docker pull minio/minio
	@docker run --name minio-netcarbon -d -e "MINIO_ACCESS_KEY=minio -e MINIO_SECRET_KEY=netcarbon" minio/minio server /data

.PHONY: stop-minio

stop-minio:
	$(info ### Stop minio ###)
	@docker stop minio-netcarbon
	@docker rm minio-netcarbon

