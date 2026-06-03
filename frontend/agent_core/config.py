"""Rate limiter and security configuration for the agent system."""

import time
from dataclasses import dataclass, field


@dataclass
class RateLimiter:
    max_requests_per_session: int = 15
    max_requests_per_minute: int = 5
    cooldown_seconds: int = 60
    _requests: list = field(default_factory=list)
    _total_count: int = 0

    def can_proceed(self) -> tuple[bool, str]:
        now = time.time()
        self._requests = [t for t in self._requests if now - t < self.cooldown_seconds]

        if self._total_count >= self.max_requests_per_session:
            return False, f"Session limit reached ({self.max_requests_per_session} queries max). Refresh page for new session."

        if len(self._requests) >= self.max_requests_per_minute:
            wait = int(self.cooldown_seconds - (now - self._requests[0]))
            return False, f"Rate limit: max {self.max_requests_per_minute}/min. Wait {wait}s."

        return True, ""

    def record_request(self):
        self._requests.append(time.time())
        self._total_count += 1

    @property
    def remaining(self) -> int:
        return max(0, self.max_requests_per_session - self._total_count)
