# Trabalho Prático 2 - Sistemas de Comunicação Móvel

**Universidade Katyavala Bwila - Instituto Politécnico**  
**Mestrado em Engenharia Informática**

## 📋 Informações Gerais

### **Disciplina:** Sistemas de Comunicação Móvel
### **Trabalho:** TP2 – FiWARE IoT Middleware

##Objectivos

### **I. Objectivos Principais**
- ✅ Instalar e iniciar o ambiente FIWARE via Docker Compose
- ✅ Criar entidades e dispositivos IoT simulados (salas com sensores de temperatura e humidade)
- ✅ Registar dispositivos com o IoT Agent (IDAS)
- ✅ Enviar dados simulados para o Context Broker (Orion)
- ✅ Criar subscrições para aplicações externas
- ✅ Persistir dados históricos com o Cygnus em base de dados MySQL
- ✅ Visualizar dados no Grafana

### **II. Objectivos de Aprendizagem**
- Compreender arquiteturas IoT baseadas em FIWARE
- Trabalhar com APIs REST e protocolos IoT
- Implementar persistência de dados em tempo real
- Configurar visualização e monitoramento
- Utilizar containers Docker para desenvolvimento

##Pré-Requisitos

### **Conhecimentos Teóricos**
- Conceitos básicos de redes e HTTP
- Lógica de programação e APIs REST
- Conceitos de sensores e IoT
- Arquiteturas de sistemas distribuídos

### **Ferramentas Necessárias**
- Docker e Docker Compose
- Postman (para testes de API)
- Cliente SSH (PuTTY ou terminal nativo)
- Editor de código (VSCode, Sublime, etc.)
- Putty (para conexões SSH)

## Materiais Necessários

### **Ambiente de Desenvolvimento**
- Computador com VM Ubuntu/Linux do Fiware Pré-configurado (neste caso não utilizamos)
- Acesso à internet
- Ambiente virtual em VMware ou VirtualBox

### **Recursos do Projeto**
- Repositório com o ambiente FIWARE (Docker Compose)
- Scripts JSON para testar com o Postman
- Documentação e guias de configuração

## Introdução

### **O que é o FIWARE?**
O FIWARE é uma plataforma de código aberto que oferece módulos (Generic Enablers) para construção de aplicações inteligentes, incluindo suporte a IoT, big data e serviços contextuais.

### **Cenário de Trabalho**
Neste laboratório, é utilizado um cenário de IoT onde simulamos o envio de dados de sensores virtuais (por exemplo, temperatura e humidade numa sala) para o Context Broker (Orion), usando o protocolo UL2.0 via IoT Agent.

### **Arquitetura do Sistema**
O ambiente é iniciado via docker-compose, onde todos os containers são levantados automaticamente:
- **MongoDB** - Base de dados NoSQL
- **Orion** - Context Broker
- **IoT Agent** - Conectividade IoT
- **Cygnus** - Persistência de dados
- **MySQL** - Base de dados relacional
- **Grafana** - Visualização de dados

## 📋 Tarefas do Trabalho Prático

### **1. Configuração do Ambiente**
```bash
# Instalação automática
./scripts/install.sh

# Ou configuração manual
docker-compose up -d
python3 scripts/fiware_manager.py setup
```

### **2. Criação de Entidades**
- Criar entidades como "Room1" com atributos temperature e humidity
- Configurar dispositivos IoT simulados
- Estabelecer comunicação com o Context Broker

### **3. Registro de Dispositivos**
- Registar dispositivos como sensor-a87020747f via IoT Agent
- Configurar protocolos de comunicação
- Testar conectividade

### **4. Simulação de Dados**
- Simular envio de dados com o Postman (em vez de curl)
- Gerar dados de temperatura e humidade
- Verificar recepção no Context Broker

### **5. Subscrições e Persistência**
- Criar subscrições para aplicações externas
- Configurar persistência de dados com Cygnus
- Verificar armazenamento em MySQL

### **6. Visualização**
- Aceder ao Grafana
- Configurar um painel de visualização
- Monitorar as medições recebidas

## 🔗 Recursos Adicionais

### **Documentação FIWARE**
- [FIWARE Foundation](https://www.fiware.org/)
- [FIWARE Tutorials](https://fiware-tutorials.readthedocs.io/)
- [FIWARE Documentation](https://fiware-documentation.readthedocs.io/)

### **Ferramentas Utilizadas**
- [Docker](https://www.docker.com/)
- [Postman](https://www.postman.com/)
- [Grafana](https://grafana.com/)
- [MySQL](https://www.mysql.com/)


### **Problemas Comuns**
- Containers não iniciam: Verificar Docker e recursos do sistema
- APIs não respondem: Verificar portas e configurações
- Dados não aparecem: Verificar subscrições e persistência
- Grafana não acessível: Verificar credenciais e configuração

---

**Trabalho Prático 2 - Sistemas de Comunicação Móvel**  
**Universidade Katyavala Bwila - Instituto Politécnico** 