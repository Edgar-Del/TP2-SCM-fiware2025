# Guia de Consultas - MongoDB FIWARE

## **1. Consulta via STH Comet (Recomendado)**

### **Instalação das Dependências:**
```bash
pip install -r requirements_consulta.txt
```

### **Executar Script de Consulta:**
```bash
python consulta_mongodb.py
```

### **Consultas Manuais via cURL:**

#### **Listar Entidades Disponíveis:**
```bash
curl -X GET "http://localhost:8666/STH/v1/contextEntities" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"
```

#### **Consultar Dados de Luminosidade (últimos 10):**
```bash
curl -X GET "http://localhost:8666/STH/v1/contextEntities/type/Lamp/id/urn:ngsi-ld:Lamp:001/attributes/luminosity?lastN=10" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"
```

#### **Consultar Dados por Período:**
```bash
curl -X GET "http://localhost:8666/STH/v1/contextEntities/type/Lamp/id/urn:ngsi-ld:Lamp:001/attributes/luminosity?hLimit=100&hOffset=0" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"
```

## **2. Acesso Direto ao MongoDB**

### **Conectar ao Container MongoDB:**
```bash
# MongoDB Histórico (com autenticação)
docker exec -it fiware-mongo-historical mongo -u admin -p admin123 --authenticationDatabase admin

# MongoDB Interno (sem autenticação)
docker exec -it fiware-mongo-internal mongo
```

### **Comandos MongoDB Úteis:**

#### **Listar Bancos de Dados:**
```javascript
show dbs
```

#### **Usar Banco do STH Comet:**
```javascript
use sth_
```

#### **Listar Coleções:**
```javascript
show collections
```

#### **Consultar Dados de uma Coleção:**
```javascript
// Primeiros 5 documentos
db.nome_da_colecao.find().limit(5)

// Todos os documentos
db.nome_da_colecao.find()

// Contar documentos
db.nome_da_colecao.countDocuments()

// Consulta com filtro
db.nome_da_colecao.find({"attrName": "luminosity"})

// Ordenar por timestamp
db.nome_da_colecao.find().sort({"recvTime": -1})
```

#### **Consultas Avançadas:**
```javascript
// Dados dos últimos 7 dias
db.nome_da_colecao.find({
  "recvTime": {
    $gte: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
  }
})

// Média de luminosidade
db.nome_da_colecao.aggregate([
  { $match: { "attrName": "luminosity" } },
  { $group: { _id: null, avgValue: { $avg: "$attrValue" } } }
])

// Valores máximos e mínimos
db.nome_da_colecao.aggregate([
  { $match: { "attrName": "luminosity" } },
  { $group: { 
    _id: null, 
    maxValue: { $max: "$attrValue" },
    minValue: { $min: "$attrValue" }
  } }
])
```

## **3. Consulta via Orion Context Broker**

### **Listar Entidades:**
```bash
curl -X GET "http://localhost:1026/v2/entities" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"
```

### **Consultar Entidade Específica:**
```bash
curl -X GET "http://localhost:1026/v2/entities/urn:ngsi-ld:Lamp:001" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"
```

### **Consultar Atributo Específico:**
```bash
curl -X GET "http://localhost:1026/v2/entities/urn:ngsi-ld:Lamp:001/attrs/luminosity" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"
```

## **4. Estrutura dos Dados**

### **Dados no STH Comet:**
```json
{
  "contextResponses": [
    {
      "contextElement": {
        "attributes": [
          {
            "values": [
              {
                "recvTime": "2024-01-01T10:00:00.000Z",
                "attrValue": 123.45
              }
            ]
          }
        ]
      }
    }
  ]
}
```

### **Dados no MongoDB Direto:**
```json
{
  "_id": ObjectId("..."),
  "attrName": "luminosity",
  "attrType": "Number",
  "attrValue": 123.45,
  "recvTime": "2024-01-01T10:00:00.000Z",
  "entityId": "urn:ngsi-ld:Lamp:001",
  "entityType": "Lamp"
}
```

## **5. Ferramentas de Visualização**

### **MongoDB Compass:**
- Interface gráfica para MongoDB
- Conectar em: `mongodb://admin:admin123@localhost:27017/admin`

### **Postman:**
- Use a collection fornecida: `FIWARE Descomplicado.postman_collection.json`

### **Dashboard Python:**
- Execute: `python api-sth.py`
- Acesse: `http://localhost:8050`

## **6. Troubleshooting**

### **Problemas Comuns:**

#### **Erro de Conexão:**
```bash
# Verificar se containers estão rodando
docker ps

# Verificar logs
docker logs fiware-mongo-historical
docker logs fiware-sth-comet
```

#### **Erro de Autenticação:**
```bash
# Verificar credenciais no docker-compose.yml
# Usar headers corretos: fiware-service e fiware-servicepath
```

#### **Dados Não Aparecem:**
```bash
# Verificar se IoT Agent está funcionando
docker logs fiware-iot-agent

# Verificar se ESP32 está enviando dados
# Verificar tópicos MQTT
```

## **7. Exemplos Práticos**

### **Script Python para Exportar Dados:**
```python
import requests
import json
import csv
from datetime import datetime

def export_data_to_csv():
    url = "http://localhost:8666/STH/v1/contextEntities/type/Lamp/id/urn:ngsi-ld:Lamp:001/attributes/luminosity?hLimit=1000"
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    with open('luminosity_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Luminosity'])
        
        for value in data['contextResponses'][0]['contextElement']['attributes'][0]['values']:
            writer.writerow([value['recvTime'], value['attrValue']])

export_data_to_csv()
```

### **Script para Backup:**
```bash
# Backup do MongoDB
docker exec fiware-mongo-historical mongodump --out /backup --username admin --password admin123 --authenticationDatabase admin

# Copiar backup para host
docker cp fiware-mongo-historical:/backup ./backup_mongodb
```

Este guia fornece todas as formas de consultar os dados persistidos no MongoDB do seu projeto FIWARE! 