# SSH brute-force attack

## Symptoms
- Hundreds of "Failed password" or "Invalid user" lines in the auth log.
- Many login attempts from one or a few IP addresses in a short time.
- Security alert for repeated authentication failures.

## Checks
- Count failures: `grep "Failed password" /var/log/auth.log | wc -l` (or /var/log/secure).
- Find the top source IPs: `grep "Failed password" /var/log/auth.log | grep -oE "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" | sort | uniq -c | sort -rn | head`.
- Check whether any login succeeded from those IPs: `grep "Accepted" /var/log/auth.log`.
- Confirm whether SSH is exposed to the internet.

## Fix
- Block the attacking IPs with the firewall or fail2ban.
- Disable password login and allow SSH keys only.
- Disable direct root login over SSH.
- Restrict SSH access to VPN or known IP ranges.

## Escalation
- Any successful login from an attacking IP: escalate to the security team immediately as a possible breach.
- Ongoing large-scale attack: inform the security and network teams.
