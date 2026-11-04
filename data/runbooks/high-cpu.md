# High CPU usage

## Symptoms
- Alert: CPU utilisation above 90% for more than 5 minutes.
- Slow application response and request timeouts.
- Users report the system feels sluggish.

## Checks
- Run `top` or `htop` and sort by CPU to find the busiest processes.
- Run `ps aux --sort=-%cpu | head` to list the top consumers.
- Check whether the load matches a scheduled job, deployment or traffic spike.
- Use `pidstat 1 5` to watch a process's CPU over time.

## Fix
- If a runaway or stuck process is found, restart it gracefully.
- Reschedule heavy batch jobs to off-peak hours.
- Scale out the service or add CPU if the load is genuine traffic.
- Roll back a recent deployment if it introduced the spike.

## Escalation
- CPU saturated on a production trading or customer-facing host: escalate to the application owner.
- Repeated spikes with no clear cause: raise a problem ticket for root cause analysis.
