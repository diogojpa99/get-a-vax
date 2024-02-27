#!/usr/bin/env bash

set -euo pipefail
IFS=$'\t\n'

echo "Starting same day scheduling test"

echo "Logging in"

# -o /dev/null redirects the output to /dev/null
# -s silences the progress bar
# --compressed tells curl to use gzip compression
# -b cookie-jar.txt tells curl to use the cookie jar
# -c cookie-jar.txt tells curl to save the cookies to the cookie jar
# -w "%{http_code}\n" tells curl to print the http status code


# Save the session cookie to a file
curl 'http://127.0.0.1:6543/c/login' \
  --data-raw 'ersid=001-80-1523&born_at=2005-04-18' \
  -c cookie-jar.txt \
  -o /dev/null \
  -s \
  -w "%{http_code}\n" \
  --compressed

# Pass the two factor auth and save the session cookie to a file
curl 'http://127.0.0.1:6543/c/login' \
  -b cookie-jar.txt \
  -c cookie-jar.txt \
  -o /dev/null \
  -s \
  -w "%{http_code}\n" \
  --data-raw 'code=' \
  --compressed



#YESTERDAY=$(date -v-1d +%Y-%m-%d)
# For ubunto use
YESTERDAY=$(date -d "yesterday 13:00" '+%Y-%m-%d')
echo "Sending curl request to schedule appointment for yesterday ${YESTERDAY}"
# Send the request with the session cookie
# Check the response headers with -I
curl 'http://127.0.0.1:6543/c/schedule/cd9f6252-697c-4d0d-8bb0-f564c3ab1529' \
  --data-raw 'id_vse=cd9f6252-697c-4d0d-8bb0-f564c3ab1529&step=1&clinic=32fcfe73-bf1a-4e7e-b729-6578b7d3b08e&at='${YESTERDAY} \
  -b cookie-jar.txt \
  -c cookie-jar.txt \
  -o /dev/null \
  -s \
  -w "%{http_code}\n" \
  --compressed



TODAY=$(date +%Y-%m-%d)
echo "Sending curl request to schedule appointment for today ${TODAY}"
curl 'http://127.0.0.1:6543/c/schedule/cd9f6252-697c-4d0d-8bb0-f564c3ab1529' \
  --data-raw 'id_vse=cd9f6252-697c-4d0d-8bb0-f564c3ab1529&step=1&clinic=32fcfe73-bf1a-4e7e-b729-6578b7d3b08e&at='${TODAY} \
  -b cookie-jar.txt \
  -c cookie-jar.txt \
  -o /dev/null \
  -s \
  -w "%{http_code}\n" \
  --compressed


#TOMORROW=$(date -v+1d +%Y-%m-%d)
# For ubunto use
TOMORROW=$(date -d "tomorrow 13:00" '+%Y-%m-%d')
echo "Sending curl request to schedule appointment for tomorrow ${TOMORROW}"
curl 'http://127.0.0.1:6543/c/schedule/cd9f6252-697c-4d0d-8bb0-f564c3ab1529' \
  --data-raw 'id_vse=cd9f6252-697c-4d0d-8bb0-f564c3ab1529&step=1&clinic=32fcfe73-bf1a-4e7e-b729-6578b7d3b08e&at='${TOMORROW} \
  -b cookie-jar.txt \
  -c cookie-jar.txt \
  -o /dev/null \
  -s \
  -w "%{http_code}\n" \
  --compressed