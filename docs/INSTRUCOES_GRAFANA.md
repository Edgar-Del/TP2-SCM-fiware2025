# 🎨 Grafana Integrado - Instruções Rápidas

## **Instalação**

### **1. Iniciar todos os serviços (incluindo Grafana):**
```bash
docker-compose up -d
```

### **2. Configurar Grafana:**
```bash
./configurar_grafana.sh
```

## **Acesso**

- **URL:** http://localhost:3000
- **Usuário:** admin
- **Senha:** admin123

## **Configuração Manual**

### **1. Criar Datasource:**
1. Acesse http://localhost:3000
2. Login: admin/admin123
3. Vá em **Configuration** > **Data Sources**
4. Clique em **Add data source**
5. Selecione **SimpleJSON**
6. Configure:
   - **Name:** `STH-Comet`
   - **URL:** `http://sth-comet:8666`
   - **Access:** `proxy`
7. Clique em **Save & Test**

### **2. Importar Dashboard:**
1. Vá em **+** > **Import**
2. Cole o conteúdo do arquivo `grafana/dashboards/fiware-dashboard.json`
3. Clique em **Load**
4. Configure o datasource
5. Clique em **Import**

## **Verificação**

### **Verificar se tudo está funcionando:**
```bash
# Verificar containers
docker ps

# Verificar logs do Grafana
docker logs fiware-grafana

# Verificar logs do STH Comet
docker logs fiware-sth-comet

# Testar STH Comet
curl -X GET "http://localhost:8666/STH/v1/contextEntities" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"
```

## **Troubleshooting**

### **Grafana não acessível:**
```bash
# Reiniciar Grafana
docker restart fiware-grafana

# Verificar logs
docker logs fiware-grafana
```

### **Dados não aparecem:**
```bash
# Verificar se há dados no MongoDB
docker exec -it fiware-mongo-historical mongo -u admin -p admin123 --authenticationDatabase admin
use sth_
db.getCollectionNames()
```

### **Datasource não funciona:**
```bash
# Verificar se STH Comet está funcionando
curl -X GET "http://localhost:8666/STH/v1/contextEntities" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"
```

## **Portas Utilizadas**

- **3000:** Grafana
- **1026:** Orion Context Broker
- **8666:** STH Comet
- **4041:** IoT Agent
- **1883:** MQTT Broker
- **27017:** MongoDB

## **Documentação Completa**

Para instruções detalhadas, consulte:
- `GUIA_GRAFANA_FIWARE.md` - Guia completo
- `GUIA_CONSULTAS_MONGODB.md` - Consultas de dados

## **Scripts Úteis**

- `./configurar_grafana.sh` - Configuração automática
- `python grafana_setup.py` - Configuração via Python
- `python consulta_mongodb.py` - Consultas de dados 