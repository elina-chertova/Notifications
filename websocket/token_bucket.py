import asyncio
import time

import websockets

MAX_MESSAGES_PER_SECOND = 5
TOKENS_PER_SECOND = 1


class TokenBucket:
    def __init__(self, capacity, fill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.fill_rate = fill_rate
        self.last_fill = time.monotonic()

    def get_tokens(self):
        now = time.monotonic()
        tokens_to_add = (now - self.last_fill) * self.fill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_fill = now
        return self.tokens

    def consume_tokens(self, count):
        tokens = self.get_tokens()
        if tokens >= count:
            self.tokens = tokens - count
            return True
        else:
            return False
