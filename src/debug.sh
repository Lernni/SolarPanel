#!/bin/bash
# TODO: Open in different terminals

cd solar_module
source ./.venv/bin/activate
DEBUG=true python -m app --wait-for-client --multiprocess -m flask run &
deactivate

cd ../web_socket
NODE_ENV=debug node index.js &

cd ../frontend
npm run serve &