# simplisafe-switch

Turn on or off simplisafe.com alarm system. To use this you must have the upgraded monitoring package.

The script assumes that you want to set the state to your first subscription only.

To use it create an authorization file in the following format:

```json
{
  "username": "your-simplisafe-user",
  "password": "your-simplisafe-pass",
  "client_id": "uuid"
}
```

This script is based on https://github.com/bachya/simplisafe-python, see instructions there on how to
obtain the MFA client_id, specifically these instructions here: https://simplisafe-python.readthedocs.io/en/latest/usage.html#simplisafe-multi-factor-authentication.

I recommend using a virtual env with this script. The minimum Python version is 3.7, I used 3.8.4.
