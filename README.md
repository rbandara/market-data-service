# market-data-service

Projecgt Structure

k3s-ec2/
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars
├── ansible/
│   ├── inventory.ini        # populated by Terraform output
│   └── playbook.yml         # installs k3s
├── provision.sh             # wrapper to run everything
