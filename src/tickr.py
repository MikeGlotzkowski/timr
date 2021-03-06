import click
import datetime

cli_version = "1.0.0-beta1"
one_day_of_work_in_h = delta = datetime.timedelta(
    hours=7, minutes=24, seconds=00)


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


@click.command()
@click.option('-s', '--start-time', required=True, default="8:15")
@click.option('-e', '--end-time', required=True, default="18:00")
def calc(start_time, end_time):
    start_today = get_date_today_from_h_m_string(start_time)
    end_today = get_date_today_from_h_m_string(end_time)
    click.echo(start_today)
    click.echo(end_today)
    duration = end_today - start_today
    click.echo(duration - one_day_of_work_in_h)
    click.echo(float((duration - one_day_of_work_in_h).seconds/3600))


cli.add_command(version)
cli.add_command(calc)

if __name__ == '__main__':
    cli()
