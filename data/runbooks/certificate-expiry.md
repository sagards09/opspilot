# SSL/TLS certificate expiry

## Symptoms
- Browsers show "Your connection is not private" or a certificate expired warning.
- API clients fail with TLS handshake or certificate validation errors.
- Alert: certificate expires in fewer than 30 days.

## Checks
- Check the expiry date of a live site: `echo | openssl s_client -connect <host>:443 2>/dev/null | openssl x509 -noout -dates`.
- Check a certificate file: `openssl x509 -in cert.pem -noout -enddate`.
- Confirm which servers and load balancers use the certificate.
- Check that the full certificate chain is installed.

## Fix
- Request or renew the certificate from the certificate authority.
- Install the new certificate and chain on every server that uses it.
- Reload the web server or load balancer, for example `systemctl reload nginx`.
- Verify the new expiry date with the openssl check.

## Escalation
- Certificate already expired on a customer-facing service: open a major incident.
- Certificate managed by another team or vendor: escalate to the certificate owner.
