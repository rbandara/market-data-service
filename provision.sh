#!/bin/bash
cd terraform
terraform init
terraform apply -auto-approve

cd ../ansible
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory.ini playbook.yml
