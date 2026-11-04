# Service down or crashed

## Symptoms
- Alert: health check failing or port not responding.
- Users receive connection refused or HTTP 502/503 errors.
- Monitoring shows the process is not running.

## Checks
- Run `systemctl status <service>` to see whether it is running and why it stopped.
- Read recent logs: `journalctl -u <service> -n 100`.
- Check whether the port is listening: `ss -tlnp | grep <port>`.
- Check for dependency failures such as the database, disk space or configuration errors.

## Fix
- Fix the cause shown in the logs, for example a config typo or a full disk.
- Validate configuration before restarting, for example `nginx -t`.
- Restart the service: `systemctl restart <service>`.
- Confirm it is healthy again with the health check URL or port test.

## Escalation
- Service will not start after a restart: escalate to the application owner.
- Customer-facing outage: open a major incident and follow the incident process.
