# 🚀 FIWARE IoT Platform

**Trabalho Prático 2 - Sistemas de Comunicação Móvel**  
**Universidade Katyavala Bwila - Instituto Politécnico**  
**Mestrado em Engenharia Informática**

Plataforma completa de IoT baseada no FIWARE com persistência de dados, visualização e monitoramento.

## 📋 Informações do Trabalho Prático

### **I. Objectivos**
- ✅ Instalar e iniciar o ambiente FIWARE via Docker Compose
- ✅ Criar entidades e dispositivos IoT simulados (salas com sensores de temperatura e humidade)
- ✅ Registar dispositivos com o IoT Agent (IDAS)
- ✅ Enviar dados simulados para o Context Broker (Orion)
- ✅ Criar subscrições para aplicações externas
- ✅ Persistir dados históricos com o Cygnus em base de dados MySQL
- ✅ Visualizar dados no Grafana

### **II. Pré-Requisitos**
#### **Conhecimentos:**
- Conceitos básicos de redes e HTTP
- Lógica de programação e APIs REST
- Conceitos de sensores e IoT

#### **Ferramentas Necessárias:**
- Docker e Docker Compose
- Postman
- Editor de código (VSCode, preferencial)

### **III. Materiais Necessários**
- Computador
- Acesso à internet
- Repositório com o ambiente FIWARE (Docker Compose)
- Scripts JSON para testar com o Postman

### **V. Introdução**
O FIWARE é uma plataforma de código aberto que oferece módulos (Generic Enablers) para construção de aplicações inteligentes, incluindo suporte a IoT, big data e serviços contextuais. 

Neste projecto, é utilizado um cenário de IoT onde simulamos o envio de dados de sensores virtuais (por exemplo, temperatura e humidade numa sala) para o Context Broker (Orion), usando o protocolo UL2.0 via IoT Agent.

O ambiente é iniciado via docker-compose, onde todos os containers (MongoDB, Orion, IDAS, Cygnus, MySQL e Grafana) são levantados automaticamente.

## 📁 Estrutura do Projeto

```
fiware/
├── 📁 docs/                    # Documentação
│   ├── GUIA_CONSULTAS_MONGODB.md
│   ├── GUIA_GRAFANA_FIWARE.md
│   ├── GUIA_SUBSCRICOES_CYGNUS.md
│   ├── GUIA_VISUALIZACAO_DADOS.md
│   ├── INSTRUCOES_GRAFANA.md
│   ├── INSTRUCOES_SUBSCRICOES.md
│   └── README_STH_Comet_dashboard.md
├── 📁 scripts/                 # Scripts de automação
│   ├── fiware_manager.py       # 🎯 Script principal
│   ├── configurar_subscricoes.py
│   ├── testar_subscricoes.py
│   ├── configurar_grafana_dados.py
│   ├── consulta_mongodb.py
│   ├── api-sth.py
│   ├── setup_grafana.sh
│   └── configurar_grafana.sh
├── 📁 config/                  # Configurações
│   ├── environment.py          # 🔧 Configurações de ambiente
│   └── requirements.txt        # 📦 Dependências Python
├── 📁 examples/                # Exemplos e código
│   ├── fiware_ngsi_mqtt_esp32.ino
│   ├── esp32_ntp.ino
│   ├── arduino.txt
│   ├── esp32_ldr.png
│   └── mqtt_esp32.md
├── 📁 tools/                   # Ferramentas
│   └── FIWARE Descomplicado.postman_collection.json
├── 📁 grafana/                 # Configurações Grafana
│   ├── provisioning/
│   └── dashboards/
├── 📁 mysql/                   # Configurações MySQL
│   └── init/
├── 📁 mosquitto/               # Configurações MQTT
│   └── mosquitto.conf
├── 📄 docker-compose.yml       # 🐳 Configuração principal
├── 📄 README.md               # Este arquivo
├── 📄 PROJECT_STRUCTURE.md    # 📋 Estrutura do projeto
└── 📄 TRABALHO_PRATICO_2.md  # 🎓 Documentação do TP2
```

## 🚀 Início Rápido

### **1. Instalação**
```bash
# Clonar o projeto
git clone <repository-url>
cd fiware

# Instalar dependências
pip install -r config/requirements.txt

# Iniciar serviços
docker-compose up -d
```

### **2. Configuração Automática**
```bash
# Executar configuração completa
python3 scripts/fiware_manager.py setup

# Verificar status
python3 scripts/fiware_manager.py status
```

### **3. Acesso aos Serviços**
- **Grafana:** http://localhost:3000 (admin/admin123)
- **Orion:** http://localhost:1026
- **STH Comet:** http://localhost:8666
- **IoT Agent:** http://localhost:4041

## 🎯 Script Principal

O `fiware_manager.py` é o script principal que integra todas as funcionalidades:

```bash
# Ver comandos disponíveis
python3 scripts/fiware_manager.py help

# Comandos principais
python3 scripts/fiware_manager.py status      # Status do sistema
python3 scripts/fiware_manager.py setup       # Configuração completa
python3 scripts/fiware_manager.py check       # Verificar serviços
python3 scripts/fiware_manager.py test-data   # Gerar dados de teste
```

## 🏗️ Arquitetura

### **Componentes Principais:**
- **Orion Context Broker** - Gerenciamento de contexto
- **STH Comet** - Armazenamento histórico
- **Cygnus** - Persistência de dados
- **MySQL** - Banco de dados relacional
- **MongoDB** - Banco de dados NoSQL
- **Grafana** - Visualização e monitoramento
- **IoT Agent** - Conectividade IoT
- **Mosquitto** - Broker MQTT

### **Fluxo de Dados:**
```
ESP32 → MQTT → IoT Agent → Orion → [Subscrições] → Cygnus → MySQL/MongoDB
                                    ↓
                                 STH Comet → Grafana
```

## 📊 Funcionalidades

### **✅ Implementadas:**
- ✅ Persistência automática de dados
- ✅ Subscrições Orion configuráveis
- ✅ Visualização no Grafana
- ✅ Suporte a MySQL e MongoDB
- ✅ Scripts de automação
- ✅ Geração de dados de teste
- ✅ Monitoramento de serviços

### **🔧 Configurações:**
- 🔧 Dashboards personalizáveis
- 🔧 Alertas configuráveis
- 🔧 Integração com ESP32
- 🔧 APIs REST documentadas

## 📚 Documentação

### **🎓 Trabalho Prático 2:**
- `TRABALHO_PRATICO_2.md` - **Documentação completa do TP2**
- Informações sobre objectivos, pré-requisitos e avaliação
- Guia passo-a-passo para implementação
- Critérios de avaliação e entregáveis

### **Guias Técnicos:**
- `docs/GUIA_CONSULTAS_MONGODB.md` - Consultas de dados
- `docs/GUIA_GRAFANA_FIWARE.md` - Configuração Grafana
- `docs/GUIA_SUBSCRICOES_CYGNUS.md` - Subscrições e persistência
- `docs/GUIA_VISUALIZACAO_DADOS.md` - Visualização de dados

### **Exemplos:**
- `examples/fiware_ngsi_mqtt_esp32.ino` - Código ESP32
- `tools/FIWARE Descomplicado.postman_collection.json` - Collection Postman

## 🔧 Configuração

### **Portas Utilizadas:**
- **1026:** Orion Context Broker
- **8666:** STH Comet
- **3000:** Grafana
- **4041:** IoT Agent
- **1883:** MQTT Broker
- **3306:** MySQL
- **27017:** MongoDB
- **5080:** Cygnus

### **Credenciais:**
- **Grafana:** admin/admin123
- **MySQL:** fiware/fiware123
- **MongoDB:** admin/admin123

## 🚀 Comandos Úteis

### **Gerenciamento de Serviços:**
```bash
# Iniciar todos os serviços
docker-compose up -d

# Parar serviços
docker-compose down

# Ver logs
docker-compose logs -f

# Verificar containers
docker ps
```

### **Scripts de Automação:**
```bash
# Configuração completa
python3 scripts/fiware_manager.py setup

# Verificar status
python3 scripts/fiware_manager.py status

# Gerar dados de teste
python3 scripts/fiware_manager.py test-data

# Configurar Grafana
python3 scripts/fiware_manager.py grafana
```

### **Consultas de Dados:**
```bash
# Consultar entidades
curl -X GET "http://localhost:1026/v2/entities" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"

# Consultar dados históricos
curl -X GET "http://localhost:8666/STH/v1/contextEntities" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"
```

## 🐛 Troubleshooting

### **Problemas Comuns:**

#### **Serviços não iniciam:**
```bash
# Verificar se Docker está rodando
docker --version

# Verificar logs
docker-compose logs

# Reiniciar serviços
docker-compose restart
```

#### **Grafana não acessível:**
```bash
# Verificar container
docker ps | grep grafana

# Verificar logs
docker logs fiware-grafana

# Reiniciar Grafana
docker restart fiware-grafana
```

#### **Dados não aparecem:**
```bash
# Verificar subscrições
python3 scripts/fiware_manager.py check

# Gerar dados de teste
python3 scripts/fiware_manager.py test-data

# Verificar persistência
python3 scripts/fiware_manager.py persistence
```

## 🎓 Trabalho Prático 2 - Sistemas de Comunicação Móvel

### **📚 Contexto Académico**
Este projeto foi desenvolvido no âmbito do **Trabalho Prático 2** da disciplina de **Sistemas de Comunicação Móvel** do **Mestrado em Engenharia Informática** da **Universidade Katyavala Bwila - Instituto Politécnico**.

### **🎯 Objectivos Alcançados**
- ✅ **Ambiente FIWARE** instalado e configurado via Docker Compose
- ✅ **Entidades IoT** criadas (salas com sensores de temperatura e humidade)
- ✅ **Dispositivos registados** com IoT Agent (IDAS)
- ✅ **Dados simulados** enviados para Context Broker (Orion)
- ✅ **Subscrições criadas** para aplicações externas
- ✅ **Persistência de dados** implementada com Cygnus e MySQL
- ✅ **Visualização** configurada no Grafana

### **🔬 Cenário de Teste**
O projeto simula um ambiente IoT onde:
- **Sensores virtuais** enviam dados de temperatura e humidade
- **Salas** são representadas como entidades no sistema
- **Dados históricos** são persistidos automaticamente
- **Visualização em tempo real** é disponibilizada via Grafana

### **📊 Tecnologias Utilizadas**
- **FIWARE Orion** - Context Broker
- **IoT Agent UL** - Conectividade IoT
- **Cygnus** - Persistência de dados
- **MySQL** - Base de dados relacional
- **MongoDB** - Base de dados NoSQL
- **Grafana** - Visualização de dados
- **Docker Compose** - Orquestração de containers

### **🎓 Aprendizagens**
Este trabalho prático permitiu:
- Compreender arquiteturas IoT baseadas em FIWARE
- Trabalhar com APIs REST e protocolos IoT
- Implementar persistência de dados em tempo real
- Configurar visualização e monitoramento
- Utilizar containers Docker para desenvolvimento

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [FIWARE Foundation](https://www.fiware.org/)
- [FIWARE Tutorials](https://fiware-tutorials.readthedocs.io/)
- [Telefónica IoT](https://iot.telefonica.com/)
- **Universidade Katyavala Bwila** - Instituto Politécnico
- **Professores** da disciplina de Sistemas de Comunicação Móvel

---

**🎯 Projeto organizado e pronto para uso!**  
**🎓 Trabalho Prático 2 - Sistemas de Comunicação Móvel**
