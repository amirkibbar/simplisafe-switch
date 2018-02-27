#!/bin/bash

auth_file=$1
script_dir=`dirname $0`

. $script_dir/functions.sh

auth_file=$1
verify_usage "state --force" "state can be one of: HOME, AWAY, OFF. The OFF state will not override AWAY, unless you pass --force"

target_state=$2
force=$3

lower_case_target_state=`echo $target_state | tr "[:upper:]" "[:lower:]"`

if [ -z "$target_state" ]; then
	echo "please specify state"
	exit 1
fi

if [[ ! "OFF HOME AWAY" =~ ($target_state) ]]; then
  echo "state should be one of: OFF, HOME, or AWAY"	
	exit 1
fi

$script_dir/get-state.sh $auth_file | while read subscription_state; do
  sid=`echo $subscription_state | cut -d: -f1`
  curr_state=`echo $subscription_state | cut -d: -f2`
  state_updated=`echo $subscription_state | cut -d: -f3`
  access_token=`echo $subscription_state | cut -d: -f4`
  user_id=`echo $subscription_state | cut -d: -f5`

	echo "user $user_id, subscription $sid current state: $curr_state"

	if [ "$curr_state" == "AWAY" -a -z "$force" ]; then
		echo "state AWAY cannot be overriden without --force"
	  continue
	fi

	bearer_header="Authorization: Bearer $access_token"
	curl -s -H "$bearer_header" -H "content-type: application/json" \
		-d "{\"state\": \"$target_state\"}" $API_URL/ss3/subscriptions/$sid/state/$lower_case_target_state
done

