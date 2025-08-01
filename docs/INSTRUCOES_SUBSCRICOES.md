# 📡 Subscrições Orion + Cygnus - Instruções Rápidas

## **Instalação**

### **1. Iniciar todos os serviços (incluindo Cygnus e MySQL):**
```bash
docker-compose up -d
```

### **2. Configurar subscrições:**
```bash
python configurar_subscricoes.py
```

### **3. Testar subscrições:**
```bash
python testar_subscricoes.py
```

## **Componentes Adicionados**

- **MySQL:** Porta 3306 (fiware/fiware123)
- **Cygnus:** Porta 5080 (serviço), 5050 (admin)

## **Verificação**

### **Verificar se tudo está funcionando:**
```bash
# Verificar containers
docker ps

# Verificar logs do Cygnus
docker logs fiware-cygnus

# Verificar logs do MySQL
docker logs fiware-mysql

# Testar Orion
curl -X GET "http://localhost:1026/v2/version"

# Testar Cygnus
curl -X GET "http://localhost:5080/v1/version"
```

## **Gerenciamento de Subscrições**

### **Listar subscrições:**
```bash
curl -X GET "http://localhost:1026/v2/subscriptions" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"
```

### **Deletar subscrição:**
```bash
curl -X DELETE "http://localhost:1026/v2/subscriptions/{subscription_id}" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"
```

## **Verificação de Dados**

### **Verificar dados no MySQL:**
```bash
docker exec -it fiware-mysql mysql -u fiware -pfiware123 fiware
SHOW TABLES;
SELECT * FROM smart_default_lamp;
```

### **Verificar dados no MongoDB:**
```bash
docker exec -it fiware-mongo-historical mongo -u admin -p admin123 --authenticationDatabase admin
use cygnus
show collections
db.smart_default_lamp.find()
```

## **Troubleshooting**

### **Subscrição não funciona:**
```bash
# Verificar se Orion está funcionando
curl -X GET "http://localhost:1026/v2/version"

# Verificar se Cygnus está funcionando
curl -X GET "http://localhost:5080/v1/version"

# Verificar logs do Cygnus
docker logs fiware-cygnus
```

### **Dados não aparecem no banco:**
```bash
# Verificar se subscrição foi criada
curl -X GET "http://localhost:1026/v2/subscriptions" \
  -H "fiware-service: smart" \
  -H "fiware-servicepath: /"

# Verificar logs do Cygnus
docker logs fiware-cygnus
```

## **Portas Utilizadas**

- **1026:** Orion Context Broker
- **5080:** Cygnus (serviço)
- **5050:** Cygnus (admin)
- **3306:** MySQL
- **27017:** MongoDB

## **Documentação Completa**

Para instruções detalhadas, consulte:
- `GUIA_SUBSCRICOES_CYGNUS.md` - Guia completo

## **Scripts Úteis**

- `python configurar_subscricoes.py` - Configurar subscrições
- `python testar_subscricoes.py` - Testar subscrições
- `python consulta_mongodb.py` - Consultas de dados 