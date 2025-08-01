#!/bin/bash

echo "🚀 FIWARE IoT Platform - Instalação Rápida"
echo "=========================================="

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Instale o Docker Compose primeiro."
    exit 1
fi

# Verificar se Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não está instalado. Instale o Python3 primeiro."
    exit 1
fi

echo "✅ Pré-requisitos verificados!"

# Parar serviços existentes
echo "📋 Parando serviços existentes..."
docker-compose down 2>/dev/null

# Instalar dependências Python
echo "🐍 Instalando dependências Python..."
pip3 install -r config/requirements.txt

# Iniciar serviços
echo "🐳 Iniciando serviços..."
docker-compose up -d

# Aguardar serviços iniciarem
echo "⏳ Aguardando serviços iniciarem..."
sleep 30

# Verificar se serviços estão rodando
echo "🔍 Verificando serviços..."
python3 scripts/fiware_manager.py check

# Executar configuração automática
echo "⚙️  Executando configuração automática..."
python3 scripts/fiware_manager.py setup

echo ""
echo "🎉 Instalação concluída!"
echo "========================"
echo "🌐 Acesse os serviços:"
echo "  - Grafana: http://localhost:3000 (admin/admin123)"
echo "  - Orion: http://localhost:1026"
echo "  - STH Comet: http://localhost:8666"
echo ""
echo "📋 Comandos úteis:"
echo "  - Status: python3 scripts/fiware_manager.py status"
echo "  - Testar: python3 scripts/fiware_manager.py test-data"
echo "  - Logs: docker-compose logs -f"
echo ""
echo "📚 Documentação: docs/" 