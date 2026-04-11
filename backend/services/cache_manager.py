from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class CacheManager:
    def __init__(self, cache_dir: str = "data/cache") -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def hash_bytes(self, file_bytes: bytes) -> str:
        return hashlib.md5(file_bytes).hexdigest()

    def get(self, file_hash: str) -> dict[str, Any] | None:
        path = self._path(file_hash)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None

    def set(self, file_hash: str, payload: dict[str, Any]) -> None:
        path = self._path(file_hash)
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    def _path(self, file_hash: str) -> Path:
        return self.cache_dir / f"{file_hash}.json"
