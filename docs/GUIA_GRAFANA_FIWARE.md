# Guia Grafana + FIWARE

## **1. Instalação e Configuração**

### **Opção A: Usar docker-compose com Grafana**

```bash
# Usar o arquivo com Grafana incluído
docker-compose -f docker-compose-grafana.yml up -d

# Aguardar todos os serviços iniciarem
docker-compose -f docker-compose-grafana.yml logs -f
```

### **Opção B: Adicionar Grafana ao projeto existente**

```bash
# Parar serviços atuais
docker-compose down

# Adicionar Grafana ao docker-compose.yml existente
# (Copiar configuração do docker-compose-grafana.yml)

# Reiniciar com Grafana
docker-compose up -d
```

## **2. Acesso ao Grafana**

### **URL e Credenciais:**
- **URL:** `http://localhost:3000`
- **Usuário:** `admin`
- **Senha:** `admin123`

### **Verificar se está funcionando:**
```bash
# Verificar se o container está rodando
docker ps | grep grafana

# Verificar logs
docker logs fiware-grafana
```

## **3. Configuração Manual do Datasource**

### **Passo 1: Acessar Grafana**
1. Abra `http://localhost:3000`
2. Faça login com `admin/admin123`

### **Passo 2: Criar Datasource**
1. Vá em **Configuration** > **Data Sources**
2. Clique em **Add data source**
3. Selecione **SimpleJSON**
4. Configure:
   - **Name:** `STH-Comet`
   - **URL:** `http://sth-comet:8666`
   - **Access:** `proxy`

### **Passo 3: Testar Conexão**
1. Clique em **Save & Test**
2. Verifique se aparece "Data source is working"

## **4. Configuração Automática**

### **Executar Script de Configuração:**
```bash
# Instalar dependências
pip install requests

# Executar script de configuração
python grafana_setup.py
```

## **5. Criando Dashboards**

### **Opção A: Importar Dashboard JSON**

1. Vá em **+** > **Import**
2. Cole o conteúdo do arquivo `grafana/dashboards/fiware-dashboard.json`
3. Clique em **Load**
4. Configure o datasource
5. Clique em **Import**

### **Opção B: Criar Dashboard Manualmente**

#### **Painel 1: Gráfico de Luminosidade**
1. Clique em **+** > **Dashboard**
2. Clique em **Add new panel**
3. Configure:
   - **Data source:** `STH-Comet`
   - **Query:** `luminosity`
   - **Visualization:** `Time series`

#### **Painel 2: Status do LED**
1. Adicione novo painel
2. Configure:
   - **Data source:** `STH-Comet`
   - **Query:** `status`
   - **Visualization:** `Stat`

## **6. Queries para STH Comet**

### **Query Básica para Luminosidade:**
```json
{
  "targets": [
    {
      "target": "luminosity",
      "refId": "A",
      "type": "timeserie"
    }
  ],
  "range": {
    "from": "2024-01-01T00:00:00Z",
    "to": "2024-01-02T00:00:00Z"
  }
}
```

### **Query com Filtros:**
```json
{
  "targets": [
    {
      "target": "luminosity",
      "refId": "A",
      "type": "timeserie",
      "entityId": "urn:ngsi-ld:Lamp:001",
      "entityType": "Lamp"
    }
  ]
}
```

## **7. Configuração de Alertas**

### **Criar Alerta de Luminosidade Baixa:**
1. Vá no painel de luminosidade
2. Clique em **Alert**
3. Configure:
   - **Condition:** `WHEN avg() OF query(A, 5m, now) IS BELOW 50`
   - **For:** `5m`
   - **Notifications:** Configure canal desejado

### **Criar Alerta de LED Desligado:**
1. Vá no painel de status
2. Clique em **Alert**
3. Configure:
   - **Condition:** `WHEN last() OF query(A, 1m, now) IS BELOW 1`
   - **For:** `2m`

## **8. Dashboards Avançados**

### **Dashboard com Múltiplos Dispositivos:**
```json
{
  "panels": [
    {
      "title": "Luminosidade - Lamp 001",
      "targets": [
        {
          "target": "luminosity",
          "entityId": "urn:ngsi-ld:Lamp:001"
        }
      ]
    },
    {
      "title": "Luminosidade - Lamp 002",
      "targets": [
        {
          "target": "luminosity",
          "entityId": "urn:ngsi-ld:Lamp:002"
        }
      ]
    }
  ]
}
```

### **Dashboard com Métricas Agregadas:**
```json
{
  "panels": [
    {
      "title": "Média de Luminosidade (1h)",
      "targets": [
        {
          "target": "avg(luminosity)",
          "timeRange": "1h"
        }
      ]
    },
    {
      "title": "Máxima Luminosidade (24h)",
      "targets": [
        {
          "target": "max(luminosity)",
          "timeRange": "24h"
        }
      ]
    }
  ]
}
```

## **9. Troubleshooting**

### **Problemas Comuns:**

#### **Grafana não acessível:**
```bash
# Verificar se container está rodando
docker ps | grep grafana

# Verificar logs
docker logs fiware-grafana

# Reiniciar container
docker restart fiware-grafana
```

#### **Datasource não funciona:**
```bash
# Verificar se STH Comet está funcionando
curl -X GET "http://localhost:8666/STH/v1/contextEntities" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"

# Verificar logs do STH Comet
docker logs fiware-sth-comet
```

#### **Dados não aparecem:**
```bash
# Verificar se há dados no MongoDB
docker exec -it fiware-mongo-historical mongo -u admin -p admin123 --authenticationDatabase admin
use sth_
db.getCollectionNames()
```

### **Logs Úteis:**
```bash
# Logs do Grafana
docker logs fiware-grafana

# Logs do STH Comet
docker logs fiware-sth-comet

# Logs do MongoDB
docker logs fiware-mongo-historical
```

## **10. Exemplos de Dashboards**

### **Dashboard Básico:**
- Gráfico de linha para luminosidade
- Indicador de status do LED
- Tabela com últimos valores

### **Dashboard Avançado:**
- Múltiplos gráficos por dispositivo
- Métricas agregadas (média, máximo, mínimo)
- Alertas configurados
- Filtros por período

### **Dashboard em Tempo Real:**
- Atualização automática a cada 5s
- Gráficos em tempo real
- Indicadores de status
- Histórico das últimas 24h

## **11. Integração com APIs**

### **Script Python para Enviar Dados:**
```python
import requests
import json
from datetime import datetime

def send_data_to_grafana():
    url = "http://localhost:3000/api/datasources/proxy/1/query"
    
    data = {
        "targets": [
            {
                "target": "luminosity",
                "refId": "A"
            }
        ],
        "range": {
            "from": "now-1h",
            "to": "now"
        }
    }
    
    response = requests.post(url, json=data)
    return response.json()

# Usar dados
data = send_data_to_grafana()
print(data)
```

Este guia fornece tudo que você precisa para visualizar dados do FIWARE no Grafana! 