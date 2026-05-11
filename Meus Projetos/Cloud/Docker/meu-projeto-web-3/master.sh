#!/bin/bash
echo "=== Iniciando Swarm Master ==="
sudo docker swarm init --advertise-addr=192.168.56.100

# Salva o comando de join para os workers usarem
sudo docker swarm join-token worker | grep "docker swarm join" > /vagrant/worker.sh
echo "=== Token salvo em /vagrant/worker.sh ==="