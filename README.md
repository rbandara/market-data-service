# Market Data Service (Real-Time Ingestion on K3s)

This project sets up a real-time market data ingestion pipeline using Redis and TimescaleDB, deployed on a lightweight K3s Kubernetes cluster. It uses **Terraform** to provision infrastructure (if needed), and **Ansible** for post-deployment configuration. **Helm** is used to install components on Kubernetes.

---

## 📁 Project Structure

market-data-service/
├── ansible/ # Ansible playbooks for config tasks
│ ├── inventory.ini
│ └── playbook.yml
├── database/ # DB schema, seed data, or migrations
├── docker/ # Dockerfiles or docker-compose (optional)
├── k8-manifests/ # Custom K8s manifests (if not using Helm)
├── redis-consumer/ # Redis consumer microservice
├── terraform/ # Terraform modules (optional if using EC2)
├── websocket-listener/ # WebSocket tick ingestor service
├── provision.sh # Shell script to kickstart provisioning
└── README.md # You're here!



---

## 🚀 Setup Guide

### 1. Prerequisites

- [Ansible](https://docs.ansible.com/)
- [Terraform](https://www.terraform.io/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [K3s](https://k3s.io/)
- [Helm](https://helm.sh/)
- SSH access to K3s nodes (local or remote)

---

## 🛠 Provisioning & Configuration

### Step 1: Provision Infrastructure (Optional)


```bash
cd terraform
terraform init
terraform apply
```

This creates EC2 instances or desired infra with necessary security groups.


Step 2: Configure K3s Cluster with Ansible
Update your ansible/inventory.ini with your K3s node IPs:

```
[k3s]
192.168.1.100 ansible_user=ubuntu


Run the playbook:

```
cd ansible
ansible-playbook -i inventory.ini playbook.yml


This will:

Install TimescaleDB on K3s (via Helm)

Install Redis on K3s (via Helm)

Setup required namespaces, PVCs, configs


Step 3: Deploy Microservices

If you’re using Helm:

```
helm install redis oci://registry-1.docker.io/bitnamicharts/redis
helm install timescaledb oci://registry-1.docker.io/bitnamicharts/postgresql

```

If you're using raw K8s manifests:

kubectl apply -f k8-manifests/



Microservices Overview
websocket-listener
Connects to market data feed

Publishes ticks to Redis Streams

redis-consumer
Subscribes to Redis stream

Stores market ticks into TimescaleDB




### 🧱 Deployment Approach

| Component     | Tool      | Approach                                    |
|---------------|-----------|---------------------------------------------|
| Redis         | Ansible   | Installed directly on k3s nodes             |
| TimescaleDB   | Ansible   | Installed directly on k3s nodes             |
| Prometheus    | Helm      | Installed via Helm charts in Kubernetes     |
| Grafana       | Helm      | Installed via Helm charts in Kubernetes     |
| Provisioning  | Terraform | Provisions EC2, networking, etc.            |
| Configuration | Ansible   | Configures nodes, installs base software    |





## Useful commands

### View pods
kubectl get pods -A

### Port-forward TimescaleDB
kubectl port-forward svc/timescaledb 5432:5432 -n <namespace>

### Access Redis CLI
kubectl exec -it <redis-pod> -- redis-cli

