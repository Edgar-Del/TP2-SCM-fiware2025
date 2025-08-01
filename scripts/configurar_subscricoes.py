#!/usr/bin/env python3
"""
Script para configurar subscrições no Orion Context Broker
para persistir dados usando Cygnus
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

def wait_for_orion():
    """Aguarda o Orion estar disponível"""
    print("Aguardando Orion estar disponível...")
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{ORION_URL}/version")
            if response.status_code == 200:
                print("Orion está disponível!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(2)
        print(f"Tentativa {attempt + 1}/{max_attempts}...")
    
    print("Orion não está disponível")
    return False

def create_subscription_to_cygnus_mysql():
    """Cria subscrição para persistir dados no MySQL via Cygnus"""
    print("\nCriando subscrição para MySQL...")
    
    subscription_data = {
        "description": "Subscrição para persistir dados no MySQL via Cygnus",
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
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    
    try:
        response = requests.post(
            f"{ORION_URL}/v2/subscriptions",
            headers=headers,
            json=subscription_data
        )
        
        if response.status_code == 201:
            print("Subscrição para MySQL criada com sucesso!")
            subscription_id = response.headers.get('Location', '').split('/')[-1]
            print(f"ID da subscrição: {subscription_id}")
            return subscription_id
        else:
            print(f"Erro ao criar subscrição: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Erro na criação da subscrição: {e}")
        return None

def create_subscription_to_cygnus_mongodb():
    """Cria subscrição para persistir dados no MongoDB via Cygnus"""
    print("\nCriando subscrição para MongoDB...")
    
    subscription_data = {
        "description": "Subscrição para persistir dados no MongoDB via Cygnus",
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
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    
    try:
        response = requests.post(
            f"{ORION_URL}/v2/subscriptions",
            headers=headers,
            json=subscription_data
        )
        
        if response.status_code == 201:
            print("Subscrição para MongoDB criada com sucesso!")
            subscription_id = response.headers.get('Location', '').split('/')[-1]
            print(f"ID da subscrição: {subscription_id}")
            return subscription_id
        else:
            print(f"Erro ao criar subscrição: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Erro na criação da subscrição: {e}")
        return None

def list_subscriptions():
    """Lista todas as subscrições existentes"""
    print("\nListando subscrições existentes...")
    
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
            print(f"Erro ao listar subscrições: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Erro ao listar subscrições: {e}")
        return []

def delete_subscription(subscription_id):
    """Deleta uma subscrição específica"""
    print(f"\nDeletando subscrição {subscription_id}...")
    
    headers = {
        'Accept': 'application/json',
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    
    try:
        response = requests.delete(
            f"{ORION_URL}/v2/subscriptions/{subscription_id}",
            headers=headers
        )
        
        if response.status_code == 204:
            print("Subscrição deletada com sucesso!")
            return True
        else:
            print(f"Erro ao deletar subscrição: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Erro ao deletar subscrição: {e}")
        return False

def test_cygnus_connection():
    """Testa conexão com Cygnus"""
    print("\nTestando conexão com Cygnus...")
    
    try:
        response = requests.get(f"{CYGNUS_URL}/v1/version")
        if response.status_code == 200:
            print("Cygnus está funcionando!")
            return True
        else:
            print(f"Cygnus retornou erro: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Erro ao conectar com Cygnus: {e}")
        return False

def create_test_entity():
    """Cria uma entidade de teste para verificar as subscrições"""
    print("\nCriando entidade de teste...")
    
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
            print("Entidade de teste criada com sucesso!")
            return True
        else:
            print(f"Erro ao criar entidade: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"Erro ao criar entidade: {e}")
        return False

def main():
    """Função principal"""
    print("Configurando Subscrições Orion + Cygnus")
    print("=" * 50)
    
    # 1. Aguardar Orion
    if not wait_for_orion():
        return
    
    # 2. Testar Cygnus
    if not test_cygnus_connection():
        print("Cygnus não está disponível, mas continuando...")
    
    # 3. Listar subscrições existentes
    existing_subscriptions = list_subscriptions()
    
    # 4. Deletar subscrições existentes (opcional)
    if existing_subscriptions:
        print("\nDeletando subscrições existentes...")
        for sub in existing_subscriptions:
            delete_subscription(sub.get('id'))
    
    # 5. Criar subscrição para MySQL
    mysql_sub_id = create_subscription_to_cygnus_mysql()
    
    # 6. Criar subscrição para MongoDB
    mongodb_sub_id = create_subscription_to_cygnus_mongodb()
    
    # 7. Criar entidade de teste
    create_test_entity()
    
    # 8. Listar subscrições finais
    list_subscriptions()
    
    print("\n" + "=" * 50)
    print("Configuração concluída!")
    print("\nPróximos passos (para testar):")
    print("1. Verifique os logs do Cygnus: docker logs fiware-cygnus")
    print("2. Verifique os dados no MySQL: docker exec -it fiware-mysql mysql -u fiware -pfiware123 fiware")
    print("3. Verifique os dados no MongoDB: docker exec -it fiware-mongo-historical mongo -u admin -p admin123 --authenticationDatabase admin")
    print("4. Teste atualizando uma entidade para ver as notificações")

if __name__ == "__main__":
    main() 