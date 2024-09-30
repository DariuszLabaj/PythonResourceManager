from typing import Self
import locale
import ctypes

windll = ctypes.windll.kernel32

class CultureInfoManager:
    _instance = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super(CultureInfoManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.__current_culture = locale.windows_locale[windll.GetUserDefaultUILanguage()]

    def SetCulture(self, culture: str) -> None:
        self.__current_culture = culture

    @property
    def CurrentCulture(self) -> str:
        return self.__current_culture
    
CultureInfo = CultureInfoManager()