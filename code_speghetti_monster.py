# task_manager.py (bad)
import json, time, random

STATE = {"tasks": [], "next_id": 1, "log": []}   # global mutable state!!

def add_task(title, priority=1, tags=[]):  # mutable default arg!
    try:
        x = {"id": STATE["next_id"], "title": title, "priority": priority, "done": False}
        for t in tags:                    # mutates shared list
            x.setdefault("tags", []).append(t)
        STATE["tasks"].append(x)
        STATE["next_id"] += 1
        if len(STATE["tasks"]) % 3 == 0:  # random side quest
            _recalc_priorities()          # circular side effects
        log("added", x)
        return x
    except:
        pass  # swallow ALL errors

def complete_task(id_or_title):
    for i, x in enumerate(STATE["tasks"]):
        if x["id"] == id_or_title or x["title"] == id_or_title:
            x["done"] = True
            if random.random() < 0.2:
                save("tasks.json")        # I/O in the middle of business logic
            log("completed", x)
            return True
    return False

def find(f=None):
    # overloaded: returns list or prints depending on f
    if f is None:
        for x in STATE["tasks"]:
            print(x)                      # I/O mixed in
        return None
    out = []
    for x in STATE["tasks"]:
        try:
            if eval(f):                   # eval on user-provided string 😱
                out.append(x)
        except:
            pass
    return out

def _recalc_priorities():
    # randomly bumps priorities; also completes tasks sometimes??
    for x in STATE["tasks"]:
        if not x.get("done"):
            x["priority"] = min(5, x.get("priority", 1) + (1 if random.random() < 0.5 else 0))
        else:
            if random.random() < 0.1:
                x["done"] = False         # undo completion by accident
    if len(STATE["tasks"]) > 10:
        _backup_then_clear()              # surprise global mutation

def _backup_then_clear():
    save("backup.json")
    for i in range(len(STATE["tasks"])):  # clears in-place weirdly
        if i % 2 == 0:
            continue
        try:
            del STATE["tasks"][i]         # index mutation while iterating ☠️
        except:
            pass

def save(path):
    # sleeps, logs, sometimes recurses for no reason
    time.sleep(0.05)
    try:
        with open(path, "w") as f:
            f.write(json.dumps(STATE))    # tight coupling to global shape
        if random.random() < 0.05:
            save(path)                    # accidental recursion
        log("saved", {"path": path})
    except:
        log("save_failed", {"path": path})

def load(path):
    try:
        STATE.update(json.load(open(path)))  # replaces whole state silently
        log("loaded", {"path": path})
    except:
        pass

def log(event, payload):
    STATE["log"].append({"t": time.time(), "e": event, "p": payload})

# ad-hoc demo flow (logic + CLI + side effects all tangled)
if __name__ == "__main__":
    add_task("buy milk", 2, tags=["home"])
    add_task("write report", 3)
    add_task("email Bob", 1, tags=["work"])
    find()  # prints
    complete_task("write report")
    print(find("x['priority'] >= 2 and not x['done']"))
    save("tasks.json")
