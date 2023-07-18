#!/bin/bash

set -e

echo "Running DB migrations"
alembic upgrade head || { echo 'DB migrations failed' ; exit 1; }

# If the main.py file exists, use it as the default
if [ -f /app/app/main.py ]; then
	DEFAULT_MODULE_NAME=app.main
elif [ -f /app/main.py ]; then
	DEFAULT_MODULE_NAME=main
fi
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

# If there's a prestart.sh script in the /app directory or other path specified, run it before starting
PRE_START_PATH=${PRE_START_PATH:-/app/prestart.sh}
echo "Checking for script in $PRE_START_PATH"
if [ -f "$PRE_START_PATH" ] ; then
	echo "Running script $PRE_START_PATH"
	# shellcheck disable=SC1090
	. "$PRE_START_PATH" || { echo 'Prestart script failed' ; exit 1; }
else
	echo "There is no script $PRE_START_PATH"
fi

# Start Uvicorn
echo "Starting Uvicorn"
exec uvicorn --host 0.0.0.0 --port 8080 "${APP_MODULE}" --reload || { echo 'Uvicorn failed to start' ; exit 1; }
