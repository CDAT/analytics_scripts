from stats.models import Machine
import json

machines = Machine.objects.all()
users = {}
for m in machines:
    users[m.hashed_hostname] = set()
    for s in m.session_set.all():
        users[m.hashed_hostname].add(s.user.hashed_username)

with open("machine_users.json", "w") as f:
    json.dump({m: list(u) for m, u in users.items()}, f)
