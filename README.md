# AI-Powered Cyber Attack Command Center

An AI-driven Security Operations Center (SOC) built on Splunk that detects, explains, and responds to cyber attacks in real time — turning raw security events into autonomous, auditable defense actions.

**Splunk Agentic Ops Hackathon 2026**
---

## The Problem

Traditional SOCs can detect threats, but they still rely heavily on humans to respond. An analyst has to see an alert, investigate it, and then take action — often minutes or even hours after an attack begins.

Attackers operate in seconds. Defenders need systems that can act just as fast — while still keeping decisions transparent enough for humans to trust and audit.

---

## What This Project Does

This project simulates a live enterprise environment under attack and demonstrates a full agentic pipeline running on top of Splunk:

### Ingest
A Python event generator (`log_stream.py`) simulates security telemetry from identity and endpoint systems: login attempts, geolocation, device type, and per-event risk signals. Events stream continuously into a file that Splunk monitors in real time (`index: ai_soc`).

### Process
Splunk extracts fields from raw events using `rex` (since the generator emits Python-dict-formatted logs), normalizes them, and classifies each event by severity (**CRITICAL / HIGH / LOW**).

### Reason
The system correlates events into attack patterns rather than analyzing them in isolation:
- A burst of failed logins → **brute-force attack**
- Logins from distant locations in seconds → **impossible travel**
- Suspicious login followed by sensitive access → **account takeover**

Each detection includes a confidence score.

### Act
High-confidence detections trigger automated responses:
- Lock account  
- Enforce MFA  
- Alert the SOC  

Every action is logged back into Splunk, creating a full feedback loop.

### Show
A real-time Splunk dashboard provides:
- Live threat feed  
- Global attack map  
- AI decision table with reasoning  
- Action timeline  
- Live alert banner  

---

## Attack Scenarios Simulated

| Scenario | What it looks like | Typical outcome |
|----------|------------------|-----------------|
| **Normal activity (50%)** | Routine successful logins | Monitor |
| **Brute force wave (25%)** | 20–50 rapid failed logins on high-value accounts (admin, root, ceo, finance) | Trigger MFA or lock account |
| **Impossible travel (15%)** | Logins from different countries within seconds | Flag and step-up authentication |
| **Account takeover (10%)** | Suspicious login → privilege escalation → sensitive access | Lock account |

---

## Dashboard Panels

- **Live AI Threat Status** — Banner that switches from *SYSTEM STABLE* to an alert when a critical attack occurs  
- **Max Threat Level** — Highest risk score in the selected time window  
- **Global Attack Surface** — Geographic map of attacker origins  
- **Top Active Threat Targets** — Most attacked accounts ranked by risk  
- **AI Actions Executed Over Time** — Breakdown of automated responses  
- **Attack Timeline** — Attack progression from reconnaissance → compromise  
- **Live Threat Feed** — Raw incoming events  
- **AI Decision Engine** — Explains what happened, why it matters, what action was taken, and confidence level  

---

## Example Search Powering the Attack Map

```spl
index=ai_soc
| rex "'location':\s*'(?<location>[^']+)'"
| eval lat=case(location=="US",37.0902, location=="RU",61.5240, location=="CN",35.8617,
                location=="IN",20.5937, location=="DE",51.1657, true(), null())
| eval lon=case(location=="US",-95.7129, location=="RU",105.3188, location=="CN",104.1954,
                location=="IN",78.9629, location=="DE",10.4515, true(), null())
| where isnotnull(lat) AND isnotnull(lon)
| geostats count latfield=lat longfield=lon
```
---
## Repository Contents
```
├── README.md
├── ai_soc_architecture_diagram.png
├── log_stream.py
├── dashboard/
│   └── ai_soc_dashboard.json
├── DEMO_SCRIPT.md
```
## Quick Start

### Prerequisites

- Python 3.11+
- Splunk Enterprise 10.x (free trial + Developer License)
- A Splunk index named `ai_soc`

---

### 1. Create the Index

In Splunk Web:  
**Settings → Indexes → New Index → `ai_soc`**

---

### 2. Start the Live Event Stream

#### Windows (PowerShell)
```bash
python -u log_stream.py >> live_logs.txt
```
#### macOS/Linux
```bash
python3 -u log_stream.py >> live_logs.txt
```
Leave this running — it continuously generates realistic security events and attack patterns.

---

### 3. Point Splunk to the Stream

Go to:  
**Home → Add Data → Upload **

- Select `live_logs.txt`
- Choose Event Breaks **Every line** if not already
- Choose **Continuously Monitor**  
- Set the index to `ai_soc` or whatever you prefer

Splunk will now ingest events in real time.

---

### 4. Import the Dashboard

Go to:  
**Search & Reporting → Dashboards → Create New Dashboard**

Then open the **source editor** and paste:

```bash
dashboard/ai_soc_dashboard.json
```
