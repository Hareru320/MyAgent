from typing import Any, cast

from agt_agent.commons.auto_init import auto_init
from agt_agent.agt_platform.platform.websocket_platform import WebsocketPlatform
from agt_agent.agt_agent_core.generation_manager import generation_manager, GenerationManager
from agt_agent.agt_platform.register import register_platform
from agt_agent.commons.type_def import AgtEntryDataSchema, AgtEventEnvelope
from agt_agent.commons.logger import logger


class DefaultPlatform(WebsocketPlatform):

    def __init__(self, gen_mgr: GenerationManager):
        super().__init__(platform="default", gen_mgr=gen_mgr)

    # envelope convert
    def _open_envelope(self, envelope: AgtEventEnvelope) -> dict:
        """
        Convert AgtEventEnvelope -> legacy websocket payload
        """

        if not envelope:
            return {}

        target = envelope.get("target") or {}
        data = envelope.get("data") or {}

        event = envelope.get("event")
        generation_id = envelope.get("generation_id")
        ts = envelope.get("timestamp")

        client_id = target.get("id")
        platform = target.get("platform", "default")
        history_id = target.get("conversation_id", "")

        block_id = envelope.get("block_id", "")

        return {
            "action": event,
            "ts": int(ts * 1000) if ts else 0,
            "generation_id": generation_id,
            "client_id": client_id,
            "platform": platform,
            "data": {
                "history_id": history_id,
                "messages": data
            },
            "block_id": block_id
        }


    def trans_payload(self, raw_data: Any) -> AgtEntryDataSchema:
        return cast(AgtEntryDataSchema, raw_data)


default_platform = DefaultPlatform(generation_manager)

auto_init.register(default_platform)


register_platform(default_platform)