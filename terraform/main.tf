provider "aws" {
  region = "us-east-1"
}

resource "aws_key_pair" "k3s_key" {
  key_name   = "k3s-key"
  public_key = file("~/.ssh/k3s-key.pub")
}

resource "aws_security_group" "k3s_sg" {
  name        = "k3s-sg"
  description = "Allow SSH and k3s traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 6443
    to_port     = 6443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "k3s_node" {
  ami                    = "ami-0c101f26f147fa7fd"  # Amazon Linux 2023 x86_64
  instance_type          = "t3.micro"
  key_name               = aws_key_pair.k3s_key.key_name
  security_groups        = [aws_security_group.k3s_sg.name]

  tags = {
    Name = "k3s-node"
  }

  provisioner "local-exec" {
    command = "echo '${self.public_ip}' > ../ansible/inventory.ini"
  }
}

output "public_ip" {
  value = aws_instance.k3s_node.public_ip
}
