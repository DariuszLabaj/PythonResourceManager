"""
This type stub file was generated by pyright.
"""

from typing import Protocol


class CultureInfoManager(Protocol):
    
    def SetCulture(self, culture: str) -> None:
        ...
    
    @property
    def CurrentCulture(self) -> str:
        ...
    


CultureInfo: CultureInfoManager = ...
