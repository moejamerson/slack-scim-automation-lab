# Slack SCIM Automation Lab

**What it does**  
- **Onboard**: Create a user, set profile attributes, add to default groups (SCIM Groups)  
- **Offboard**: Deactivate a user
- **Cleanup**: Read audit events (Enterprise Grid only) and archive idle channels or remove deactivated users from groups

**Assumptions**  
- Slack token(s) provided via env:
  - `SLACK_SCIM_TOKEN` (SCIM bearer; requires SCIM scope)
  - `SLACK_BOT_TOKEN` (for Web API cleanup, e.g., conversations.*)
  - `SLACK_AUDIT_TOKEN` (Enterprise Grid Audit Logs)
- Default groups exist (e.g., `onboarding`, `engineering`)

**Run**
```bash
python scim_lifecycle.py --onboard --email "new.user@example.com" --name "New User"
python scim_lifecycle.py --offboard --email "new.user@example.com"
python cleanup.py --archive-idle --days 90
```

