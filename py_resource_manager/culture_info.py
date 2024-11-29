from typing import Protocol, Self
import locale
import platform

class CultureInfoManager(Protocol):
    def SetCulture(self, culture: str) -> None:
        ...
    @property
    def CurrentCulture(self) -> str:
        ...

class _CultureInfoManager:
    _instance = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super(_CultureInfoManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if platform.system() == "Windows":
            import ctypes
            windll = ctypes.windll.kernel32
            self.__current_culture = locale.windows_locale[windll.GetUserDefaultUILanguage()]
        else:
            self.__current_culture = locale.getdefaultlocale()[0]

    def SetCulture(self, culture: str) -> None:
        self.__current_culture = culture

    @property
    def CurrentCulture(self) -> str:
        return self.__current_culture
    
CultureInfo: CultureInfoManager = _CultureInfoManager()
