#!/bin/bash

auth_file=$1
script_dir=`dirname $0`

. $script_dir/functions.sh

auth_file=$1
verify_usage

login_info=`$script_dir/login.sh $auth_file`

access_token=`echo $login_info | cut -d: -f1`
user_id=`echo $login_info | cut -d: -f2`

bearer_header="Authorization: Bearer $access_token"

curl -s -H "$bearer_header" \
 	"$API_URL/users/$user_id/subscriptions?activeOnly=true" | \
 	jq -r '.subscriptions[] | .sid' | while read sid; do
  json=`curl -s -H "$bearer_header" $API_URL/ss3/subscriptions/$sid/state`
	sid_state=`echo $json | jq -r '.state'`
	sid_last_updated=`echo $json | jq -r '.stateUpdated'`
	echo "$sid:$sid_state:$sid_last_updated:$access_token:$user_id"
done
