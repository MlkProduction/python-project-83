#!/usr/bin/env bash
# скачиваем uv и запускаем команду установки зависимостей
curl -LsSf https://astral.sh/uv/install.sh | sh

export PATH="$HOME/.local/bin:$PATH"

uv sync

make install && psql -a -d $DATABASE_URL -f database.sql