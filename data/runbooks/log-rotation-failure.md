# Log rotation failure

## Symptoms
- A single log file grows very large, for example several gigabytes.
- Old logs are not compressed or archived.
- Disk usage on /var/log keeps increasing.

## Checks
- Find large logs: `ls -lh /var/log` or `du -sh /var/log/*`.
- Check the logrotate configuration in `/etc/logrotate.conf` and `/etc/logrotate.d/`.
- Test the configuration without changing anything: `logrotate -d /etc/logrotate.conf`.
- Check whether the logrotate job runs (cron or systemd timer).

## Fix
- Fix syntax errors or wrong paths in the logrotate configuration.
- Run rotation manually once: `logrotate -f /etc/logrotate.conf`.
- Make sure the application reopens its log file after rotation (`copytruncate` or a reload).
- Compress and archive old logs to free space.

## Escalation
- Disk close to full because of logs: also follow the disk full runbook.
- Application cannot release its log file: escalate to the application owner.
