# coding=utf-8
import click


@click.group()
def main():
    pass


@main.command()
@click.option('-c', '--config-file', help="config file path")
def worker(config_file):
    from nwpc_monitor_task_scheduler.celery_server.celery import app
    app.start()


@main.command()
def beat():
    from nwpc_monitor_task_scheduler.celery_server.celery import app, celery_config
    app.Beat(
        schedule=celery_config.config['celery_beat']['schedule']
    ).run()


if __name__ == "__main__":
    main()
