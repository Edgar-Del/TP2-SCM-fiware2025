#!/usr/bin/env python3
"""
Script para consultar dados persistidos no MongoDB do FIWARE
Demonstra diferentes formas de acessar os dados
"""

import requests
import json
from datetime import datetime
import pymongo
from pymongo import MongoClient

# Configurações
IP_ADDRESS = "localhost"  # Altere para seu IP
PORT_STH = 8666
MONGO_HOST = "localhost"
MONGO_PORT = 27017

def consulta_sth_comet():
    """
    Consulta dados via API REST do STH Comet
    """
    print("=== CONSULTA VIA STH COMET ===")
    
    # URL base do STH Comet
    base_url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1"
    
    # Headers necessários
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    
    # 1. Listar entidades disponíveis
    print("\n1. Listando entidades disponíveis:")
    try:
        response = requests.get(f"{base_url}/contextEntities", headers=headers)
        if response.status_code == 200:
            entities = response.json()
            print(json.dumps(entities, indent=2))
        else:
            print(f"Erro: {response.status_code}")
    except Exception as e:
        print(f"Erro na consulta: {e}")
    
    # 2. Consultar dados de luminosidade
    print("\n2. Consultando dados de luminosidade (últimos 10):")
    try:
        url = f"{base_url}/contextEntities/type/Lamp/id/urn:ngsi-ld:Lamp:001/attributes/luminosity?lastN=10"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=2))
        else:
            print(f"Erro: {response.status_code}")
    except Exception as e:
        print(f"Erro na consulta: {e}")
    
    # 3. Consultar dados por período
    print("\n3. Consultando dados por período:")
    try:
        # Últimas 24 horas
        url = f"{base_url}/contextEntities/type/Lamp/id/urn:ngsi-ld:Lamp:001/attributes/luminosity?hLimit=100&hOffset=0"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"Total de registros: {len(data.get('contextResponses', []))}")
        else:
            print(f"Erro: {response.status_code}")
    except Exception as e:
        print(f"Erro na consulta: {e}")

def consulta_mongodb_direto():
    """
    Consulta dados diretamente no MongoDB
    """
    print("\n=== CONSULTA DIRETA NO MONGODB ===")
    
    try:
        # Conectar ao MongoDB histórico
        client = MongoClient(f"mongodb://admin:admin123@{MONGO_HOST}:{MONGO_PORT}/admin")
        
        # Listar bancos de dados
        print("\n1. Bancos de dados disponíveis:")
        databases = client.list_database_names()
        for db in databases:
            print(f"  - {db}")
        
        # Acessar banco do STH Comet
        db = client['sth_']
        print(f"\n2. Coleções no banco 'sth_':")
        collections = db.list_collection_names()
        for collection in collections:
            print(f"  - {collection}")
        
        # Consultar dados de uma coleção específica
        if collections:
            collection_name = collections[0]
            print(f"\n3. Dados da coleção '{collection_name}':")
            collection = db[collection_name]
            
            # Primeiros 5 documentos
            documents = collection.find().limit(5)
            for doc in documents:
                print(json.dumps(doc, indent=2, default=str))
        
        client.close()
        
    except Exception as e:
        print(f"Erro na conexão com MongoDB: {e}")

def consulta_orion_context_broker():
    """
    Consulta dados via Orion Context Broker
    """
    print("\n=== CONSULTA VIA ORION CONTEXT BROKER ===")
    
    # URL do Orion
    orion_url = f"http://{IP_ADDRESS}:1026/v2"
    
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    
    # 1. Listar entidades
    print("\n1. Entidades no Orion:")
    try:
        response = requests.get(f"{orion_url}/entities", headers=headers)
        if response.status_code == 200:
            entities = response.json()
            print(json.dumps(entities, indent=2))
        else:
            print(f"Erro: {response.status_code}")
    except Exception as e:
        print(f"Erro na consulta: {e}")
    
    # 2. Consultar entidade específica
    print("\n2. Dados da entidade Lamp:001:")
    try:
        response = requests.get(f"{orion_url}/entities/urn:ngsi-ld:Lamp:001", headers=headers)
        if response.status_code == 200:
            entity = response.json()
            print(json.dumps(entity, indent=2))
        else:
            print(f"Erro: {response.status_code}")
    except Exception as e:
        print(f"Erro na consulta: {e}")

def main():
    """
    Função principal que executa todas as consultas
    """
    print("CONSULTAS DE DADOS DO FIWARE")
    print("=" * 50)
    
    # 1. Consulta via STH Comet
    consulta_sth_comet()
    
    # 2. Consulta direta no MongoDB
    consulta_mongodb_direto()
    
    # 3. Consulta via Orion
    consulta_orion_context_broker()
    
    print("\n" + "=" * 50)
    print("FIM DAS CONSULTAS")

if __name__ == "__main__":
    main() 