from nwpc_monitor_web.app import app as application


def create_app():
    return application


if __name__ == "main":
    application.run()
