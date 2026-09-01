# Empire WAF — Configuration Reference
# Provider: AWS WAF + CloudFront, GCP Cloud Armor, DigitalOcean Cloud Firewall, iptables (local)
#
# For each of the 45 regional hubs + Synthesis L2 Aggregator:
#   - AWS: AWS WAF Web ACL + CloudFront distribution
#   - GCP: Cloud Armor Security Policy
#   - DigitalOcean: Cloud Firewall rules
#   - Local: iptables (empire_waf.sh)

# ─────────────────────────────────────────────────────────────────────────────
# RULE 1: Rate Limiting
# ─────────────────────────────────────────────────────────────────────────────
# HTTP/S requests per IP: 1000 per 5 min → block 15 min
# Authenticated API calls per IP: 5000 per 5 min → block 15 min
# Health check endpoints: unlimited

# ─────────────────────────────────────────────────────────────────────────────
# RULE 2: Geo-Blocking
# ─────────────────────────────────────────────────────────────────────────────
# Block: North Korea (KP), Iran (IR), Syria (SY), Cuba (CU), Russia (RU) partial
# Allow: all other countries (bio-finance data is global)
# Custom: force reCAPTCHA for high-risk regions

# ─────────────────────────────────────────────────────────────────────────────
# RULE 3: SQLi / XSS Protection
# ─────────────────────────────────────────────────────────────────────────────
# Block requests matching:
#   SQL keywords: UNION, SELECT, INSERT, DROP, --, '; 
#   XSS patterns: <script>, javascript:, <iframe>, onerror=
#   Path traversal: ../, /etc/passwd, cmd=, 
#   Command injection: |, ;, &, $(), ``

# ─────────────────────────────────────────────────────────────────────────────
# RULE 4: Allowed Traffic Profiles
# ─────────────────────────────────────────────────────────────────────────────
# ONLY sovereign orchestration traffic allowed:
#   - Spacelift worker IPs: registered worker pools only
#   - Inter-hub: 168.1.0.0/16 (internal empire network)
#   - Synthesis L2 Aggregator: 168.1.255.255 (central)
#   - Public HTTP/S: 443 (TLS), 8443 (internal API)
#   - SSH: 22 (allowlisted to 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 only)

# ─────────────────────────────────────────────────────────────────────────────
# RULE 5: DDoS Mitigation
# ─────────────────────────────────────────────────────────────────────────────
# AWS: AWS WAF bot control + rate-based rules
#   - Challenge/bypass for suspicious bots
#   - CAPTCHA for automated scanners
# GCP: Cloud Armor Adaptive Protection (ML-based)
# DigitalOcean: automatic DDoS mitigation (always-on)

# ─────────────────────────────────────────────────────────────────────────────
# RULE 6: Explicit Block Rules
# ─────────────────────────────────────────────────────────────────────────────
# Block:
#   - Port 80 (force redirect to 443)
#   - SSH from non-private ranges
#   - Raw ICMP from external sources
#   - Known scanning / reconnaissance tool User-Agents
#   - SSH brute-force: 5 failures / 60s → 15 min block

# ─────────────────────────────────────────────────────────────────────────────
# Per-Provider Configuration
# ─────────────────────────────────────────────────────────────────────────────

# AWS — Web ACL: empire-global-waf
#   Associated resources: all 16 AWS CloudFront distributions
#   Rules: see above (OWASP CRS v3.x)
#   Logs: CloudWatch Logs → S3 → SIEM

# GCP — Security Policy: empire-hub-defensive
#   Associated: all 15 GCP backend services
#   Rules: Cloud Armor preconfigured rules + custom
#   Adaptive Protection: ON (ML-based DDoS detection)

# DigitalOcean — Cloud Firewall: empire-node-00
#   Inbound:
#     - Allow: TCP 22 (from 10.0.0.0/8 only)
#     - Allow: TCP 443 (all)
#     - Allow: TCP 8443 (from 168.1.0.0/16)
#     - Allow: ICMP (rate-limited)
#     - Drop: all else
#   Applied to: all 15 DigitalOcean droplets