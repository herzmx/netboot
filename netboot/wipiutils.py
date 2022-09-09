import os
import platform
import subprocess
from typing import List, Dict, Any
import csv


SYSTEM_SUPPORT = {
    'Sega Naomi': ['Sega Naomi', 'Sammy Atomiswave'],
    'Sega Naomi2': ['Sega Naomi', 'Sega Naomi2', 'Sammy Atomiswave'],
    'Sega Chihiro': ['Sega Chihiro'],
    'Sega Triforce': ['Sega Triforce']
}


class WiPiUtils:
    @staticmethod
    def getdimmlist(file: str) -> List[Dict[str, Any]]:
        dimmlist: List[Dict[str, Any]] = []
        with open(file) as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                dimmlist.append(row)
        return dimmlist

    @staticmethod
    def getrominfo(file: str) -> List[Dict[str, Any]]:
        rominfo = List[Dict[str, Any]] = []
        with open(file) as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                row['alpha_key'] = row['description'][:1].upper()
                rominfo.append(row)
        return rominfo

    @staticmethod
    def ping(host: str) -> bool:
        on_windows: bool = platform.system() == "Windows"
        param = '-n' if on_windows else '-c'
        command = ['ping', param, '1', host]
        return subprocess.call(command) == 0

    @staticmethod
    def getavailabledimms(system: str, dimmscsv: str) -> List[Dict[str, Any]]:
        dimmlist = WiPiUtils.getdimmlist(dimmscsv)
        availabledimms: List[Dict[str, Any]] = []
        for dimm in dimmlist:
            if system in SYSTEM_SUPPORT[dimm['type']] and WiPiUtils.ping(dimm['ipaddress']):
                availabledimms.append(dimm)
        return availabledimms
