# Server clock out of sync (time drift)

## Symptoms
- Log timestamps do not match other servers.
- Authentication or certificate errors caused by time differences.
- Alert: NTP offset larger than the allowed threshold.

## Checks
- Run `timedatectl` and check "System clock synchronized".
- With chrony, run `chronyc tracking` and `chronyc sources`.
- With ntpd, run `ntpq -p` to see the time sources and offset.
- Confirm the server can reach its NTP servers on UDP port 123.

## Fix
- Restart the time service: `systemctl restart chronyd` (or `ntpd`).
- Force a correction with `chronyc makestep` if the offset is large.
- Fix firewall rules if NTP traffic is blocked.
- Make sure all servers use the same approved time sources.

## Escalation
- Time drift on trading or financial systems: escalate immediately, as timestamps may have regulatory impact.
- NTP servers themselves unreachable: escalate to the network team.
