#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$0")
RDS_DATA_DIR="$SCRIPT_DIR/../sql"
ALTER_TABLE_DIR="$RDS_DATA_DIR/alter_table"

export PGPASSWORD=$DB_PASSWORD

for sql_file in $(ls "$RDS_DATA_DIR"); do
  sql_path=$RDS_DATA_DIR/$sql_file
  echo "$sql_path"
  if [ ! -d "$sql_path" ]; then
    echo "$sql_path"
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USERNAME" -d "$DB_NAME" -f "$sql_path"
  fi
done

for sql_file in $(ls $ALTER_TABLE_DIR); do
  sql_path=$ALTER_TABLE_DIR/$sql_file
  echo "$sql_path"
  if [ ! -d "$sql_path" ]; then
    echo "$sql_path"
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USERNAME" -d "$DB_NAME" -f "$sql_path"
  fi
done
