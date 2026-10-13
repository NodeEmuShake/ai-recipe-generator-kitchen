"""Token-stream handler — buffers model output and emits structured events."""
from __future__ import annotations

from collections.abc import Iterator, Callable


class StreamHandler:
    """Consumes a token iterator, emits partial text and finish callbacks.

    Callbacks fire synchronously on the calling thread. For UI integration
    marshal to the main thread yourself — this class does not own a loop.
    """

    def __init__(self, on_token: Callable[[str], None] | None = None,
                 on_done: Callable[[str], None] | None = None) -> None:
        self._on_token = on_token or (lambda _t: None)
        self._on_done = on_done or (lambda _t: None)

    def consume(self, tokens: Iterator[str]) -> str:
        buf: list[str] = []
        for tok in tokens:
            buf.append(tok)
            self._on_token(tok)
        text = "".join(buf)
        self._on_done(text)
        return text