# task_manager_clean.py (good)
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Iterable, Protocol, Optional
import json
from pathlib import Path

@dataclass(frozen=True)
class Task:
    id: int
    title: str
    priority: int = 1
    done: bool = False
    tags: List[str] = field(default_factory=list)

@dataclass
class TaskList:
    next_id: int = 1
    tasks: List[Task] = field(default_factory=list)

    def add(self, title: str, priority: int = 1, tags: Iterable[str] = ())-> Task:
        t = Task(self.next_id, title, max(1, min(5, priority)), False, list(tags))
        self.next_id += 1
        self.tasks.append(t)
        return t

    def complete(self, task_id: int) -> Task:
        for i, t in enumerate(self.tasks):
            if t.id == task_id:
                nt = Task(t.id, t.title, t.priority, True, t.tags)
                self.tasks[i] = nt
                return nt
        raise KeyError(f"No task with id={task_id}")

    def query(self, *, min_priority: int = 1, include_done: bool = True, tags: Optional[Iterable[str]] = None) -> List[Task]:
        tagset = set(tags or [])
        out = []
        for t in self.tasks:
            if t.priority < min_priority: continue
            if not include_done and t.done: continue
            if tagset and not tagset.issubset(t.tags): continue
            out.append(t)
        return out

class TaskRepo(Protocol):
    def load(self) -> TaskList: ...
    def save(self, tl: TaskList) -> None: ...

class JsonFileRepo:
    def __init__(self, path: Path): self.path = path
    def load(self) -> TaskList:
        if not self.path.exists(): return TaskList()
        data = json.loads(self.path.read_text())
        tl = TaskList(next_id=data["next_id"])
        for raw in data["tasks"]:
            tl.tasks.append(Task(**raw))
        return tl
    def save(self, tl: TaskList) -> None:
        payload = {"next_id": tl.next_id, "tasks": [asdict(t) for t in tl.tasks]}
        self.path.write_text(json.dumps(payload, indent=2))

# Application service (orchestrates repo + domain)
class TaskService:
    def __init__(self, repo: TaskRepo): self.repo = repo
    def add(self, *args, **kwargs) -> Task:
        tl = self.repo.load()
        t = tl.add(*args, **kwargs)
        self.repo.save(tl)
        return t
    def complete(self, task_id: int) -> Task:
        tl = self.repo.load()
        t = tl.complete(task_id)
        self.repo.save(tl)
        return t
    def list(self, **filters) -> List[Task]:
        tl = self.repo.load()
        return tl.query(**filters)

# Minimal CLI glue kept separate
if __name__ == "__main__":
    import argparse
    repo = JsonFileRepo(Path("tasks.json"))
    svc = TaskService(repo)

    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    a.add_argument("title")
    a.add_argument("--priority", type=int, default=1)
    a.add_argument("--tags", nargs="*", default=[])

    c = sub.add_parser("complete")
    c.add_argument("id", type=int)

    l = sub.add_parser("list")
    l.add_argument("--min-priority", type=int, default=1)
    l.add_argument("--include-done", action="store_true")
    l.add_argument("--tags", nargs="*")

    args = ap.parse_args()
    if args.cmd == "add":
        t = svc.add(args.title, priority=args.priority, tags=args.tags)
        print(f"Added #{t.id}: {t.title} (p{t.priority}) tags={t.tags}")
    elif args.cmd == "complete":
        try:
            t = svc.complete(args.id)
            print(f"Completed #{t.id}: {t.title}")
        except KeyError as e:
            print(e)
    elif args.cmd == "list":
        tasks = svc.list(min_priority=args.min_priority, include_done=args.include_done, tags=args.tags)
        for t in tasks:
            status = "✓" if t.done else " "
            print(f"[{status}] #{t.id} p{t.priority} {t.title}  {' '.join('#'+tag for tag in t.tags)}")
