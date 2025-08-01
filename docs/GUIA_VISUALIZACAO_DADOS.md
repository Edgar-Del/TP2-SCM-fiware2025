# 📊 Guia de Visualização de Dados - Grafana + FIWARE

## **Status Atual**

✅ **Serviços Funcionando:**
- Orion Context Broker (porta 1026)
- STH Comet (porta 8666)
- Grafana (porta 3000)
- MySQL (porta 3306)
- MongoDB (porta 27017)

✅ **Configurações Realizadas:**
- Datasource MySQL configurado
- Dashboard básico criado
- Subscrições Orion ativas

## **Acesso ao Grafana**

- **URL:** http://localhost:3000
- **Usuário:** admin
- **Senha:** admin123

## **Configuração Manual dos Datasources**

### **1. Datasource STH Comet**

1. Acesse http://localhost:3000
2. Faça login com admin/admin123
3. Vá em **Configuration** > **Data Sources**
4. Clique em **Add data source**
5. Selecione **SimpleJSON**
6. Configure:
   - **Name:** `STH-Comet`
   - **URL:** `http://sth-comet:8666`
   - **Access:** `proxy`
7. Clique em **Save & Test**

### **2. Datasource MySQL**

1. Vá em **Configuration** > **Data Sources**
2. Clique em **Add data source**
3. Selecione **MySQL**
4. Configure:
   - **Name:** `MySQL`
   - **Host:** `mysql:3306`
   - **Database:** `fiware`
   - **User:** `fiware`
   - **Password:** `fiware123`
5. Clique em **Save & Test**

## **Criando Dashboards**

### **Dashboard 1: Dados de Luminosidade**

1. Vá em **+** > **Dashboard**
2. Clique em **Add new panel**
3. Configure:
   - **Data source:** `STH-Comet`
   - **Query:** `luminosity`
   - **Visualization:** `Time series`

### **Dashboard 2: Status do LED**

1. Adicione novo painel
2. Configure:
   - **Data source:** `STH-Comet`
   - **Query:** `status`
   - **Visualization:** `Stat`

### **Dashboard 3: Dados MySQL**

1. Adicione novo painel
2. Configure:
   - **Data source:** `MySQL`
   - **Query SQL:**
   ```sql
   SELECT 
     recvTime as time,
     attrValue as value
   FROM smart_default_lamp_luminosity 
   WHERE attrName = 'luminosity'
   ORDER BY recvTime DESC
   LIMIT 100
   ```

## **Geração de Dados de Teste**

### **Script Automático:**
```bash
python3 configurar_grafana_dados.py
```

### **Manual via cURL:**
```bash
# Criar entidade
curl -X POST "http://localhost:1026/v2/entities" \
  -H "Content-Type: application/json" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /" \
  -d '{
    "id": "urn:ngsi-ld:Lamp:001",
    "type": "Lamp",
    "luminosity": {"type": "Number", "value": 150},
    "status": {"type": "Text", "value": "ON"}
  }'

# Atualizar entidade
curl -X PATCH "http://localhost:1026/v2/entities/urn:ngsi-ld:Lamp:001/attrs" \
  -H "Content-Type: application/json" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /" \
  -d '{
    "luminosity": {"type": "Number", "value": 200},
    "status": {"type": "Text", "value": "OFF"}
  }'
```

## **Consultas de Dados**

### **STH Comet:**
```bash
# Consultar dados de luminosidade
curl -X GET "http://localhost:8666/STH/v1/contextEntities/type/Lamp/id/urn:ngsi-ld:Lamp:001/attributes/luminosity?lastN=10" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"
```

### **MySQL:**
```bash
# Conectar ao MySQL
docker exec -it fiware-mysql mysql -u fiware -pfiware123 fiware

# Consultar dados
SELECT * FROM smart_default_lamp_luminosity;
```

### **MongoDB:**
```bash
# Conectar ao MongoDB
docker exec -it fiware-mongo-historical mongo -u admin -p admin123 --authenticationDatabase admin

# Consultar dados
use sth_
db.getCollectionNames()
db.smart_default_lamp.find()
```

## **Configurações Avançadas**

### **Alertas no Grafana:**

1. Vá no painel de luminosidade
2. Clique em **Alert**
3. Configure:
   - **Condition:** `WHEN avg() OF query(A, 5m, now) IS BELOW 50`
   - **For:** `5m`
   - **Notifications:** Configure canal desejado

### **Queries Avançadas:**

#### **STH Comet Query:**
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

#### **MySQL Query:**
```sql
SELECT 
  recvTime as time,
  attrValue as value,
  attrName as metric
FROM smart_default_lamp_luminosity 
WHERE attrName = 'luminosity'
  AND recvTime >= NOW() - INTERVAL 1 HOUR
ORDER BY recvTime DESC
```

## **Troubleshooting**

### **Grafana não acessível:**
```bash
# Verificar se container está rodando
docker ps | grep grafana

# Verificar logs
docker logs fiware-grafana

# Reiniciar container
docker restart fiware-grafana
```

### **Dados não aparecem:**
```bash
# Verificar se STH Comet está funcionando
curl -X GET "http://localhost:8666/STH/v1/contextEntities" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"

# Verificar se Orion está funcionando
curl -X GET "http://localhost:1026/v2/entities" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"
```

### **Datasource não funciona:**
```bash
# Verificar se MySQL está rodando
docker logs fiware-mysql

# Testar conexão MySQL
docker exec -it fiware-mysql mysql -u fiware -pfiware123 -e "SHOW DATABASES;"
```

## **Exemplos de Dashboards**

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

## **Scripts Úteis**

- `python3 configurar_grafana_dados.py` - Configuração automática
- `python3 configurar_subscricoes.py` - Configurar subscrições
- `python3 testar_subscricoes.py` - Testar subscrições
- `python3 consulta_mongodb.py` - Consultas de dados

## **Próximos Passos**

1. **Acesse o Grafana:** http://localhost:3000
2. **Configure os datasources** conforme instruções
3. **Crie dashboards** para seus dados específicos
4. **Configure alertas** para monitoramento
5. **Integre com outros sistemas** conforme necessário

Este guia fornece tudo que você precisa para visualizar dados do FIWARE no Grafana! 