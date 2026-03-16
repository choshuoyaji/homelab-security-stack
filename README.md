# 🔒 Home Lab Security Stack

A complete, production-grade security monitoring and response stack built entirely in a home lab environment. This repository contains all the configurations, detection rules, automation playbooks, and infrastructure-as-code used in my [Medium articles](https://takahiro-oda.medium.com) and [dev.to posts](https://dev.to/t_o_jp).

![Security Stack](https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Home Lab Network                   │
├─────────────┬──────────────┬────────────────────────┤
│  Endpoints  │   Cloud      │    Infrastructure       │
│  ─────────  │   ─────      │    ──────────────       │
│  Wazuh Agent│   AWS        │    EKS Cluster          │
│  CrowdStrike│   CloudTrail │    EC2 Instances        │
│  Falcon     │   GuardDuty  │    On-prem VMs          │
└──────┬──────┴──────┬───────┴──────────┬─────────────┘
       │             │                  │
       ▼             ▼                  ▼
┌─────────────────────────────────────────────────────┐
│                  SIEM (Splunk)                        │
│              Sigma Rules → SPL Queries                │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              SOAR (Shuffle + n8n)                     │
│           CACAO v2.0 Playbooks                        │
│                                                       │
│  ┌───────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Enrichment│  │ Decision │  │ Response Actions  │  │
│  │ - AbuseIP │  │ - AI     │  │ - Block IP (WAF) │  │
│  │ - VT      │  │   Triage │  │ - Isolate Host   │  │
│  │ - MITRE   │  │ - Rules  │  │ - Create Ticket  │  │
│  └───────────┘  └──────────┘  │ - Slack Alert    │  │
│                                └──────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## 📁 Repository Structure

```
homelab-security-stack/
├── sigma-rules/              # Custom Sigma detection rules
│   ├── cloud/                # AWS CloudTrail, GuardDuty rules
│   ├── endpoint/             # EDR, process creation rules
│   ├── network/              # Network traffic rules
│   └── identity/             # IAM, authentication rules
├── playbooks/                # CACAO v2.0 SOAR playbooks
│   ├── incident-response/    # IR playbooks
│   ├── enrichment/           # Threat intel enrichment
│   └── remediation/          # Auto-remediation actions
├── enrichment/               # Threat intelligence scripts
│   ├── ip_reputation.py
│   ├── ai_triage.py
│   └── mitre_mapper.py
├── infrastructure/           # Infrastructure as Code
│   ├── docker-compose.yml    # Local stack deployment
│   ├── terraform/            # AWS infrastructure
│   └── ansible/              # Configuration management
├── ci-cd/                    # CI/CD pipeline configs
│   ├── sigma-validation.yml
│   └── playbook-ci.yml
└── docs/                     # Documentation
    ├── setup-guide.md
    └── troubleshooting.md
```

## 🛠️ Stack Components

| Component | Tool | Purpose |
|-----------|------|---------|
| SIEM | Splunk (dev license) | Log aggregation & detection |
| EDR | CrowdStrike Falcon + Wazuh | Endpoint monitoring |
| SOAR | Shuffle + n8n | Orchestration & automation |
| Cloud | AWS (CloudTrail, GuardDuty) | Cloud security monitoring |
| CNAPP | Wiz | Cloud-native app protection |
| Ticketing | Jira | Incident tracking |
| Detection | Sigma Rules | Portable detection logic |
| Playbooks | CACAO v2.0 | Standardized response |

## 📚 Related Articles

### Detection Engineering Series
- **Series 1**: [Building 20+ Sigma Rules for Multi-Source Threat Detection](https://takahiro-oda.medium.com/detection-engineering-in-my-home-lab-series-1-building-20-sigma-rules-for-multi-source-threat-614015b067e8) ([dev.to mirror](https://dev.to/t_o_jp/detection-engineering-in-my-home-lab-series-1-building-20-sigma-rules-for-multi-source-threat-43el))

### SOAR Series
- **Series 1**: Building an Automated Incident Response Pipeline from Scratch (coming soon)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/choshuoyaji/homelab-security-stack.git
cd homelab-security-stack

# Deploy the local stack
docker-compose up -d

# Validate Sigma rules
python3 ci-cd/validate_sigma.py sigma-rules/

# Test playbooks
python3 -m pytest tests/playbook_tests/ -v
```

## 🎯 MITRE ATT&CK Coverage

Current detection coverage across techniques:

- **Credential Access** — T1003, T1078, T1110
- **Lateral Movement** — T1021, T1570
- **Defense Evasion** — T1562, T1070
- **Initial Access** — T1190, T1133
- **Execution** — T1059, T1204

Coverage improved from ~15% to ~45% of relevant techniques.

## 📊 Results

| Metric | Before | After |
|--------|--------|-------|
| MITRE ATT&CK Coverage | ~15% | ~45% |
| Mean Time to Detect | Hours | Minutes |
| Alert Triage Time | 15 min | < 2 min |
| Detection Rules | 5 | 20+ |
| Automated Playbooks | 0 | 8 |

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting PRs.

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

## 👤 Author

**Takahiro Oda**
- Medium: [@takahiro-oda](https://takahiro-oda.medium.com)
- dev.to: [@t_o_jp](https://dev.to/t_o_jp)
- GitHub: [@choshuoyaji](https://github.com/choshuoyaji)