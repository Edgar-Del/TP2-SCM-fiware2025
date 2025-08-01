#!/bin/bash

echo "🎨 Configurando Grafana para FIWARE"
echo "==================================="

# Verificar se Grafana está rodando
echo "🔍 Verificando se Grafana está rodando..."
if ! docker ps | grep -q "fiware-grafana"; then
    echo "❌ Grafana não está rodando. Inicie os serviços primeiro:"
    echo "   docker-compose up -d"
    exit 1
fi

echo "✅ Grafana está rodando!"

# Aguardar Grafana estar pronto
echo "⏳ Aguardando Grafana estar pronto..."
sleep 10

# Criar estrutura de pastas se não existir
echo "📁 Criando estrutura de pastas..."
mkdir -p grafana/provisioning/datasources
mkdir -p grafana/provisioning/dashboards
mkdir -p grafana/dashboards

# Verificar se STH Comet está funcionando
echo "🔍 Verificando STH Comet..."
if curl -s "http://localhost:8666/STH/v1/contextEntities" > /dev/null; then
    echo "✅ STH Comet está funcionando!"
else
    echo "⚠️  STH Comet não está respondendo. Verifique os logs:"
    docker logs fiware-sth-comet
fi

# Executar configuração Python se disponível
echo "🐍 Executando configuração automática..."
if command -v python3 &> /dev/null; then
    pip3 install requests 2>/dev/null
    if [ -f "grafana_setup.py" ]; then
        python3 grafana_setup.py
    else
        echo "⚠️  Script grafana_setup.py não encontrado"
    fi
else
    echo "⚠️  Python3 não encontrado. Configure manualmente:"
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
echo "1. Acesse http://localhost:3000"
echo "2. Faça login com admin/admin123"
echo "3. Configure o datasource STH-Comet"
echo "4. Importe o dashboard JSON"
echo "5. Configure as queries para seus dados"
echo ""
echo "📚 Documentação: GUIA_GRAFANA_FIWARE.md" 