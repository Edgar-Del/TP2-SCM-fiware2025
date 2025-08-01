#!/usr/bin/env python3
"""
Script para testar subscrições Orion e persistência com Cygnus
"""

import requests
import json
import time
from datetime import datetime

# Configurações
ORION_URL = "http://localhost:1026"
CYGNUS_URL = "http://localhost:5080"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306

def test_orion_connection():
    """Testa conexão com Orion"""
    print("🔍 Testando conexão com Orion...")
    
    try:
        response = requests.get(f"{ORION_URL}/version")
        if response.status_code == 200:
            print("✅ Orion está funcionando!")
            return True
        else:
            print(f"❌ Orion retornou erro: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar com Orion: {e}")
        return False

def test_cygnus_connection():
    """Testa conexão com Cygnus"""
    print("🔍 Testando conexão com Cygnus...")
    
    try:
        response = requests.get(f"{CYGNUS_URL}/v1/version")
        if response.status_code == 200:
            print("✅ Cygnus está funcionando!")
            return True
        else:
            print(f"❌ Cygnus retornou erro: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar com Cygnus: {e}")
        return False

def list_subscriptions():
    """Lista subscrições existentes"""
    print("\n📋 Listando subscrições...")
    
    headers = {
        'Accept': 'application/json',
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    
    try:
        response = requests.get(
            f"{ORION_URL}/v2/subscriptions",
            headers=headers
        )
        
        if response.status_code == 200:
            subscriptions = response.json()
            print(f"📊 Total de subscrições: {len(subscriptions)}")
            for sub in subscriptions:
                print(f"  - ID: {sub.get('id')}")
                print(f"    Descrição: {sub.get('description')}")
                print(f"    URL: {sub.get('notification', {}).get('http', {}).get('url')}")
                print("")
            return subscriptions
        else:
            print(f"❌ Erro ao listar subscrições: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Erro ao listar subscrições: {e}")
        return []

def create_test_entity():
    """Cria uma entidade de teste"""
    print("\n🧪 Criando entidade de teste...")
    
    entity_data = {
        "id": "urn:ngsi-ld:Lamp:test001",
        "type": "Lamp",
        "luminosity": {
            "type": "Number",
            "value": 150.5,
            "metadata": {
                "dateCreated": {
                    "type": "DateTime",
                    "value": datetime.now().isoformat()
                }
            }
        },
        "status": {
            "type": "Text",
            "value": "ON",
            "metadata": {
                "dateCreated": {
                    "type": "DateTime",
                    "value": datetime.now().isoformat()
                }
            }
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    
    try:
        response = requests.post(
            f"{ORION_URL}/v2/entities",
            headers=headers,
            json=entity_data
        )
        
        if response.status_code == 201:
            print("✅ Entidade de teste criada com sucesso!")
            return True
        else:
            print(f"❌ Erro ao criar entidade: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Erro ao criar entidade: {e}")
        return False

def update_test_entity():
    """Atualiza a entidade de teste para testar subscrições"""
    print("\n🔄 Atualizando entidade de teste...")
    
    update_data = {
        "luminosity": {
            "type": "Number",
            "value": 200.0,
            "metadata": {
                "dateModified": {
                    "type": "DateTime",
                    "value": datetime.now().isoformat()
                }
            }
        },
        "status": {
            "type": "Text",
            "value": "OFF",
            "metadata": {
                "dateModified": {
                    "type": "DateTime",
                    "value": datetime.now().isoformat()
                }
            }
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    
    try:
        response = requests.patch(
            f"{ORION_URL}/v2/entities/urn:ngsi-ld:Lamp:test001/attrs",
            headers=headers,
            json=update_data
        )
        
        if response.status_code == 204:
            print("✅ Entidade atualizada com sucesso!")
            return True
        else:
            print(f"❌ Erro ao atualizar entidade: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Erro ao atualizar entidade: {e}")
        return False

def test_cygnus_notification():
    """Testa notificação direta para Cygnus"""
    print("\n📡 Testando notificação para Cygnus...")
    
    notification_data = {
        "subscriptionId": "test-subscription",
        "data": [
            {
                "id": "urn:ngsi-ld:Lamp:test001",
                "type": "Lamp",
                "luminosity": {
                    "type": "Number",
                    "value": 250.0,
                    "metadata": {
                        "dateModified": {
                            "type": "DateTime",
                            "value": datetime.now().isoformat()
                        }
                    }
                },
                "status": {
                    "type": "Text",
                    "value": "ON",
                    "metadata": {
                        "dateModified": {
                            "type": "DateTime",
                            "value": datetime.now().isoformat()
                        }
                    }
                }
            }
        ]
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.post(
            f"{CYGNUS_URL}/notify",
            headers=headers,
            json=notification_data
        )
        
        if response.status_code == 200:
            print("✅ Notificação enviada com sucesso!")
            return True
        else:
            print(f"❌ Erro ao enviar notificação: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Erro ao enviar notificação: {e}")
        return False

def check_mysql_data():
    """Verifica dados no MySQL"""
    print("\n🗄️  Verificando dados no MySQL...")
    
    try:
        import subprocess
        
        # Comando para verificar dados no MySQL
        cmd = [
            "docker", "exec", "fiware-mysql",
            "mysql", "-u", "fiware", "-pfiware123", "fiware",
            "-e", "SHOW TABLES;"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Conexão com MySQL bem-sucedida!")
            print("📊 Tabelas encontradas:")
            print(result.stdout)
            return True
        else:
            print(f"❌ Erro ao conectar com MySQL: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar MySQL: {e}")
        return False

def check_mongodb_data():
    """Verifica dados no MongoDB"""
    print("\n🗄️  Verificando dados no MongoDB...")
    
    try:
        import subprocess
        
        # Comando para verificar dados no MongoDB
        cmd = [
            "docker", "exec", "fiware-mongo-historical",
            "mongo", "-u", "admin", "-p", "admin123",
            "--authenticationDatabase", "admin",
            "--eval", "show dbs"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Conexão com MongoDB bem-sucedida!")
            print("📊 Bancos encontrados:")
            print(result.stdout)
            return True
        else:
            print(f"❌ Erro ao conectar com MongoDB: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar MongoDB: {e}")
        return False

def main():
    """Função principal"""
    print("🧪 Testando Subscrições Orion + Cygnus")
    print("=" * 50)
    
    # 1. Testar conexões
    if not test_orion_connection():
        print("❌ Orion não está disponível")
        return
    
    if not test_cygnus_connection():
        print("⚠️  Cygnus não está disponível")
    
    # 2. Listar subscrições
    subscriptions = list_subscriptions()
    
    if not subscriptions:
        print("⚠️  Nenhuma subscrição encontrada. Execute configurar_subscricoes.py primeiro.")
        return
    
    # 3. Criar entidade de teste
    if not create_test_entity():
        print("⚠️  Erro ao criar entidade de teste")
    
    # 4. Aguardar um pouco
    print("\n⏳ Aguardando 5 segundos...")
    time.sleep(5)
    
    # 5. Atualizar entidade para testar subscrições
    if not update_test_entity():
        print("⚠️  Erro ao atualizar entidade")
    
    # 6. Testar notificação direta
    test_cygnus_notification()
    
    # 7. Verificar dados nos bancos
    check_mysql_data()
    check_mongodb_data()
    
    print("\n" + "=" * 50)
    print("✅ Teste concluído!")
    print("\n📋 Próximos passos:")
    print("1. Verifique os logs do Cygnus: docker logs fiware-cygnus")
    print("2. Verifique dados no MySQL: docker exec -it fiware-mysql mysql -u fiware -pfiware123 fiware")
    print("3. Verifique dados no MongoDB: docker exec -it fiware-mongo-historical mongo -u admin -p admin123 --authenticationDatabase admin")
    print("4. Configure Grafana para visualizar os dados")

if __name__ == "__main__":
    main() 