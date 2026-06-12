import random
import time
from datetime import datetime, UTC

users = [f"user{i}" for i in range(1, 80)] + ["admin", "root", "ceo", "finance"]
countries = ["US", "CN", "RU", "UK", "DE", "FR", "IN", "BR", "JP", "IR", "KP"]
devices = ["desktop", "mobile", "laptop", "tablet"]

HIGH_VALUE_TARGETS = ["admin", "root", "ceo", "finance"]

def generate_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

def base_event(user, event_type, risk):
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "user": user,
        "ip": generate_ip(),
        "location": random.choice(countries),
        "device": random.choice(devices),
        "risk_score": risk,
        "event_type": event_type
    }

# attack scenario

def brute_force_wave():
    user = random.choice(HIGH_VALUE_TARGETS)
    events = []
    for _ in range(random.randint(20, 50)):  # BIG burst
        e = base_event(user, "brute_force_attempt", random.randint(80, 100))
        e["action"] = "login_failed"
        e["status"] = 401
        events.append(e)
    return events

def impossible_travel():
    user = random.choice(users)
    loc1, loc2 = random.sample(countries, 2)

    e1 = base_event(user, "normal_activity", 20)
    e1["location"] = loc1
    e1["action"] = "login_success"
    e1["status"] = 200

    e2 = base_event(user, "impossible_travel", random.randint(80, 95))
    e2["location"] = loc2
    e2["action"] = "login_success"
    e2["status"] = 200

    return [e1, e2]

def account_takeover():
    user = random.choice(HIGH_VALUE_TARGETS)

    events = []

    # suspicious login
    e1 = base_event(user, "account_takeover", random.randint(85, 100))
    e1["action"] = "login_success"
    e1["status"] = 200

    # privilege escalation
    e2 = base_event(user, "privilege_escalation", 95)
    e2["action"] = "access_sensitive_data"
    e2["status"] = 200

    # account locked
    e3 = base_event(user, "account_locked", 100)
    e3["action"] = "lock_account"
    e3["status"] = 403

    events.extend([e1, e2, e3])
    return events

def normal_activity():
    user = random.choice(users)
    e = base_event(user, "normal_activity", random.randint(1, 40))
    e["action"] = "login_success"
    e["status"] = 200
    return [e]

# secario engine

def generate_scenario():
    scenario = random.choices(
        ["normal", "brute_force", "travel", "takeover"],
        weights=[50, 25, 15, 10]
    )[0]

    if scenario == "brute_force":
        return brute_force_wave()
    elif scenario == "travel":
        return impossible_travel()
    elif scenario == "takeover":
        return account_takeover()
    else:
        return normal_activity()

while True:
    events = generate_scenario()

    for e in events:
        print(e, flush=True)

    # rando speed to make real world trafic patterens
    if random.random() < 0.2:
        time.sleep(0.05)  # rapid burst
    else:
        time.sleep(random.uniform(0.2, 0.8))