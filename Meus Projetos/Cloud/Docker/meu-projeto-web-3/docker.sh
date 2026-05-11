#!/bin/bash
echo "=== Instalando Docker ==="
export DEBIAN_FRONTEND=noninteractive
curl -fsSL https://get.docker.com | sudo DEBIAN_FRONTEND=noninteractive bash
sudo usermod -aG docker vagrant
sudo systemctl enable docker
sudo systemctl start docker
echo "=== Docker instalado com sucesso ==="