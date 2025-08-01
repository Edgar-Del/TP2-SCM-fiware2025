#!/usr/bin/env python3
"""
Script para configurar Grafana com dados do STH Comet
"""

import requests
import json
import time
from datetime import datetime

# Configurações
GRAFANA_URL = "http://localhost:3000"
GRAFANA_USER = "admin"
GRAFANA_PASSWORD = "admin123"
STH_COMET_URL = "http://localhost:8666"

def wait_for_grafana():
    """Aguarda o Grafana estar disponível"""
    print("Aguardando Grafana estar disponível...")
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{GRAFANA_URL}/api/health")
            if response.status_code == 200:
                print("✅ Grafana está disponível!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(2)
        print(f"Tentativa {attempt + 1}/{max_attempts}...")
    
    print("❌ Grafana não está disponível")
    return False

def create_datasource_sth_comet():
    """Cria datasource para STH Comet"""
    print("\n📊 Criando datasource STH Comet...")
    
    datasource_config = {
        "name": "STH-Comet",
        "type": "grafana-simple-json-datasource",
        "access": "proxy",
        "url": f"http://sth-comet:8666",
        "jsonData": {
            "defaultDatabase": "sth_"
        },
        "editable": True
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.post(
            f"{GRAFANA_URL}/api/datasources",
            headers=headers,
            auth=(GRAFANA_USER, GRAFANA_PASSWORD),
            json=datasource_config
        )
        
        if response.status_code == 200:
            print("✅ Datasource STH Comet criado com sucesso!")
            return True
        else:
            print(f"❌ Erro ao criar datasource: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Erro na criação do datasource: {e}")
        return False

def create_datasource_mysql():
    """Cria datasource para MySQL"""
    print("\n📊 Criando datasource MySQL...")
    
    datasource_config = {
        "name": "MySQL",
        "type": "mysql",
        "access": "proxy",
        "url": "mysql:3306",
        "database": "fiware",
        "user": "fiware",
        "secureJsonData": {
            "password": "fiware123"
        },
        "jsonData": {
            "maxOpenConns": 0,
            "maxIdleConns": 2,
            "connMaxLifetime": 14400
        },
        "editable": True
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.post(
            f"{GRAFANA_URL}/api/datasources",
            headers=headers,
            auth=(GRAFANA_USER, GRAFANA_PASSWORD),
            json=datasource_config
        )
        
        if response.status_code == 200:
            print("✅ Datasource MySQL criado com sucesso!")
            return True
        else:
            print(f"❌ Erro ao criar datasource MySQL: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Erro na criação do datasource MySQL: {e}")
        return False

def create_dashboard():
    """Cria dashboard para visualizar dados"""
    print("\n📈 Criando dashboard...")
    
    dashboard_config = {
        "dashboard": {
            "title": "FIWARE IoT Dashboard",
            "uid": "fiware-iot-dashboard",
            "tags": ["fiware", "iot"],
            "time": {
                "from": "now-1h",
                "to": "now"
            },
            "panels": [
                {
                    "title": "Dados de Luminosidade",
                    "type": "graph",
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
                    "targets": [
                        {
                            "expr": "luminosity",
                            "legendFormat": "Luminosidade",
                            "refId": "A"
                        }
                    ],
                    "datasource": "STH-Comet"
                },
                {
                    "title": "Status do LED",
                    "type": "stat",
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
                    "targets": [
                        {
                            "expr": "status",
                            "legendFormat": "Status",
                            "refId": "A"
                        }
                    ],
                    "datasource": "STH-Comet"
                }
            ]
        },
        "overwrite": True
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.post(
            f"{GRAFANA_URL}/api/dashboards/db",
            headers=headers,
            auth=(GRAFANA_USER, GRAFANA_PASSWORD),
            json=dashboard_config
        )
        
        if response.status_code == 200:
            print("✅ Dashboard criado com sucesso!")
            return True
        else:
            print(f"❌ Erro ao criar dashboard: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Erro na criação do dashboard: {e}")
        return False

def generate_test_data():
    """Gera dados de teste"""
    print("\n🧪 Gerando dados de teste...")
    
    # Criar entidade
    entity_data = {
        "id": "urn:ngsi-ld:Lamp:001",
        "type": "Lamp",
        "luminosity": {
            "type": "Number",
            "value": 150
        },
        "status": {
            "type": "Text",
            "value": "ON"
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    
    try:
        # Criar entidade
        response = requests.post(
            "http://localhost:1026/v2/entities",
            headers=headers,
            json=entity_data
        )
        
        if response.status_code == 201:
            print("✅ Entidade criada com sucesso!")
            
            # Atualizar entidade várias vezes para gerar dados
            for i in range(1, 11):
                update_data = {
                    "luminosity": {
                        "type": "Number",
                        "value": 100 + (i * 10)
                    },
                    "status": {
                        "type": "Text",
                        "value": "ON" if i % 2 == 0 else "OFF"
                    }
                }
                
                response = requests.patch(
                    f"http://localhost:1026/v2/entities/urn:ngsi-ld:Lamp:001/attrs",
                    headers=headers,
                    json=update_data
                )
                
                if response.status_code == 204:
                    print(f"✅ Atualização {i}/10 realizada")
                else:
                    print(f"❌ Erro na atualização {i}")
                
                time.sleep(1)
            
            return True
        else:
            print(f"❌ Erro ao criar entidade: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao gerar dados de teste: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Configurando Grafana para Visualização de Dados")
    print("=" * 50)
    
    # 1. Aguardar Grafana
    if not wait_for_grafana():
        return
    
    # 2. Gerar dados de teste
    generate_test_data()
    
    # 3. Criar datasource STH Comet
    create_datasource_sth_comet()
    
    # 4. Criar datasource MySQL
    create_datasource_mysql()
    
    # 5. Criar dashboard
    create_dashboard()
    
    print("\n" + "=" * 50)
    print("✅ Configuração concluída!")
    print(f"🌐 Acesse o Grafana em: {GRAFANA_URL}")
    print("👤 Usuário: admin")
    print("🔑 Senha: admin123")
    print("\n📋 Próximos passos:")
    print("1. Faça login no Grafana")
    print("2. Vá em Configuration > Data Sources")
    print("3. Configure os datasources STH-Comet e MySQL")
    print("4. Importe o dashboard JSON")
    print("5. Configure as queries para seus dados")

if __name__ == "__main__":
    main() 