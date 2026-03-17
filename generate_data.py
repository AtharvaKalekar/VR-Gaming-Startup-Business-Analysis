import pandas as pd
import numpy  as np
import uuid, random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

NUM_USERS       = 40000          # onboarded in Year 1
NUM_SAMPLE      = 2000           # rows in session dataset (representative sample)
GENRES          = ['Action', 'Adventure', 'Simulation', 'Multiplayer']
START_DATE      = datetime(2025, 1, 1)

def random_timestamp(start: datetime, days: int = 365) -> datetime:
    return start + timedelta(
        days=random.randint(0, days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )

print("Generating Gaming Session Dataset")

sessions = []

for _ in range(NUM_SAMPLE):

    user_id   = f'USER_{random.randint(1, NUM_USERS):05d}'
    genre     = random.choice(GENRES)
    timestamp = random_timestamp(START_DATE)

    # Session duration: 20–120 min (log-normal, mean ~45 min)
    session_min = round(max(10, min(180, np.random.lognormal(mean=3.8, sigma=0.5))), 1)

    # Engagement rate 0–1 (beta distribution, skewed high)
    engagement = round(min(1.0, max(0.0, np.random.beta(a=6, b=2))), 3)

    # Game completion rate 0–1
    completion = round(min(1.0, max(0.0, np.random.beta(a=5, b=3))), 3)

    # System performance flag (99.5 % uptime)
    lag_event = np.random.choice([True, False], p=[0.005, 0.995])

    # fps: mostly 60–90 fps, occasional drops
    fps = round(max(20, np.random.normal(loc=75, scale=8)), 1)

    sessions.append({
        'session_id'       : str(uuid.uuid4()),
        'user_id'          : user_id,
        'genre'            : genre,
        'timestamp'        : timestamp.strftime('%Y-%m-%d %H:%M'),
        'session_min'      : session_min,       # Variable 1 — session duration
        'engagement_rate'  : engagement,        # Variable 2 — engagement rate
        'game_completion'  : completion,        # Variable 3 — game completion rate
        'fps'              : fps,               # Variable 4 — frames per second
        'lag_event'        : lag_event,         # Variable 5 — performance issue flag
    })

df_sessions = pd.DataFrame(sessions)
print(f"   Done — {len(df_sessions):,} session records created.")

print("Generating System Monitoring Dataset  (365 daily records)")

monitoring = []

for i in range(365):
    date = (START_DATE + timedelta(days=i)).strftime('%Y-%m-%d')

    uptime = round(
        max(98.5, min(100.0, 100 - abs(np.random.normal(loc=0, scale=0.15)))), 4
    )

    avg_fps = round(max(40, np.random.normal(loc=74, scale=5)), 1)

    crash_reports  = max(0, int(np.random.poisson(lam=3)))
    server_load    = round(min(1.0, max(0.0, np.random.beta(a=4, b=3))), 3)   # 0-1
    support_tickets = max(0, int(np.random.poisson(lam=8)))

    status = 'ALERT' if (uptime < 99.0 or crash_reports > 10) else 'Normal'

    monitoring.append({
        'date'           : date,
        'uptime_pct'     : uptime,
        'avg_fps'        : avg_fps,
        'crash_reports'  : crash_reports,
        'server_load'    : server_load,
        'support_tickets': support_tickets,
        'status'         : status,
    })

df_monitor = pd.DataFrame(monitoring)
print(f"   Done — {len(df_monitor):,} daily records created.")

print("Generating CRM & User Satisfaction Dataset  (1,000 users)")

NUM_CRM = 1000
crm = []

for i in range(1, NUM_CRM + 1):
    genre = random.choice(GENRES)
    months = random.randint(1, 12)

    satisfaction = round(
        max(1.0, min(10.0, np.random.normal(loc=7.8, scale=1.0))), 1
    )

    tickets   = max(0, int(np.random.poisson(lam=1.5)))

    # Renewal probability rises with satisfaction
    renewal_p = round(max(0.05, min(0.99, 0.4 + (satisfaction - 5) * 0.08)), 2)

    # CLV = 3 * (1 + satisfaction / 10)  [in thousands of INR]
    clv_k = round(3 * (1 + satisfaction / 10), 2)

    if satisfaction >= 8.0:
        churn_risk = 'LOW'
    elif satisfaction >= 6.5:
        churn_risk = 'MEDIUM'
    else:
        churn_risk = 'HIGH'

    crm.append({
        'user_id'             : f'USER_{i:05d}',
        'genre'               : genre,
        'subscription_months' : months,
        'satisfaction_score'  : satisfaction,
        'support_tickets'     : tickets,
        'renewal_probability' : renewal_p,
        'clv_k_inr'           : clv_k,          # in thousands of INR
        'churn_risk'          : churn_risk,
    })

df_crm = pd.DataFrame(crm)
print(f"   Done — {len(df_crm):,} user CRM records created.")

df_sessions.to_csv('vrgames_sessions.csv',  index=False)
df_monitor.to_csv( 'vrgames_monitoring.csv', index=False)
df_crm.to_csv(     'vrgames_crm.csv',        index=False)

print("\n  All 3 CSV files saved successfully!")
