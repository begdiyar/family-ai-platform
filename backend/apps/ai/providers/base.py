from abc import ABC, abstractmethod
from typing import Generator


class AIProvider(ABC):

    @abstractmethod
    def stream(self, messages: list) -> Generator[str, None, None]:
        """SSE streaming — yields text chunks one by one."""
        ...

    @abstractmethod
    def complete(self, messages: list) -> str:
        """Non-streaming response with default params. Backwards-compat alias for generate()."""
        ...

    @abstractmethod
    def generate(self, messages: list, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Non-streaming response with configurable params."""
        ...
