import yaml
from typing import Dict


class WiPiException(Exception):
    pass


class WiPi:
    def __init__(
        self,
        menumode: str,
        openmode: str,
        soundmode: str,
        navmode: str,
        ffbmode: str,
        osmmode: str,
        servermode: str,
    ) -> None:
        self.__menumode: str = menumode
        self.__openmode: str = openmode
        self.__soundmode: str = soundmode
        self.__navmode: str = navmode
        self.__ffbmode: str = ffbmode
        self.__osmmode: str = osmmode
        self.__servermode: str = servermode

    # def __repr__(self) -> str:
    #     return f"WiPi([{', '.join(repr(cab) for cab in self.cabinets)}])"

    @property
    def menumode(self) -> str:
        return self.__menumode

    @menumode.setter
    def menumode(self, menumode: str) -> None:
        self.__menumode = menumode

    @property
    def openmode(self) -> str:
        return self.__openmode

    @openmode.setter
    def openmode(self, openmode: str) -> None:
        self.__openmode = openmode

    @property
    def soundmode(self) -> str:
        return self.__soundmode

    @soundmode.setter
    def soundmode(self, soundmode: str) -> None:
        self.__soundmode = soundmode

    @property
    def navmode(self) -> str:
        return self.__navmode

    @navmode.setter
    def navmode(self, navmode: str) -> None:
        self.__navmode = navmode

    @property
    def ffbmode(self) -> str:
        return self.__ffbmode

    @ffbmode.setter
    def ffbmode(self, ffbmode: str) -> None:
        self.__ffbmode = ffbmode

    @property
    def osmmode(self) -> str:
        return self.__osmmode

    @osmmode.setter
    def osmmode(self, osmmode: str) -> None:
        self.__osmmode = osmmode

    @property
    def servermode(self) -> str:
        return self.__servermode

    @servermode.setter
    def servermode(self, servermode: str) -> None:
        self.__servermode = servermode

    @staticmethod
    def from_yaml(yaml_file: str) -> "WiPi":
        with open(yaml_file, "r") as fp:
            data = yaml.safe_load(fp)

        if data is None:
            # Assume this is an empty file, create with default values
            return WiPi(
                menumode='advanced',
                openmode='openoff',
                soundmode='soundoff',
                navmode='navon',
                ffbmode='ffboff',
                osmmode='osmoff',
                servermode='serveroff'
            )

        if not isinstance(data, dict):
            raise WiPiException(f"Invalid YAML file format for {yaml_file}, missing values!")

        print(data)

        return WiPi(**data)

    def to_yaml(self, yaml_file: str) -> None:
        data: Dict[Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str]] = {}
        
        data = {
            'menumode': self.__menumode,
            'openmode': self.__openmode,
            'soundmode': self.__soundmode,
            'navmode': self.__navmode,
            'ffbmode': self.__ffbmode,
            'osmmode': self.__osmmode,
            'servermode': self.__servermode
        }

        with open(yaml_file, "w") as fp:
            yaml.dump(data, fp)
