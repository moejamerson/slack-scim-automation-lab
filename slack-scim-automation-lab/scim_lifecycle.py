#!/usr/bin/env python3
import os, sys, json, argparse, requests

SCIM_BASE = "https://api.slack.com/scim/v1"
HEADERS = {"Authorization": f"Bearer {os.environ.get('SLACK_SCIM_TOKEN')}", "Content-Type": "application/json"}

def scim_get_user_id_by_email(email):
    r = requests.get(f"{SCIM_BASE}/Users?filter=userName eq \"{email}\"", headers=HEADERS)
    r.raise_for_status()
    res = r.json()
    if res.get("Resources"):
        return res["Resources"][0]["id"]
    return None

def onboard(email, name, groups):
    payload = {
        "userName": email,
        "name": {"givenName": name.split()[0], "familyName": name.split()[-1]},
        "active": True,
        "emails": [{"value": email, "primary": True}]
    }
    r = requests.post(f"{SCIM_BASE}/Users", headers=HEADERS, data=json.dumps(payload))
    r.raise_for_status()
    user = r.json()
    print(f"[OK] Created user {email} (id: {user['id']})")

    for g in groups:
        gr = requests.get(f"{SCIM_BASE}/Groups?filter=displayName eq \"{g}\"", headers=HEADERS)
        gr.raise_for_status()
        gres = gr.json()
        if not gres.get("Resources"):
            print(f"[WARN] Group '{g}' not found")
            continue
        gid = gres["Resources"][0]["id"]
        patch = {
          "Operations": [{
            "op": "Add",
            "path": "members",
            "value": [{"value": user["id"]}]
          }]
        }
        pr = requests.patch(f"{SCIM_BASE}/Groups/{gid}", headers=HEADERS, data=json.dumps(patch))
        pr.raise_for_status()
        print(f"[OK] Added {email} to group '{g}'")

def offboard(email):
    uid = scim_get_user_id_by_email(email)
    if not uid:
        print(f"[INFO] User {email} not found")
        return
    r = requests.patch(f"{SCIM_BASE}/Users/{uid}", headers=HEADERS,
                       data=json.dumps({"Operations":[{"op":"Replace","path":"active","value":False}]}))
    r.raise_for_status()
    print(f"[OK] Deactivated {email}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--onboard", action="store_true")
    ap.add_argument("--offboard", action="store_true")
    ap.add_argument("--email", required=True)
    ap.add_argument("--name", default="New User")
    ap.add_argument("--groups", nargs="*", default=["onboarding"])
    args = ap.parse_args()

    if args.onboard:
        onboard(args.email, args.name, args.groups)
    elif args.offboard:
        offboard(args.email)
    else:
        print("Specify --onboard or --offboard")
        sys.exit(1)
