from typing import Union, Any, Optional
from abc import ABC, abstractmethod


class IJWT(ABC):
    @abstractmethod
    def create(self, payload: dict) -> str:
        pass

    @abstractmethod
    def decode(self, token: str) -> Optional[dict[str, Any]]:
        pass
