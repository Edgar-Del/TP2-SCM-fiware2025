# FIWARE IoT Platform - Configurações de Ambiente

# URLs dos Serviços
ORION_URL = "http://localhost:1026"
STH_COMET_URL = "http://localhost:8666"
GRAFANA_URL = "http://localhost:3000"
CYGNUS_URL = "http://localhost:5080"

# Credenciais
GRAFANA_USER = "admin"
GRAFANA_PASSWORD = "admin123"
MYSQL_USER = "fiware"
MYSQL_PASSWORD = "fiware123"
MONGODB_USER = "admin"
MONGODB_PASSWORD = "admin123"

# Configurações do Projeto
FIWARE_SERVICE = "smart"
FIWARE_SERVICEPATH = "/"

# Portas dos Serviços
ORION_PORT = 1026
STH_COMET_PORT = 8666
GRAFANA_PORT = 3000
MQTT_PORT = 1883
MYSQL_PORT = 3306
MONGODB_PORT = 27017

# Headers padrão para Orion
ORION_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'fiware-service': FIWARE_SERVICE,
    'fiware-servicepath': FIWARE_SERVICEPATH
} 