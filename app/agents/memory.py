import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class PortableBrain:
    def __init__(self, root: Path | None = None):
        self.root = root or Path(".agent")
        self.working = self.root / "working"
        self.episodic = self.root / "episodic"
        self.semantic = self.root / "semantic"
        self.personal = self.root / "personal"
        self._ensure_structure()

    def _ensure_structure(self) -> None:
        for p in [self.root, self.working, self.episodic, self.semantic, self.personal]:
            p.mkdir(parents=True, exist_ok=True)

    def write_working_state(self, key: str, payload: dict[str, Any]) -> None:
        out = self.working / f"{key}.json"
        out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def log_episode(self, agent_name: str, event_type: str, payload: dict[str, Any]) -> None:
        event = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "agent": agent_name,
            "event_type": event_type,
            "payload": payload,
        }
        log_path = self.episodic / "events.jsonl"
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")

    def read_lessons(self, query: str | None = None) -> list[dict[str, Any]]:
        lessons_path = self.semantic / "lessons.jsonl"
        if not lessons_path.exists():
            return []
        lessons = [json.loads(line) for line in lessons_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not query:
            return lessons
        q = query.lower()
        return [l for l in lessons if q in l.get("lesson", "").lower() or q in l.get("topic", "").lower()]

    def read_preferences(self) -> dict[str, Any]:
        prefs = self.personal / "preferences.json"
        if not prefs.exists():
            return {}
        return json.loads(prefs.read_text(encoding="utf-8"))
