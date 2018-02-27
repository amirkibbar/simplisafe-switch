#!/bin/bash

API_URL=https://api.simplisafe.com/v1

function verify_usage() {
	local more_opts="$1"
	local more_desc="$2"

	if [ -z "$auth_file" ]; then
    echo "usage: $0 auth-file $more_opts"
    echo "auth file should include this JSON:"
    cat << zZ
{
  "grant_type": "password",
  "username": "simplisafe-username",
  "password": "simplisafe-password"
}
zZ
    echo "$more_desc"
    exit 1
  fi
}
