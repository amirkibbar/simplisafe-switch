import asyncio
import click
import json

from aiohttp import ClientSession
import simplipy


async def get_system():
  creds = get_creds()
  async with ClientSession() as session:
    simplisafe = await simplipy.API.login_via_credentials(creds["username"], creds["password"], client_id=creds["client_id"], session=session)
    systems = await simplisafe.get_systems()
    
    system = systems.get(list(systems.keys())[0])
    return system


def get_creds():
  with open('./simplisafe.json') as f:
    return json.load(f)


async def turn_system_on(mode):
  system = await get_system()
  curr_state = system.state
  print('SimpliSafe at {}'.format(system.address))

  if curr_state == simplipy.system.SystemStates.off:
    print('System is OFF, turning it on to mode {}'.format(mode))
    if mode == "home":
      await system.set_home()
    elif mode == "away":
      await system.set_away()
    else:
      print('Unknown mode {}'.format(mode))
    
    system = await get_system()
    print('SimpliSafe state is now {}'.format(system.state))
  else:
    print('System is {}, aborting turn on request to mode {}'.format(curr_state, mode))


async def turn_system_off():
  system = await get_system()
  curr_state = system.state
  print('SimpliSafe at {}'.format(system.address))

  if curr_state == simplipy.system.SystemStates.home:
    print('System is turned on and in more HOME, turning it off')
    await system.set_off()

    system = await get_system()
    print('SimpliSafe state is now {}'.format(system.state))
  else:
    print('System is in mode {}, ignoring turn off request'.format(curr_state))


async def print_sensors_status():
  system = await get_system()
  for serial, sensor in system.sensors.items():
    await sensor.update(cached=True)
    if sensor.type.name != 'keypad' and sensor.type.name != 'keychain':
      status = 'closed'
      if sensor.triggered and sensor.type.name == 'entry':
        status = 'open'  
      elif sensor.triggered:
        status = 'triggered'
      elif sensor.type.name != 'entry':
        status = "not triggered"

      print('Sensor {} ({}) is {}'.format(sensor.name, sensor.type.name, status))


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


if __name__ == '__main__':
  cli()
