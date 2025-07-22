#!/bin/bash

cd terraform
terraform init
terraform apply -auto-approve

# Extract IP
IP=$(terraform output -raw k3s_ip)

cd ../ansible
echo "[k3s]" > inventory.ini
echo "ec2-user@$IP" >> inventory.ini

ansible-playbook -i inventory.ini playbook.yml
