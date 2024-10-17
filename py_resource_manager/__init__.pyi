from .culture_info import CultureInfoManager
from ._singleton import Singleton

class ResourceManager(metaclass=Singleton):
    compiled = ...
    def __init__(self, resource_file_path: str = ...) -> None:
        ...
    
    def get_string(self, key: str) -> str:
        """
        Retrieves a string for the current culture or falls back to the main resources.
        """
        ...

CultureInfo: CultureInfoManager
