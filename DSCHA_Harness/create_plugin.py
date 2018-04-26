"""
This tool provides simple way to to create an action plugin for DSCHA Harness controller

Example use:
python create_plugin.py - n bigip_reboot
"""
import os
import logging
import sys
import argparse

log = logging.getLogger(__name__)

# Plugin
PLUGIN_DIR = "plugin"
ACTION_FUNC = "action"

PLUGIN_TEMPLATE = """
from celery import shared_task
from lib.bigip_tmsh import *
from lib.bigip_rest import *
from lib.bigip_lib import *
from lib.dsc_lib import *
from lib.application_lib import *
from action.handler.base import get_application, get_bigip, get_dsc
from action.handler.error import ModelNotExistException


@shared_task()
def action(*args, **kwargs):

    \"\"\"
    Action function to define your periodic task action. Get your target object id from kwargs or args

    :param args: list argument of application id, bigip id, or dsc id. [<app_id>/<bigip_id>/<dsc_id>]
    :param kwargs: dictionary of app id, bigip id, or dsc id.
    {"app": <app_id>, "bigip": <bigip_id>, "dsc": <dsc_id>}
    :return:
    \"\"\"
    app_obj = None
    bigip_obj = None
    dsc_obj = None
    if 'app' in kwargs:
        app_id = kwargs.get('app')
        app_obj = get_application(app_id)
    if 'bigip' in kwargs:
        bigip_id = kwargs.get('bigip')
        bigip_obj = get_application(bigip_id)
    if 'dsc' in kwargs:
        dsc_id = kwargs.get('dsc')
        dsc_obj = get_application(dsc_id)
    if not app_obj and not bigip_obj and not dsc_obj:
        raise ModelNotExistException


"""


def list_plugin():

    plugin_list = []
    for (dirpath, dirnames, filenames) in os.walk(PLUGIN_DIR):
        for file in filenames:
            if file.endswith('.py') is True:
                file_path = os.path.join(dirpath, file)
                if "def %s(*args, **kwargs):" % ACTION_FUNC in open(file_path, "r").read():
                    plugin_list.append(file.split(".")[0])
    return plugin_list


def main():

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", "--name", type=str,
                        help="Enter your plugin's name")
    parser.add_argument("-l", "--listplugin", action="store_true", default=False,
                        help="List all available plugins")
    args = parser.parse_args()
    try:
        plugin_list = list_plugin()
        if args.listplugin is True:
            print("List all available plugins:")
            for plugin in plugin_list:
                print(plugin)
            return
        plugin_name = args.name or input('Enter your plugin name: ')
        print(plugin_name)
        if plugin_name.endswith(".py"):
            plugin_name = plugin_name[:-3]
        name_list = []
        last_word = ""
        for char in plugin_name:
            if char == " " or char == "-" or char == "." :
                if last_word:
                    name_list.append(last_word)
                    last_word = ""
            else:
                last_word += char

        if last_word:
            name_list.append(last_word)
        format_plugin_name = "_".join(name_list)
        if format_plugin_name in plugin_list:
            raise Exception("Plugin %s already exists, please change another name" % format_plugin_name)
        open(os.path.join(PLUGIN_DIR, format_plugin_name+ ".py"), "w").write(PLUGIN_TEMPLATE)
        print("Plugin %s successfully created." % format_plugin_name)
    except KeyboardInterrupt:
        log.warning("Exit application")


if __name__ == "__main__":
    sys.exit(main())
