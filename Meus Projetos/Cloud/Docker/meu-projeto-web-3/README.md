# 🐳 Cluster Docker Swarm Local com Vagrant

Projeto desenvolvido como parte do bootcamp **Formação em Docker** da [DIO](https://www.dio.me/), com o objetivo de criar um Cluster Docker Swarm local utilizando máquinas virtuais provisionadas pelo Vagrant.

---

## 📋 Sobre o Projeto

Este projeto demonstra como criar e configurar um **Cluster Docker Swarm** de forma automatizada, utilizando o Vagrant para provisionar as máquinas virtuais e scripts shell para instalar e configurar o Docker e o Swarm em cada nó.

### O que é Docker Swarm?

Docker Swarm é a solução nativa de orquestração de containers do Docker. Ele permite transformar múltiplos hosts Docker em um único cluster, oferecendo:

- **Alta disponibilidade** dos serviços
- **Escalabilidade** horizontal de containers
- **Load balancing** automático entre os nós
- **Gerenciamento centralizado** via nó Manager

### O que é Vagrant?

Vagrant é uma ferramenta para criar e gerenciar ambientes de desenvolvimento virtualizados. Com um único arquivo (`Vagrantfile`), é possível definir e provisionar múltiplas máquinas virtuais de forma automatizada e reproduzível.

---

## 🏗️ Arquitetura do Cluster

```
+------------------------------------------+
|          CLUSTER DOCKER SWARM            |
|                                          |
|  +------------------------------------+  |
|  | master (192.168.56.100)            |  |
|  | Funcao: Manager / Leader           |  |
|  | RAM: 1024MB | CPU: 1               |  |
|  +------------------------------------+  |
|                                          |
|  +-----------------+-----------------+   |
|  | node01          | node02          |   |
|  | 192.168.56.101  | 192.168.56.102  |   |
|  | Funcao: Worker  | Funcao: Worker  |   |
|  | RAM: 512MB      | RAM: 512MB      |   |
|  +-----------------+-----------------+   |
|                                          |
+------------------------------------------+
```

---

## 🛠️ Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado:

- [VirtualBox](https://www.virtualbox.org/wiki/Downloads) — Hypervisor para rodar as VMs
- [Vagrant](https://www.vagrantup.com/downloads) — Gerenciador de VMs
- Git Bash ou terminal compatível com bash

---

## 📁 Estrutura do Projeto

```
meu-projeto-web-3/
├── Vagrantfile
├── docker.sh
├── master.sh
├── worker.sh
└── README.md
```

---

## 📄 Arquivos de Configuração

### `Vagrantfile`
```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

machines = {
  "master" => {"memory" => "1024", "cpu" => "1", "ip" => "100"},
  "node01" => {"memory" => "512",  "cpu" => "1", "ip" => "101"},
  "node02" => {"memory" => "512",  "cpu" => "1", "ip" => "102"}
}

Vagrant.configure("2") do |config|
  config.vm.boot_timeout = 600
  config.ssh.insert_key = false

  machines.each do |name, conf|
    config.vm.define "#{name}" do |machine|
      machine.vm.box = "ubuntu/focal64"
      machine.vm.hostname = "#{name}"
      machine.vm.network "private_network", ip: "192.168.56.#{conf["ip"]}"

      machine.vm.provider "virtualbox" do |vb|
        vb.name = "#{name}"
        vb.memory = conf["memory"]
        vb.cpus = conf["cpu"]
        vb.gui = false
        vb.customize ["modifyvm", :id, "--uart1", "0x3F8", "4"]
        vb.customize ["modifyvm", :id, "--uartmode1", "file", File::NULL]
      end

      machine.vm.provision "shell", path: "docker.sh"

      if "#{name}" == "master"
        machine.vm.provision "shell", path: "master.sh"
      else
        machine.vm.provision "shell", path: "worker.sh"
      end
    end
  end
end
```

### `docker.sh`
```bash
#!/bin/bash
echo "=== Instalando Docker ==="
export DEBIAN_FRONTEND=noninteractive
curl -fsSL https://get.docker.com | sudo DEBIAN_FRONTEND=noninteractive bash
sudo usermod -aG docker vagrant
sudo systemctl enable docker
sudo systemctl start docker
echo "=== Docker instalado com sucesso ==="
```

### `master.sh`
```bash
#!/bin/bash
echo "=== Iniciando Swarm Master ==="
sudo docker swarm init --advertise-addr enp0s8 --listen-addr enp0s8:2377
sudo docker swarm join-token worker | grep docker > /vagrant/worker.sh
echo "=== Token salvo em /vagrant/worker.sh ==="
```

### `worker.sh`
```bash
#!/bin/bash
echo "=== Worker aguardando token do master... ==="
# Este arquivo será sobrescrito pelo master.sh com o token real
```

---

## 🚀 Como Executar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Suba as máquinas virtuais
```bash
vagrant up
```
> ⏳ Aguarde — pode levar alguns minutos para baixar a box e provisionar as 3 VMs.

### 3. Verifique o status das VMs
```bash
vagrant status
```
Resultado esperado:

master    running (virtualbox)
node01    running (virtualbox)
node02    running (virtualbox)

### 4. Acesse o nó master
```bash
vagrant ssh master
```

### 5. Verifique o Cluster Swarm

```bash
sudo docker node ls
```
Resultado esperado:

```
ID                            HOSTNAME   STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
abc123 *                      master     Ready     Active         Leader           26.1.3
def456                        node01     Ready     Active                          26.1.3
ghi789                        node02     Ready     Active                          26.1.3
```

---

## ⚠️ Solução de Problemas Conhecidos

### Workers não entram no Swarm automaticamente

Caso o `worker.sh` não execute corretamente no provisionamento, faça manualmente:

**Na master:**
```bash
sudo docker swarm join-token worker | grep docker > /vagrant/worker.sh
```

**Em cada worker (node01, node02):**
```bash
sudo bash /vagrant/worker.sh
```

### Timeout de boot das VMs

```
Se aparecer o erro `Timed out while waiting for the machine to boot`, o `Vagrantfile` já está configurado com `config.vm.boot_timeout = 600` para 10 minutos. Aguarde ou verifique se o Hyper-V está desabilitado no Windows.
```

### Desabilitar Hyper-V no Windows (se necessário)

Abra o PowerShell como Administrador:
```powershell
bcdedit /set hypervisorlaunchtype off
```
Reinicie o computador.

---

## 🔧 Comandos Úteis

| Comando | Descrição |
|---|---|
| `vagrant up` | Sobe todas as VMs |
| `vagrant halt` | Desliga todas as VMs |
| `vagrant destroy -f` | Destrói todas as VMs |
| `vagrant ssh master` | Acessa a VM master |
| `vagrant ssh node01` | Acessa o node01 |
| `vagrant status` | Verifica status das VMs |
| `sudo docker node ls` | Lista nós do Swarm (na master) |
| `sudo docker service ls` | Lista serviços do Swarm |

---

## 📚 Tecnologias Utilizadas

- [Docker](https://www.docker.com/) — Plataforma de containers
- [Docker Swarm](https://docs.docker.com/engine/swarm/) — Orquestração de containers
- [Vagrant](https://www.vagrantup.com/) — Gerenciamento de VMs
- [VirtualBox](https://www.virtualbox.org/) — Hypervisor
- [Ubuntu 20.04 LTS](https://releases.ubuntu.com/20.04/) — Sistema operacional das VMs

---

## 👨‍💻 Autor

Desenvolvido por **Carlos Alexandre** como parte do bootcamp Formação em Docker.

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.



