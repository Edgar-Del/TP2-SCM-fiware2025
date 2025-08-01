#!/bin/bash

echo "🚀 Configurando Grafana para FIWARE"
echo "=================================="

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Inicie o Docker primeiro."
    exit 1
fi

# Parar serviços existentes se estiverem rodando
echo "📋 Parando serviços existentes..."
docker-compose down 2>/dev/null

# Criar estrutura de pastas
echo "📁 Criando estrutura de pastas..."
mkdir -p grafana/provisioning/datasources
mkdir -p grafana/provisioning/dashboards
mkdir -p grafana/dashboards

# Iniciar serviços com Grafana
echo "🐳 Iniciando serviços com Grafana..."
docker-compose up -d

# Aguardar serviços iniciarem
echo "⏳ Aguardando serviços iniciarem..."
sleep 30

# Verificar se Grafana está rodando
echo "🔍 Verificando se Grafana está rodando..."
if docker ps | grep -q "fiware-grafana"; then
    echo "✅ Grafana está rodando!"
else
    echo "❌ Grafana não está rodando. Verifique os logs:"
    docker logs fiware-grafana
    exit 1
fi

# Verificar se STH Comet está funcionando
echo "🔍 Verificando STH Comet..."
if curl -s "http://localhost:8666/STH/v1/contextEntities" > /dev/null; then
    echo "✅ STH Comet está funcionando!"
else
    echo "⚠️  STH Comet não está respondendo. Verifique os logs:"
    docker logs fiware-sth-comet
fi

# Executar script de configuração Python
echo "🐍 Executando configuração automática..."
if command -v python3 &> /dev/null; then
    pip3 install requests 2>/dev/null
    python3 grafana_setup.py
else
    echo "⚠️  Python3 não encontrado. Configure manualmente:"
    echo "1. Acesse http://localhost:3000"
    echo "2. Login: admin/admin123"
    echo "3. Configure datasource STH-Comet"
fi

echo ""
echo "🎉 Configuração concluída!"
echo "=========================="
echo "🌐 Grafana: http://localhost:3000"
echo "👤 Usuário: admin"
echo "🔑 Senha: admin123"
echo ""
echo "📊 STH Comet: http://localhost:8666"
echo "🔧 Orion: http://localhost:1026"
echo ""
echo "📋 Próximos passos:"
echo "1. Acesse o Grafana"
echo "2. Configure o datasource STH-Comet"
echo "3. Importe o dashboard JSON"
echo "4. Configure as queries para seus dados"
echo ""
echo "📚 Documentação: GUIA_GRAFANA_FIWARE.md" 