#!/bin/bash
set -ex
echo "Creating datawarehouse user"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER dwh;
EOSQL
echo "Datawarehouse user created successfully"
