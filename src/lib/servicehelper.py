
import shlex
import logging
import subprocess

logger = logging.getLogger("ServiceHelper")

def executeCommand(command: str):
    if not command: return

    try:
        subprocess.Popen(
            shlex.split(command), shell=False, start_new_session=True)
    except Exception as e:
        logger.exception(e)
        #Notification(
        #    app_name=APP_NAME,
        #    title="Command executor",
        #    icon_path=ICON_LOCATION,
        #    urgency="critical",
        #    description=str(e)
        #).send_linux()

def openUrl(url: str):
    subprocess.Popen(["xdg-open", url], shell=False)
