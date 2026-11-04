# High memory usage and OOM killer

## Symptoms
- Alert: memory usage above 90% or swap usage growing.
- Processes killed unexpectedly; "Out of memory: Killed process" in the kernel log.
- Application crashes or restarts without an obvious error.

## Checks
- Run `free -h` to see used, available and swap memory.
- Run `ps aux --sort=-%mem | head` to find the largest processes.
- Search for OOM events: `dmesg -T | grep -i "killed process"` or `journalctl -k | grep -i oom`.
- Check whether memory grows steadily over days, which suggests a memory leak.

## Fix
- Restart the process that is leaking memory to recover quickly.
- Reduce the cache or heap size settings if they are too large.
- Add memory or move the workload to a larger host.
- Report suspected leaks to the development team with memory graphs.

## Escalation
- OOM kills on production services: escalate to the application owner.
- Memory leak confirmed: raise a defect with the development team.
