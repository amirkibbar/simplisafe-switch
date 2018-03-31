#!/bin/bash

auth_file=$1
script_dir=`dirname $0`

. $script_dir/functions.sh

auth_file=$1
verify_usage

# reverse engineered 5 = entry, 4 = motion
sensor_type=${2:-5}

login_info=`$script_dir/login.sh $auth_file`

access_token=`echo $login_info | cut -d: -f1`
user_id=`echo $login_info | cut -d: -f2`

bearer_header="Authorization: Bearer $access_token"

curl -s -H "$bearer_header" \
 	"$API_URL/users/$user_id/subscriptions?activeOnly=true" | \
 	jq -r '.subscriptions[] | .sid' | while read sid; do
	curl -s -H "$bearer_header" \
		"$API_URL/ss3/subscriptions/$sid/sensors?forceUpdate=true" | \
	 	jq -r ".sensors[] | select(.type == $sensor_type) | .name, .status.triggered" | while read line; do
	  sensor=$line
		read triggered
		echo "$sensor:$triggered"
	done
done
