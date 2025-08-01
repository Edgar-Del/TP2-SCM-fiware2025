#!/usr/bin/env python3
"""
Script para configurar Grafana com dados do FIWARE
Cria datasource e dashboard automaticamente
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

def create_datasource():
    """Cria datasource HTTP para STH Comet"""
    print("\n📊 Criando datasource...")
    
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
            print("✅ Datasource criado com sucesso!")
            return True
        else:
            print(f"❌ Erro ao criar datasource: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Erro na criação do datasource: {e}")
        return False

def create_dashboard():
    """Cria dashboard para visualizar dados do FIWARE"""
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

def test_sth_comet():
    """Testa conexão com STH Comet"""
    print("\n🔍 Testando conexão com STH Comet...")
    
    try:
        response = requests.get(
            f"{STH_COMET_URL}/STH/v1/contextEntities",
            headers={
                'fiware-service': 'smart',
                'fiware-servicepath': '/'
            }
        )
        
        if response.status_code == 200:
            print("✅ STH Comet está funcionando!")
            data = response.json()
            print(f"📊 Entidades encontradas: {len(data.get('contextResponses', []))}")
            return True
        else:
            print(f"❌ STH Comet retornou erro: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao conectar com STH Comet: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Configurando Grafana para FIWARE")
    print("=" * 50)
    
    # 1. Aguardar Grafana
    if not wait_for_grafana():
        return
    
    # 2. Testar STH Comet
    if not test_sth_comet():
        print("⚠️  STH Comet não está disponível, mas continuando...")
    
    # 3. Criar datasource
    if not create_datasource():
        print("⚠️  Erro ao criar datasource")
    
    # 4. Criar dashboard
    if not create_dashboard():
        print("⚠️  Erro ao criar dashboard")
    
    print("\n" + "=" * 50)
    print("✅ Configuração concluída!")
    print(f"🌐 Acesse o Grafana em: {GRAFANA_URL}")
    print("👤 Usuário: admin")
    print("🔑 Senha: admin123")
    print("\n📋 Próximos passos:")
    print("1. Faça login no Grafana")
    print("2. Vá em Configuration > Data Sources")
    print("3. Configure o datasource STH-Comet")
    print("4. Importe o dashboard JSON")
    print("5. Configure as queries para seus dados")

if __name__ == "__main__":
    main() 