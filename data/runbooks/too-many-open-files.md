# Too many open files

## Symptoms
- Errors such as "Too many open files" or "EMFILE" in application logs.
- The application stops accepting new connections.
- Failures appear under high traffic.

## Checks
- Check the process limit: `cat /proc/<pid>/limits | grep "open files"`.
- Count the files the process has open: `ls /proc/<pid>/fd | wc -l` or `lsof -p <pid> | wc -l`.
- Check the system-wide limit: `cat /proc/sys/fs/file-max`.
- Look for a file or connection leak: a count that keeps growing over time.

## Fix
- Restart the application to release open files as a quick recovery.
- Raise the limit in the systemd unit (`LimitNOFILE=`) or in `/etc/security/limits.conf`.
- Report a suspected file or connection leak to the developers.
- Monitor the open file count after the change.

## Escalation
- Limit already high and still exhausted: escalate to the application team for a leak investigation.
