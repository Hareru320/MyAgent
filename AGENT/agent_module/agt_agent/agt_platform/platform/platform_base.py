from abc import ABC, abstractmethod
from typing import Any

from agt_agent.commons.type_def import AgtEntryDataSchema, AgtEventEnvelope


class PlatformBase(ABC):

    def __init__(self, platform: str):
        self.platform = platform

    @abstractmethod
    async def send(self, id: str, envelope: AgtEventEnvelope):
        """
        Send envelope to client.
        """
        pass

    @abstractmethod
    def trans_payload(self, raw_data: Any) -> AgtEntryDataSchema:
        """
        Translate data package to AgtEntryDataSchema.
        """
        pass

    @abstractmethod
    def _open_envelope(self, envelope: AgtEventEnvelope) -> dict:
        pass