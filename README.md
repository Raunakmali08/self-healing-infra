# Self-Healing Infrastructure 🏥

> A smart system that watches your apps 24/7, and when something breaks, it fixes itself automatically!

---

## 🎯 What Does This Project Do?

Imagine you have a robot friend who:
1. **Watches** your computer programs all day and night
2. **Notices** when something goes wrong (like a program crashing)
3. **Automatically fixes** the problem without human help
4. **Tells you** what happened through a chat app

That's exactly what this project does! It's like having a self-repairing robot for your computer programs.

---

## 🧩 The Tech Building Blocks (Like LEGO!)

This project is built with different "LEGO pieces" that work together:

### Monitoring & Watching (The Watchers)
| Tool | What It Does | Port |
|------|-------------|------|
| **Prometheus** | Collects numbers/metrics from all programs (like a scorekeeper) | 9090 |
| **Loki** | Collects and stores all the text logs from programs | 3100 |
| **Promtail** | Sends logs from programs to Loki (like a mail carrier) | - |
| **Node Exporter** | Watches the computer itself (CPU, memory, disk) | 9100 |

### Alerting & Notifying (The Alarm System)
| Tool | What It Does | Port |
|------|-------------|------|
| **Alertmanager** | Decides what to do when an alert fires | 9093 |
| **Telegram Bot** | Sends messages to your phone like a text message | 8080 |

### Visualization (The Dashboards)
| Tool | What It Does | Port |
|------|-------------|------|
| **Grafana** | Shows pretty charts and graphs of all the data | 3001 |

### Self-Healing (The Fixer-Bot)
| Tool | What It Does | Port |
|------|-------------|------|
| **Webhook Receiver** | Catches alerts and starts the healing process | 5001 |
| **Ansible** | Does the actual work of restarting broken programs | - |

### Sample Applications (The Patients)
| Tool | What It Does | Port |
|------|-------------|------|
| **Task Manager (Backend)** | API that manages a list of tasks | 3000 |
| **Task Manager (Frontend)** | Website to see and create tasks | 80 |
| **Flask App** | A simple demo app that can break (to test healing!) | 5000 |
| **PostgreSQL** | A database that stores the tasks | 5432 |

---

## 🔄 How Does the Self-Healing Work? (The Magic Flow!)

```
Step 1: Monitoring
┌─────────────────────────────────────────────────────────────────┐
│  Programs  ──────►  Prometheus  ──────►  Alertmanager           │
│  (make metrics)       (collects)            (decides)           │
└─────────────────────────────────────────────────────────────────┘
         │                                           │
         ▼                                           ▼
┌─────────────────┐                        ┌─────────────────────┐
│     Loki        │                        │   Webhook Receiver  │
│  (stores logs)  │                        │   (gets the alert)  │
└─────────────────┘                        └──────────┬──────────┘
                                                     │
                                                     ▼
Step 2: Healing                                 ┌─────────────────────┐
┌─────────────────────────────────────────┐     │      Ansible        │
│           Docker Container              │───► │  (does the fixing)  │
│  ✅ Started! / ❌ Restarted!            │     └─────────────────────┘
└─────────────────────────────────────────┘

Step 3: Notifying
┌─────────────────────────────────────────────────────────────────┐
│  Alertmanager  ──────►  Telegram Bot  ──────►  Your Phone 📱    │
└─────────────────────────────────────────────────────────────────┘
```

### Step-by-Step Story:

1. **Prometheus** checks on the Flask App every 10 seconds
2. If the Flask App is broken, Prometheus notices (`up{job="flask-app"} == 0`)
3. **Alertmanager** receives the "FlaskAppDown" alert
4. **Webhook Receiver** gets a message saying "Hey, Flask App is broken!"
5. **Ansible** runs a special script that:
   - Checks if the container is stopped
   - Starts (or restarts) the container
   - Waits for it to be healthy again
6. **Telegram Bot** sends you a message: "Fixed! Flask App is running again!"

---

## 📁 Project Structure (The Folder Map)

```
self-healing-infra/
│
├── 📁 prometheus/                    # The scorekeeper
│   ├── prometheus.yml               # What to watch
│   └── alert_rules.yml               # When to sound the alarm
│
├── 📁 grafana/                       # The picture painter
│   └── provisioning/
│       ├── datasources/             # Where to get data
│       └── dashboards/              # Pretty chart definitions
│
├── 📁 alertmanager/                  # The alarm manager
│   └── alertmanager.yml              # Who to call when things break
│
├── 📁 loki/                          # The log library
│   └── config.yml                    # How to store logs
│
├── 📁 promtail/                      # The log mail carrier
│   └── config.yml                    # Which logs to pick up
│
├── 📁 webhook-receiver/              # The fixer-bot messenger
│   ├── receiver.py                  # Catches alerts (the brain)
│   ├── Dockerfile                    # Package for shipping
│   └── requirements.txt              # Python helpers
│
├── 📁 ansible/                       # The healer
│   ├── playbook.yml                  # What to do to fix things
│   ├── inventory.ini                 # Who to fix
│   └── ansible.cfg                   # Settings
│
├── 📁 flask-app/                     # A test app (the patient)
│   ├── app.py                        # The actual app
│   ├── Dockerfile                    # Package for shipping
│   └── requirements.txt              # Python helpers
│
├── 📁 self-healing-task-manager/     # The main demo app
│   ├── docker-compose.yml            # How to run it
│   ├── 📁 backend/                   # The API server
│   │   ├── server.js                 # The brain
│   │   └── db.js                     # Database helper
│   ├── 📁 frontend/                  # The website
│   │   └── src/App.jsx              # The UI
│   └── 📁 postgres/                  # The data storage
│       └── init.sql                  # Create the tasks table
│
├── docker-compose.yml                # Main orchestra conductor
└── setup-network.sh                  # Sets up the network
```

---

## 🚀 How to Start Everything (The Magic Words)

### First Time Setup:

```bash
# 1. Create the shared network (so containers can talk)
./setup-network.sh

# 2. Start the monitoring stack (Prometheus, Grafana, etc.)
docker compose up -d

# 3. Start the task manager app
cd self-healing-task-manager
docker compose up -d
cd ..
```

### How to Access Everything:

| Service | URL | Username | Password |
|---------|-----|----------|----------|
| Grafana (Dashboards) | http://localhost:3001 | admin | admin |
| Prometheus (Metrics) | http://localhost:9090 | - | - |
| Alertmanager | http://localhost:9093 | - | - |
| Task Manager (Website) | http://localhost | - | - |
| Task Manager (API) | http://localhost:3000 | - | - |

---

## 🧪 How to Test the Self-Healing! (Fun Experiment)

Want to see the self-healing in action?

### Step 1: Start everything (as shown above)

### Step 2: Open Grafana
Go to http://localhost:3001 and login with `admin`/`admin`

### Step 3: Find a dashboard
Go to Dashboards → Task Manager to see metrics

### Step 4: Break the Flask App on purpose!
```bash
# Stop the flask app container
docker stop flask-app

# Watch it auto-heal! (should restart in ~30 seconds)
docker ps | grep flask-app
```

### Step 5: Check Telegram
You'll get a message like: "🔴 [firing] FlaskAppDown - Container flask-app is down!"

And then: "✅ [resolved] FlaskAppDown - Container flask-app is healthy again!"

---

## 🔧 Alert Rules (When Does the Alarm Sound?)

| Alert Name | What Triggers It | How Long | Severity | What Happens |
|------------|------------------|----------|----------|--------------|
| `TaskManagerDown` | Task manager stops responding | 30 sec | 🔴 Critical | Auto-heal via Ansible |
| `TaskManagerHigh5xxRate` | Too many errors (>5%) | 5 min | 🟡 Warning | Logs only |
| `PrometheusDown` | Prometheus stops | 30 sec | 🔴 Critical | Logs only |
| `AlertmanagerDown` | Alertmanager stops | 30 sec | 🔴 Critical | Logs only |
| `NodeExporterDown` | Node exporter stops | 30 sec | 🟡 Warning | Logs only |

---

## 📊 Grafana Dashboards Included

### 1. Task Manager Dashboard
Shows:
- ✅ Is the task manager alive?
- 📈 How many requests per second?
- ⏱️ How slow/fast is it? (latency)
- 🎯 Success rate percentage
- 📝 Number of tasks created
- 🔌 Database connection pool status

### 2. Logs Overview Dashboard
Shows:
- 📜 All logs from all containers
- Filterable by container name
- Searchable by text

---

## 🔌 API Endpoints

### Task Manager Backend (http://localhost:3000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/metrics` | Prometheus metrics |
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/:id` | Update a task |
| DELETE | `/tasks/:id` | Delete a task |

### Flask App (http://localhost:5000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Hello world |
| GET | `/health` | Health check |
| POST | `/simulate-load` | Create artificial load |

### Webhook Receiver (http://localhost:5001)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/webhook` | Receives Alertmanager alerts |
| GET | `/health` | Health check |

---

## 🗂️ Database Schema

The `tasks` table in PostgreSQL:

```sql
CREATE TABLE tasks (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    description TEXT,
    status      VARCHAR(50) DEFAULT 'pending',  -- pending, in-progress, done
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔐 Environment Variables

### Root Level (.env)
```env
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_ADMIN=your_telegram_chat_id
```

### Task Manager (.env)
```env
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=change_me_strong_password
POSTGRES_DB=tasks
DATABASE_URL=postgres://taskuser:change_me_strong_password@postgres:5432/tasks
BACKEND_PORT=3000
PG_POOL_MAX=10
```

---

## 🐛 Troubleshooting

### "Connection refused" errors
Make sure all containers are running:
```bash
docker compose ps
```

### "Network monitoring not found"
Run the setup script:
```bash
./setup-network.sh
```

### Self-healing not working
Check Ansible logs:
```bash
cat /tmp/ansible.log
```

### Check if Flask App is healthy:
```bash
curl http://localhost:5000/health
```

---

## 🎓 Key Concepts Explained Simply

### What is Prometheus?
Think of it like a teacher who asks every student "Are you okay?" every 10 seconds, and writes down their answers.

### What is Grafana?
Think of it like a report card that turns all those answers into pretty charts and graphs.

### What is Loki?
Think of it like a library that stores all the diary entries (logs) from every program.

### What is Alertmanager?
Think of it like a principal who decides what to do when a student says they're not okay - call the nurse? call parents? etc.

### What is Ansible?
Think of it like a janitor who can go around and restart broken computers.

### What is Docker?
Think of it like a box that contains everything a program needs to run, so it works the same everywhere.

### What is Docker Compose?
Think of it like instructions for how to arrange and connect multiple Docker boxes together.

---

## 📝 License

MIT
---

## 🙏 Credits

Built with ❤️ using Prometheus, Grafana, Loki, Alertmanager, Ansible, Flask, React, and Docker.
