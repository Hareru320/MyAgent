import asyncio
import copy
import time

from enum import Enum

from agt_agent.commons.type_def import AgtEventEnvelope, MinimalEnvelopeData, AgtIdentity
from agt_agent.commons.logger import logger


class AgentCommonEvent(str, Enum):
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'


EVENT_PIPE = asyncio.Queue(maxsize=1000)
    

class EventPipeWriter:

    async def post_event(
        self,
        *,
        event: AgentCommonEvent,
        target: AgtIdentity = None,
        data: MinimalEnvelopeData = None,
        timestamp: float = None,
        generation_id: str = None
    ):
        '''
        Args:
            event: Event enum.
            target: Event receiver, the AgtEventEnvelope will try to send to this target at the final.
            data: Event data, should contains event_name and content.
        '''
        
        envelope: AgtEventEnvelope = {
            "event": event.value,
            "target": copy.deepcopy(target),
            "data": copy.deepcopy(data),
            "timestamp": timestamp or time.time(),
            "generation_id": generation_id,
            "blocking": False,
        }

        await EVENT_PIPE.put(envelope)

    async def get_event(self) -> AgtEventEnvelope:
        return await EVENT_PIPE.get()
    
    async def clear(self):
        count = 0
        while not EVENT_PIPE.empty():
            await EVENT_PIPE.get()
            count = count + 1

        logger.info(f"Cleaned {count} in pipe.")
        return count



event_pipe = EventPipeWriter()