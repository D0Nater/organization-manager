#!/bin/sh
set -e

if [ "$MODE" = "app" ]; then
  orgmgr run -p $PORT -h $HOST
elif [ "$MODE" = "migrations" ]; then
  orgmgr db migrate
elif [ "$MODE" = "dev" ]; then
  orgmgr dev --docker
elif [ "$MODE" = "shell" ]; then
  $@
else
  echo "ERROR: \$MODE is not set to \"app\", \"migrations\","
  echo "       \"dev\" or \"shell\"."
  echo "       Exiting."
  exit 1
fi
