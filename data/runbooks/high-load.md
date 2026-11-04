# High load average

## Symptoms
- Alert: load average higher than the number of CPU cores.
- System responds slowly even when CPU usage looks moderate.
- Commands such as `ls` take a long time to return.

## Checks
- Run `uptime` and compare the load with the core count from `nproc`.
- Run `top` and check the `wa` (I/O wait) value; high wait means processes are waiting on disk.
- Run `iostat -x 1 5` to find a busy or slow disk.
- Look for processes in state "D" (uninterruptible sleep): `ps -eo state,pid,cmd | grep "^D"`.

## Fix
- If I/O wait is high, find the process causing heavy disk activity and reduce or reschedule it.
- If CPU bound, follow the high CPU runbook.
- Check for a failing disk or storage path and move the workload if needed.
- Reduce the number of parallel jobs on the host.

## Escalation
- Storage latency suspected: escalate to the storage team.
- Load stays high with no clear cause: raise a problem ticket.
