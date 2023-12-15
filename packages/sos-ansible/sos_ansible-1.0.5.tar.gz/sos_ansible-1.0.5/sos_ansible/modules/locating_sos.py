"""
Class based on the lookup plugin created by Chris Meyers.
https://github.com/chrismeyersfsu/sosreport-elk
"""

import glob
import os
from typing import Union
import re
from logging import getLogger

from sos_ansible.modules.config_manager import ConfigParser

config = ConfigParser()
config.setup()

logger = getLogger("root")


class LocateReports:
    """
    Validate the sosreport directory existance and provide the hostname and path for reference
    """

    def get_tower_hostname(self, pathname: os.path) -> Union[str, str]:
        """
        Return the hostname

        :param os.path pathname: Directory containing sosreports
        :return hostname, controller
        :rtype: Union[str, str] | str
        """
        path = os.path.join(pathname, "etc", "tower", "conf.d", "cluster_host_id.py")
        try:
            with open(path, encoding="utf-8") as file:
                data = file.read()
            cl_id = re.search("CLUSTER_HOST_ID = '(.*?)'", data)
            if cl_id.group(1):
                hostname = cl_id.group(1)
                controller = True
            return hostname, controller
        except FileNotFoundError:
            pass

        try:
            with open(
                os.path.join(pathname, "etc", "hostname"), encoding="utf-8"
            ) as file:
                hostname = file.read().rstrip("\n")
                controller = False
            return hostname, controller
        except FileNotFoundError:
            pass
        return "NOTFOUND"

    def run(self, terms: list, user_choice: str):
        """
        :param list terms: list of directories to search
        :param str user_choice: case number

        Return the hostname, path keypair
        """
        entry = {
            "hostname": "",
            "path": "",
        }

        # lookups in general are expected to both take a list as input and output a list
        # this is done so they work with the looping construct 'with_'.
        ret = []
        if not isinstance(terms, list):
            dirs_handler = []
            dirs_handler.append(terms)
        for sos_directory in dirs_handler:
            sos_dir = os.path.abspath(sos_directory)
            search_dir = os.path.join(sos_dir, user_choice, "sosreport-*")
            logger.error(sos_dir)
            for directory in glob.glob(search_dir, recursive=False):
                if os.path.isdir(directory):
                    hostname, controller = self.get_tower_hostname(directory)
                    entry = {
                        "hostname": hostname,
                        "path": directory.replace(directory + "/", ""),
                        "controller": controller,
                    }
                    ret.append(entry)

        return ret
