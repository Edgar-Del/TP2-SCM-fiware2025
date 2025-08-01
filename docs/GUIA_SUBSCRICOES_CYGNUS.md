# Guia Subscrições Orion + Cygnus

## **1. O que são Subscrições?**

### **Definição:**
Subscrições no Orion Context Broker permitem que você seja **notificado automaticamente** quando entidades ou atributos específicos são modificados. O Cygnus atua como um **sink** que recebe essas notificações e as **persiste** em bancos de dados.

### **Fluxo de Dados:**
```
ESP32 → MQTT → IoT Agent → Orion → [Subscrição] → Cygnus → MySQL/MongoDB
```

## **2. Componentes Adicionados**

### **MySQL:**
- **Porta:** 3306
- **Usuário:** fiware
- **Senha:** fiware123
- **Database:** fiware

### **Cygnus:**
- **Porta:** 5080 (serviço), 5050 (admin)
- **Função:** Recebe notificações do Orion e persiste dados
- **Suporte:** MySQL, MongoDB, PostgreSQL, etc.

## **3. Instalação e Configuração**

### **Iniciar Serviços:**
```bash
# Parar serviços existentes
docker-compose down

# Iniciar com Cygnus e MySQL
docker-compose up -d

# Verificar se todos estão rodando
docker ps
```

### **Verificar Logs:**
```bash
# Logs do Cygnus
docker logs fiware-cygnus

# Logs do MySQL
docker logs fiware-mysql

# Logs do Orion
docker logs fiware-orion
```

## **4. Configuração de Subscrições**

### **Executar Script Automático:**
```bash
# Instalar dependências
pip install requests

# Executar configuração
python configurar_subscricoes.py
```

### **Subscrição Manual via cURL:**

#### **Subscrição para MySQL:**
```bash
curl -X POST "http://localhost:1026/v2/subscriptions" \
  -H "Content-Type: application/json" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /" \
  -d '{
    "description": "Subscrição para MySQL",
    "subject": {
      "entities": [
        {
          "idPattern": ".*",
          "type": "Lamp"
        }
      ],
      "condition": {
        "attrs": ["luminosity", "status"]
      }
    },
    "notification": {
      "http": {
        "url": "http://cygnus:5080/notify"
      },
      "attrs": ["luminosity", "status"],
      "metadata": ["dateCreated", "dateModified"]
    },
    "expires": "2030-12-31T23:59:59.000Z",
    "throttling": 5
  }'
```

#### **Subscrição para MongoDB:**
```bash
curl -X POST "http://localhost:1026/v2/subscriptions" \
  -H "Content-Type: application/json" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /" \
  -d '{
    "description": "Subscrição para MongoDB",
    "subject": {
      "entities": [
        {
          "idPattern": ".*",
          "type": "Lamp"
        }
      ],
      "condition": {
        "attrs": ["luminosity", "status"]
      }
    },
    "notification": {
      "http": {
        "url": "http://cygnus:5080/notify"
      },
      "attrs": ["luminosity", "status"],
      "metadata": ["dateCreated", "dateModified"]
    },
    "expires": "2030-12-31T23:59:59.000Z",
    "throttling": 5
  }'
```

## **5. Gerenciamento de Subscrições**

### **Listar Subscrições:**
```bash
curl -X GET "http://localhost:1026/v2/subscriptions" \
  -H "Accept: application/json" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"
```

### **Deletar Subscrição:**
```bash
curl -X DELETE "http://localhost:1026/v2/subscriptions/{subscription_id}" \
  -H "Accept: application/json" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"
```

### **Atualizar Subscrição:**
```bash
curl -X PATCH "http://localhost:1026/v2/subscriptions/{subscription_id}" \
  -H "Content-Type: application/json" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /" \
  -d '{
    "expires": "2030-12-31T23:59:59.000Z"
  }'
```

## **6. Verificação de Dados**

### **Verificar Dados no MySQL:**
```bash
# Conectar ao MySQL
docker exec -it fiware-mysql mysql -u fiware -pfiware123 fiware

# Listar tabelas
SHOW TABLES;

# Consultar dados
SELECT * FROM smart_default_lamp;

# Consultar dados de luminosidade
SELECT * FROM smart_default_lamp_luminosity;
```

### **Verificar Dados no MongoDB:**
```bash
# Conectar ao MongoDB
docker exec -it fiware-mongo-historical mongo -u admin -p admin123 --authenticationDatabase admin

# Usar banco do Cygnus
use cygnus

# Listar coleções
show collections

# Consultar dados
db.smart_default_lamp.find()
```

## **7. Configurações Avançadas**

### **Subscrição com Condições:**
```json
{
  "subject": {
    "entities": [
      {
        "idPattern": ".*",
        "type": "Lamp"
      }
    ],
    "condition": {
      "attrs": ["luminosity", "status"],
      "expression": {
        "q": "luminosity>100"
      }
    }
  }
}
```

### **Subscrição com Filtros Geográficos:**
```json
{
  "subject": {
    "entities": [
      {
        "idPattern": ".*",
        "type": "Lamp"
      }
    ],
    "condition": {
      "attrs": ["luminosity"],
      "expression": {
        "georel": "near;maxDistance:1000",
        "geometry": "point",
        "coords": "[-3.7037902,40.4167754]"
      }
    }
  }
}
```

### **Subscrição com Throttling:**
```json
{
  "throttling": 10,
  "notification": {
    "http": {
      "url": "http://cygnus:5080/notify"
    },
    "attrsFormat": "legacy"
  }
}
```

## **8. Configuração do Cygnus**

### **Variáveis de Ambiente Importantes:**

#### **Para MySQL:**
```yaml
environment:
  - CYGNUS_MYSQL_HOST=mysql
  - CYGNUS_MYSQL_PORT=3306
  - CYGNUS_MYSQL_USER=fiware
  - CYGNUS_MYSQL_PASS=fiware123
  - CYGNUS_MYSQL_DATABASE=fiware
```

#### **Para MongoDB:**
```yaml
environment:
  - CYGNUS_MONGO_HOSTS=mongo-db-historical:27017
  - CYGNUS_MONGO_USER=admin
  - CYGNUS_MONGO_PASS=admin123
  - CYGNUS_MONGO_AUTH_SOURCE=admin
```

### **Configuração de Logs:**
```yaml
environment:
  - CYGNUS_LOG_LEVEL=DEBUG
  - CYGNUS_SERVICE_PORT=5080
  - CYGNUS_ADMIN_PORT=5050
```

## **9. Troubleshooting**

### **Problemas Comuns:**

#### **Subscrição não funciona:**
```bash
# Verificar se Orion está funcionando
curl -X GET "http://localhost:1026/v2/version"

# Verificar se Cygnus está funcionando
curl -X GET "http://localhost:5080/v1/version"

# Verificar logs do Cygnus
docker logs fiware-cygnus
```

#### **Dados não aparecem no banco:**
```bash
# Verificar se subscrição foi criada
curl -X GET "http://localhost:1026/v2/subscriptions" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"

# Verificar logs do Cygnus
docker logs fiware-cygnus

# Testar notificação manual
curl -X POST "http://localhost:5080/notify" \
  -H "Content-Type: application/json" \
  -d '{"data": [{"id": "test", "type": "Lamp"}]}'
```

#### **Erro de conexão com banco:**
```bash
# Verificar se MySQL está rodando
docker logs fiware-mysql

# Testar conexão MySQL
docker exec -it fiware-mysql mysql -u fiware -pfiware123 -e "SHOW DATABASES;"

# Verificar se MongoDB está rodando
docker logs fiware-mongo-historical
```

## **10. Exemplos Práticos**

### **Subscrição para Dados de Sensor:**
```json
{
  "description": "Subscrição para dados de sensor",
  "subject": {
    "entities": [
      {
        "idPattern": ".*",
        "type": "Sensor"
      }
    ],
    "condition": {
      "attrs": ["temperature", "humidity", "pressure"]
    }
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5080/notify"
    },
    "attrs": ["temperature", "humidity", "pressure"]
  }
}
```

### **Subscrição com Agregação:**
```json
{
  "description": "Subscrição com agregação",
  "subject": {
    "entities": [
      {
        "idPattern": ".*",
        "type": "Lamp"
      }
    ],
    "condition": {
      "attrs": ["luminosity"],
      "expression": {
        "q": "luminosity>50"
      }
    }
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5080/notify"
    },
    "attrs": ["luminosity"],
    "metadata": ["dateCreated", "dateModified"]
  }
}
```

## **11. Integração com Grafana**

### **Configurar Datasource MySQL no Grafana:**
1. Acesse http://localhost:3000
2. Vá em **Configuration** > **Data Sources**
3. Adicione **MySQL**
4. Configure:
   - **Host:** mysql:3306
   - **Database:** fiware
   - **User:** fiware
   - **Password:** fiware123

### **Query MySQL para Grafana:**
```sql
SELECT 
  recvTime as time,
  attrValue as value
FROM smart_default_lamp_luminosity 
WHERE attrName = 'luminosity'
ORDER BY recvTime DESC
LIMIT 100
```

Este guia fornece tudo que você precisa para configurar subscrições Orion e persistir dados com Cygnus! 