import click
import datetime
from tabulate import tabulate
import os
import json

cli_version = "1.0.0-beta1"
config_file = os.path.expanduser("~/.timr")


def get_today_at_time(h, m):
    today = datetime.datetime.today()
    today_at_h = today.replace(hour=h, minute=m, second=0, microsecond=0)
    return today_at_h


def get_date_today_from_h_m_string(h_m_string):
    time = h_m_string.split(":")
    today_at_time = get_today_at_time(int(time[0]), int(time[1]))
    return today_at_time


@click.group()
def cli():
    pass


@click.command()
def version():
    click.echo(cli_version)


def format_break_time(break_time):
    if ':' in break_time:
        split = break_time.split(":")
        delta = datetime.timedelta(hours=int(split[0]), minutes=int(split[1]))
        return(delta.seconds/3600)
    return float(break_time.replace(",", "."))


@click.command()
@click.option('-s', '--start-time', required=False)
@click.option('-e', '--end-time', required=False)
@click.option('-b', '--break-time', required=False)
@click.option('-ch', '--contract-hours-per-day')
@click.option('--local-config/--no-local-config', default=True)
def calc(start_time, end_time, break_time, contract_hours_per_day, local_config):
    # use from cli input, then config, then default
    if os.path.exists(config_file) and local_config:
        with open(config_file) as config:
            data = json.load(config)
            start_time_d = data["start"]
            end_time_d = data["end"]
            break_time_d = data["break"]
            contract_hours_per_day_d = data["contract"]
    else:
        start_time_d = "9:00"
        end_time_d = "17:30"
        break_time_d = "1"
        contract_hours_per_day_d = "7.4"

    if not start_time:
        start_time = start_time_d
    if not end_time:
        end_time = end_time_d
    if not break_time:
        break_time = break_time_d
    if not contract_hours_per_day:
        contract_hours_per_day = contract_hours_per_day_d

    break_time = format_break_time(break_time)
    start_today = get_date_today_from_h_m_string(start_time)
    end_today = get_date_today_from_h_m_string(end_time)
    duration = end_today - start_today
    worked_h = float(duration.seconds/3600) - break_time
    extra = round(worked_h - float(contract_hours_per_day), 2)
    click.echo(tabulate([
        ['Start time', start_today.time()],
        ['End time', end_today.time()],
        ['Duration at work', duration],
        ['Included break time', break_time],
        ['Hours worked', worked_h],
        ['1 day of mobile work', contract_hours_per_day],
        ['Add extra mobile work', click.style(
            str(extra), blink=True, bold=True, fg='green')]
    ], headers=[
        'Description', 'Result'], tablefmt='orgtbl'))


@click.command()
@click.option('--start-time', required=True, prompt='Provide a default start time of work')
@click.option('--end-time', required=True, prompt='Provide a default end time of work')
@click.option('--break-time', required=True, prompt='Provide a default break time')
@click.option('--contract-hours-per-day', required=True, prompt='Provide a default for work hours per day')
def configure(start_time, end_time, break_time, contract_hours_per_day):
    if os.path.exists(config_file):
        os.remove(config_file)
    data = {
        "start": start_time,
        "end": end_time,
        "break": break_time,
        "contract": contract_hours_per_day,
    }
    with open(config_file, 'w') as outfile:
        json.dump(data, outfile)
    click.echo(
        f'Configuration completed! (config file location: {config_file})')


cli.add_command(version)
cli.add_command(calc)
cli.add_command(configure)

if __name__ == '__main__':
    cli()
