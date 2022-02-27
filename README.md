# simplisafe-switch

Turn on or off simplisafe.com alarm system. To use this you must have the upgraded monitoring package.

The script assumes that you want to set the state to your first subscription only.

This script is based on https://github.com/bachya/simplisafe-python, see instructions there on how to obtain the
verification codes: https://simplisafe-python.readthedocs.io/en/latest/usage.html#installation. Once you have codes run
this once:

```bash
python3 simpli.py authenticate --code <authentication-code> --verifier <verifier-code>
```

Again, both `authentication-code` and `verifier-code` should be obtained by following the instructions in the [
`simplisafe-python` library](https://simplisafe-python.readthedocs.io/en/latest/usage.html#installation).

This will create a local `.simplisafe-auth.json` with the authentication and refresh tokens. Treat this file as a
password file and protect it. Every time you run the `simpli.py` and connect to the SimpliSafe servers, this file will
be updated with new tokens.

I recommend using a virtual env with this script. The minimum Python version is 3.7, I used 3.8.4.
