#!/bin/bash

exec python /app/telegram_webhook.py

tail -f /dev/null
