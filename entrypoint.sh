#!/bin/bash

if [ "$APP_MODE" = "PRODUCTION" ]; then
  # Production logic
  uvicorn app.main:app --host 0.0.0.0 --port 80
else
  # Development or other environment logic
  uvicorn app.main:app --host 0.0.0.0 --port 80 --reload
fi

# Run your application
exec "$@"
