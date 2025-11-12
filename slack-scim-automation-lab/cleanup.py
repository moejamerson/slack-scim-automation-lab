#!/usr/bin/env python3
import os, time, argparse, requests

AUDIT_BASE = "https://api.slack.com/audit/v1"
WEB_BASE   = "https://slack.com/api"
AUDIT_HEADERS = {"Authorization": f"Bearer {os.environ.get('SLACK_AUDIT_TOKEN')}"}
WEB_HEADERS   = {"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"}

def archive_idle(days=90):
    r = requests.get(f"{WEB_BASE}/conversations.list?limit=500&types=public_channel", headers=WEB_HEADERS)
    # Example placeholder: decide which channels to archive by inspecting recent history
    print(f"[OK] Retrieved channel list; implement idle>{days}d filter and call conversations.archive")

def list_recent_admin_events():
    r = requests.get(f"{AUDIT_BASE}/logs?limit=100", headers=AUDIT_HEADERS)
    r.raise_for_status()
    for ev in r.json().get("events", []):
        print(f"{ev['date_create']}: {ev['action']} actor={ev['actor'].get('user_id','?')}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive-idle", action="store_true")
    ap.add_argument("--days", type=int, default=90)
    args = ap.parse_args()
    if args.archive_idle:
        archive_idle(args.days)
    else:
        list_recent_admin_events()
