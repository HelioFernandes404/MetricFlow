# MetricFlow - DevOps Platform Demo

A comprehensive DevOps platform demonstrating modern infrastructure automation, CI/CD, and observability practices. This project showcases all the technologies mentioned in the DevOps stakeholder requirements.

## 🚀 Features

- **Python Flask Application** with Prometheus metrics integration
- **Docker Containerization** with security best practices
- **Kubernetes Orchestration** with HPA and auto-scaling
- **Terraform Infrastructure** for AWS EKS, VPC, and RDS
- **GitHub Actions CI/CD** with automated testing and deployment
- **ArgoCD GitOps** for continuous deployment
- **Prometheus & Grafana** monitoring stack
- **Ansible Automation** for configuration management

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      GitHub Actions CI/CD                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │    Test     │ │   Build     │ │       Deploy            │ │
│  │  & Lint     │ │   Docker    │ │    (ArgoCD GitOps)      │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    AWS EKS Cluster                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │   MetricFlow│ │    Redis    │ │      Monitoring         │ │
│  │     App     │ │   Cache     │ │  (Prometheus/Grafana)   │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
│                              │                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                  RDS PostgreSQL                        │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| **Application** | Python, Flask, Gunicorn |
| **Containerization** | Docker, Docker Compose |
| **Orchestration** | Kubernetes, Helm |
| **Infrastructure** | Terraform, AWS (EKS, VPC, RDS) |
| **CI/CD** | GitHub Actions |
| **GitOps** | ArgoCD |
| **Monitoring** | Prometheus, Grafana |
| **Configuration** | Ansible |
| **Security** | Trivy, Fail2ban, UFW |

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- kubectl and Helm
- Terraform >= 1.0
- Ansible >= 2.9
- AWS CLI configured
- Python 3.11+

### Local Development

```bash
# Clone the repository
git clone https://github.com/your-username/MetricFlow.git
cd MetricFlow

# Install Python dependencies
pip install -r requirements.txt

# Run locally
python src/app.py

# Or with Docker
docker build -t metricflow .
docker run -p 8080:8080 metricflow
```

### Infrastructure Deployment

```bash
# Deploy AWS infrastructure
cd terraform/aws
terraform init
terraform plan -var="db_password=secure_password"
terraform apply

# Configure infrastructure with Ansible
cd ../../ansible
ansible-playbook -i inventory/hosts.yml playbooks/site.yml
```

### Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Or use ArgoCD for GitOps
kubectl apply -f argocd/
```

## 📊 Monitoring

The platform includes comprehensive monitoring with:

- **Application Metrics**: Custom business metrics via `/metrics` endpoint
- **System Metrics**: CPU, memory, disk usage via Node Exporter
- **Container Metrics**: Docker and Kubernetes metrics
- **Infrastructure Metrics**: AWS CloudWatch integration

### Key Dashboards

- Application Performance Dashboard
- Infrastructure Health Dashboard
- Security and Compliance Dashboard

## 🔒 Security Features

- Container vulnerability scanning with Trivy
- Network security policies
- SSH hardening and fail2ban
- Audit logging and compliance monitoring
- Secrets management with encryption
- RBAC and service accounts

## 🔄 CI/CD Pipeline

The GitHub Actions pipeline includes:

1. **Code Quality**
   - Linting with flake8
   - Code formatting with black
   - Unit testing with pytest

2. **Security Scanning**
   - Container vulnerability scanning
   - Dependency scanning
   - Static code analysis

3. **Build & Deploy**
   - Multi-architecture Docker builds
   - Automated deployment to staging
   - Production deployment with approval

## 📝 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/health` | Health check |
| `/metrics` | Prometheus metrics |
| `/api/metrics/system` | System metrics |
| `/api/metrics/history` | Historical metrics |
| `/api/status` | Application status |

## 🧪 Testing

```bash
# Run unit tests
pytest --cov=src --cov-report=html

# Run integration tests
pytest tests/integration/

# Security testing
trivy fs .

# Load testing
kubectl apply -f tests/load-test.yaml
```

## 📚 Documentation

- [Architecture Decisions](docs/decisions.md)
- [Development Workflow](docs/todo.md)
- [Stakeholder Requirements](docs/stackholder.md)
- [LLM Integration Guide](docs/llm.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check existing documentation
- Review architecture decisions

---

**MetricFlow** - Demonstrating modern DevOps practices with real-world technologies and patterns.