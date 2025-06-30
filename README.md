<<<<<<< HEAD
 Stage 1: Provision + Base Cluster (Your Current provision.sh)
Terraform creates EC2

Ansible installs k3s

✅ At the end of this step, you should be able to:

SSH into EC2

Run kubectl get nodes

Verify k3s is running

Stage 2: Install Core Services (Optional Separate Script or Step)
Use Helm or kubectl to install:

✅ Redis

✅ Prometheus + Grafana

✅ Cert Manager (if needed)

✅ Ingress (like NGINX)

This can be:

bash
Copy
Edit
./install-core-services.sh
Inside that script:

bash
Copy
Edit
# Add Helm repos
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# Install Redis
helm install redis bitnami/redis

# Install Prometheus + Grafana
helm install kube-prometheus prometheus-community/kube-prometheus-stack
🛠️ Stage 3: Deploy Your Apps
Your WebSocket listener

Any Python consumers

Database writer

Web front-end if needed

Use Helm charts or simple YAML manifests.

📦 Option: Group with kustomize or Helmfile
If you want to automate the stack later:

Use kustomize to group apps into environments

Use helmfile to declaratively install Helm charts


