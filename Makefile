#!/bin/bash

run_postgres:
	docker-compose -f containers/docker-compose-postgres.yml up -d

run_admin:
	docker-compose -f containers/docker-compose-admin.yml up -d


