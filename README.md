# simplisafe-switch

Turn on or off simplisafe.com alarm system. To use this you must have the upgraded monitoring package.

The script assumes that you want to set the same state to all your subscriptions.

To use it create an authorization file in the following format:

```json
{
  "grant_type": "password",
  "username": "your-simplisafe-user",
  "password": "your-simplisafe-pass"
}
```

The `login.sh`, and `get-state.sh` scripts output machine-parsable results.

Use the `set-state.sh` to change the state of the alarm. The script will only change from `AWAY` state when you pass
the `--force` option.

Examples:

Set state to home:

```bash
./set-state.sh auth.json HOME
```

Set state to off even if it's away:

```bash
./set-state.sh auth.json OFF --force
```

The API is partly reversed engineered from the simplisafe.com dashboard, and partly based on this thread:
https://community.smartthings.com/t/simplisafe-alarm-integration-cloud-to-cloud/8473/44.
