# Disk full on Linux server

## Symptoms
- Alert: filesystem usage above 90%.
- Errors such as "No space left on device".
- Applications fail to write logs or temporary files.

## Checks
- Run `df -h` to see which filesystem is full.
- Run `du -sh /var/* | sort -h` to find large folders.
- Find large log files: `find /var/log -size +500M`.
- Check for deleted files still held open: `lsof +L1`.

## Fix
- Compress or delete old rotated logs in /var/log.
- Clear temporary files in /tmp if safe.
- Restart the process holding deleted files to release the space.
- If usage is still high, extend the volume or add disk.

## Escalation
- Production database disk above 95%: escalate to the DBA team immediately.
- Volume cannot be extended: raise a change request with the infrastructure team.
