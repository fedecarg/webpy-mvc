#!/bin/bash
if [ "$1" == "" ]; then
  echo "Usage: $0 <filename.sql>"
  exit 0
fi

MYSQL_DB="example"
MYSQL_HOST="127.0.0.1"
MYSQL_USER="root"

rm -f mysql/${MYSQL_DB}.sql sqlite/${MYSQL_DB}.db

mysqldump -u $MYSQL_USER -p -h $MYSQL_HOST --skip-add-locks --compatible=ansi --default-character-set=binary $MYSQL_DB > mysql/${MYSQL_DB}.sql
if [ $? -gt 0 ]; then
    exit 1
fi

cp mysql/${MYSQL_DB}.sql mysql/$1
./mysql2sqlite.sh mysql/${MYSQL_DB} sqlite/${MYSQL_DB}
cp sqlite/${MYSQL_DB}.db ./../src/db/example.sqlite