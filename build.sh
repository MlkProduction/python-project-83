#!/usr/bin/env bash
# скачиваем uv и запускаем команду установки зависимостей
curl -LsSf https://astral.sh/uv/install.sh | sh
export $(grep -v '^#' .env | xargs)
make install && psql -a -d $DATABASE_URL -f database.sql