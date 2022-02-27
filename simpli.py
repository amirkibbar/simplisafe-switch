import asyncio
import json
from types import SimpleNamespace

import click
import simplipy
from aiohttp import ClientSession


def store_creds(api):
    token = {
        'access_token': api.access_token,
        'refresh_token': api.refresh_token,
        'user_id': api.user_id,
    }
    with open('.simplisafe-auth.json', 'w') as out:
        json.dump(token, out)        


async def get_system_from_session(session):
    creds = get_creds()
    api = await simplipy.API.async_from_refresh_token(creds.refresh_token, session=session)
    store_creds(api)
    systems = await api.async_get_systems()

    return systems.get(list(systems.keys())[0])


async def get_system():
    async with ClientSession() as session:
        return await get_system_from_session(session)


def get_creds():
    with open("./.simplisafe-auth.json") as f:
        return json.loads(f.read(), object_hook=lambda d: SimpleNamespace(**d))


async def turn_system_on(mode):
    system = await get_system()
    curr_state = system.state
    print("SimpliSafe at {}".format(system.address))

    if curr_state == simplipy.system.SystemStates.OFF:
        print("System is OFF, turning it on to mode {}".format(mode))
        async with ClientSession() as session:
            system = await get_system_from_session(session)
            if mode == "home":
                await system.async_set_home()
            elif mode == "away":
                await system.async_set_away()
            else:
                print("Unknown mode {}".format(mode))

        system = await get_system()
        print("SimpliSafe state is now {}".format(system.state))
    else:
        print("System is {}, aborting turn on request to mode {}".format(curr_state, mode))


async def turn_system_off() -> None:
    system = await get_system()
    curr_state = system.state
    print("SimpliSafe at {}".format(system.address))

    if curr_state == simplipy.system.SystemStates.HOME:
        async with ClientSession() as session:
            system = await get_system_from_session(session)
            print("System is turned on and in more HOME, turning it off")
            await system.async_set_off()

            system = await get_system()
            print("SimpliSafe state is now {}".format(system.state))
    else:
        print("System is in mode {}, ignoring turn off request".format(curr_state))


async def print_sensors_status() -> None:
    async with ClientSession() as session:
        system = await get_system_from_session(session)
        for serial, sensor in system.sensors.items():
            await sensor.async_update(cached=False)
            if sensor.type.name != "keypad" and sensor.type.name != "keychain":
                status = "closed"
                if sensor.triggered and sensor.type.name == "entry":
                    status = "open"
                elif sensor.triggered:
                    status = "triggered"
                elif sensor.type.name != "entry":
                    status = "not triggered"

                print("Sensor {} ({}) is {}".format(sensor.name, sensor.type.name, status))


async def generate_code(auth_code, verifier_code) -> None:
    async with ClientSession() as session:
        api = await simplipy.API.async_from_auth(auth_code, verifier_code, session=session)
        store_creds(api)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--mode", default="home", help="home or away")
def turn_on(mode):
    asyncio.run(turn_system_on(mode))


@cli.command()
def turn_off():
    asyncio.run(turn_system_off())


@cli.command()
def sensors_status():
    asyncio.run(print_sensors_status())


@cli.command()
@click.option("--code", help="authorization code")
@click.option("--verifier", help="verifier code")
def authenticate(code, verifier):
    asyncio.run(generate_code(code, verifier))


if __name__ == "__main__":
    cli()
