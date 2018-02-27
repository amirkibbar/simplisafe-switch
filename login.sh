#!/bin/bash

script_dir=`dirname $0`

. $script_dir/functions.sh

auth_file=$1
verify_usage

basic_header="Authorization: Basic NGRmNTU2MjctNDZiMi00ZTJjLTg2NmItMTUyMWIzOTVkZWQyLjEtMC0wLldlYkFwcC5zaW1wbGlzYWZlLmNvbTo="

json=`curl -s -d @$1 -H "$basic_header" -H "Content-type: application/json" $API_URL/api/token`
access_token=`echo "$json" | jq -r '.access_token'`

bearer_header="Authorization: Bearer $access_token"

json=`curl -s -H "$bearer_header" $API_URL/api/authCheck`
user_id=`echo $json | jq -r '.userId'`

echo "$access_token:$user_id"
