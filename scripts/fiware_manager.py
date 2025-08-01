#!/usr/bin/env python3
"""
FIWARE Manager - Script principal para gerenciar o projecto FIWARE
Este é ou será o nosso arquivo de inicialização "automatizada" do projecto
"""

import requests
import json
import time
import subprocess
import sys
import os
from datetime import datetime

# Configurações
ORION_URL = "http://localhost:1026"
CYGNUS_URL = "http://localhost:5080"
STH_COMET_URL = "http://localhost:8666"
GRAFANA_URL = "http://localhost:3000"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306

class FiwareManager:
    """Classe principal para gerenciar o projeto FIWARE"""
    
    def __init__(self):
        self.orion_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'fiware-service': 'smart',
            'fiware-servicepath': '/'
        }
    
    def check_services(self):
        """Verifica se todos os serviços estão funcionando"""
        print("Verificando serviços...")
        
        services = {
            "Orion": f"{ORION_URL}/version",
            "STH Comet": f"{STH_COMET_URL}/STH/v1/contextEntities",
            "Grafana": f"{GRAFANA_URL}/api/health",
            "Cygnus": f"{CYGNUS_URL}/v1/version"
        }
        
        for service_name, url in services.items():
            try:
                if service_name == "STH Comet":
                    response = requests.get(url, headers=self.orion_headers)
                else:
                    response = requests.get(url)
                
                if response.status_code in [200, 404]:  # 404 é OK para STH Comet sem dados
                    print(f"{service_name} está funcionando")
                else:
                    print(f"{service_name} retornou erro: {response.status_code}")
            except Exception as e:
                print(f"{service_name} não está acessível: {e}")
    
    def wait_for_orion(self):
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
    
    def create_subscriptions(self):
        """Cria subscrições para persistência de dados"""
        print("\nCriando subscrições...")
        
        # Deletar subscrições existentes
        self.delete_existing_subscriptions()
        
        # Criar subscrição para Cygnus
        subscription_data = {
            "description": "Subscrição para persistir dados via Cygnus",
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
                "attrsFormat": "legacy"
            },
            "expires": "2030-12-31T23:59:59.000Z",
            "throttling": 5
        }
        
        try:
            response = requests.post(
                f"{ORION_URL}/v2/subscriptions",
                headers=self.orion_headers,
                json=subscription_data
            )
            
            if response.status_code == 201:
                print("Subscrição criada com sucesso!")
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
    
    def delete_existing_subscriptions(self):
        """Deleta subscrições existentes"""
        try:
            response = requests.get(
                f"{ORION_URL}/v2/subscriptions",
                headers=self.orion_headers
            )
            
            if response.status_code == 200:
                subscriptions = response.json()
                for sub in subscriptions:
                    sub_id = sub.get('id')
                    if sub_id:
                        requests.delete(
                            f"{ORION_URL}/v2/subscriptions/{sub_id}",
                            headers=self.orion_headers
                        )
                        print(f"Subscrição {sub_id} deletada")
        except Exception as e:
            print(f"Erro ao deletar subscrições: {e}")
    
    def generate_test_data(self):
        """Gera dados de teste"""
        print("\n Gerando dados de teste...")
        
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
        
        try:
            # Criar entidade
            response = requests.post(
                f"{ORION_URL}/v2/entities",
                headers=self.orion_headers,
                json=entity_data
            )
            
            if response.status_code == 201:
                print("Entidade criada com sucesso!")
                
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
                        f"{ORION_URL}/v2/entities/urn:ngsi-ld:Lamp:001/attrs",
                        headers=self.orion_headers,
                        json=update_data
                    )
                    
                    if response.status_code == 204:
                        print(f"Actualização {i}/10 realizada")
                    else:
                        print(f"Erro na actualização {i}")
                    
                    time.sleep(1)
                
                return True
            else:
                print(f"Erro ao criar entidade: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Erro ao gerar dados de teste: {e}")
            return False
    
    def configure_grafana(self):
        """Configura o Grafana"""
        print("\nConfigurando Grafana...")
        
        # Aguardar Grafana estar disponível
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{GRAFANA_URL}/api/health")
                if response.status_code == 200:
                    print("Grafana está disponível!")
                    break
            except requests.exceptions.ConnectionError:
                pass
            time.sleep(2)
            print(f"Tentativa {attempt + 1}/{max_attempts}...")
        else:
            print("Grafana não está disponível")
            return False
        
        # Criar datasource MySQL
        self.create_mysql_datasource()
        
        return True
    
    def create_mysql_datasource(self):
        """Cria datasource MySQL no Grafana"""
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
                auth=("admin", "admin123"),
                json=datasource_config
            )
            
            if response.status_code == 200:
                print("Datasource MySQL criado com sucesso!")
                return True
            else:
                print(f"Erro ao criar datasource MySQL: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Erro na criação do datasource MySQL: {e}")
            return False
    
    def check_data_persistence(self):
        """Verifica a persistência de dados"""
        print("\nVerificando persistência de dados...")
        
        # Verificar MySQL
        try:
            cmd = [
                "docker", "exec", "fiware-mysql",
                "mysql", "-u", "fiware", "-pfiware123", "fiware",
                "-e", "SHOW TABLES;"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Conexão com MySQL bem-sucedida!")
                if result.stdout.strip():
                    print("Tabelas encontradas no MySQL")
                else:
                    print("Nenhuma tabela encontrada no MySQL")
            else:
                print(f"Erro ao conectar com MySQL: {result.stderr}")
        except Exception as e:
            print(f"Erro ao verificar MySQL: {e}")
        
        # Verificar MongoDB
        try:
            cmd = [
                "docker", "exec", "fiware-mongo-historical",
                "mongo", "-u", "admin", "-p", "admin123",
                "--authenticationDatabase", "admin",
                "--eval", "show dbs"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Conexão com MongoDB bem-sucedida!")
            else:
                print(f"Erro ao conectar com MongoDB: {result.stderr}")
        except Exception as e:
            print(f"Erro ao verificar MongoDB: {e}")
    
    def show_status(self):
        """Mostra o status atual do sistema"""
        print("\nStatus do Sistema FIWARE")
        print("=" * 40)
        
        # Verificar containers
        try:
            result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
            if result.returncode == 0:
                containers = result.stdout
                fiware_containers = [line for line in containers.split('\n') if 'fiware' in line]
                print(f"🐳 Containers FIWARE ativos: {len(fiware_containers)}")
                for container in fiware_containers[:5]:  # Mostrar apenas os primeiros 5
                    if container.strip():
                        print(f"  - {container.split()[-1]}")
            else:
                print("erro ao verificar containers")
        except Exception as e:
            print(f"Erro ao verificar containers: {e}")
        
        # Verificar serviços
        self.check_services()
        
        # Verificar subscrições
        try:
            response = requests.get(
                f"{ORION_URL}/v2/subscriptions",
                headers=self.orion_headers
            )
            
            if response.status_code == 200:
                subscriptions = response.json()
                print(f"\nSubscrições activas: {len(subscriptions)}")
                for sub in subscriptions:
                    print(f"  - {sub.get('description', 'Sem descrição')}")
            else:
                print("\nErro ao verificar subscrições")
        except Exception as e:
            print(f"\nErro ao verificar subscrições: {e}")
    
    def run_full_setup(self):
        """Executa configuração completa do sistema"""
        print("Configuração Completa do Sistema FIWARE")
        print("=" * 50)
        
        # 1. Verificar serviços
        self.check_services()
        
        # 2. Aguardar Orion
        if not self.wait_for_orion():
            return
        
        # 3. Criar subscrições
        self.create_subscriptions()
        
        # 4. Gerar dados de teste
        self.generate_test_data()
        
        # 5. Configurar Grafana
        self.configure_grafana()
        
        # 6. Verificar persistência
        self.check_data_persistence()
        
        print("\n" + "=" * 50)
        print("Configuração completa finalizada!")
        print("\nPróximos passos:")
        print("1. Acesse o Grafana: http://localhost:3000 (admin/admin123)")
        print("2. Configure o datasource STH Comet manualmente")
        print("3. Crie dashboards para seus dados")
        print("4. Teste com dados reais do seu ESP32 (proximo desafio - ainda não implementado)")
    
    def show_help(self):
        """Mostra ajuda do script"""
        print("""
FIWARE Manager - Gerenciador do Projeto FIWARE

Uso: python3 fiware_manager.py [comando]

Comandos disponíveis:
  status          - Mostra status atual do sistema
  setup           - Executa configuração completa
  check           - Verifica se todos os serviços estão funcionando
  subscriptions   - Cria subscrições para persistência
  test-data       - Gera dados de teste
  grafana         - Configura Grafana
  persistence     - Verifica persistência de dados
  help            - Mostra esta ajuda

Exemplos:
  python3 fiware_manager.py status
  python3 fiware_manager.py setup
  python3 fiware_manager.py check
        """)

def main():
    """Função principal"""
    manager = FiwareManager()
    
    if len(sys.argv) < 2:
        manager.show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        manager.show_status()
    elif command == "setup":
        manager.run_full_setup()
    elif command == "check":
        manager.check_services()
    elif command == "subscriptions":
        manager.create_subscriptions()
    elif command == "test-data":
        manager.generate_test_data()
    elif command == "grafana":
        manager.configure_grafana()
    elif command == "persistence":
        manager.check_data_persistence()
    elif command == "help":
        manager.show_help()
    else:
        print(f"Comando '{command}' não reconhecido")
        manager.show_help()

if __name__ == "__main__":
    main() 