#!/bin/bash

echo "🚀 Setting up Pyatiletka in GitHub Codespace..."
echo ""

# Create required directories
echo "📁 Creating directory structure..."
mkdir -p platform/airflow/{dags,plugins,logs}
mkdir -p infrastructure/grafana/provisioning/datasources
mkdir -p analytics/dbt_pyatiletka/models/{staging,marts/heavy_industry}
mkdir -p scripts/data-generators

# Start Docker services
echo "🐳 Starting Docker services..."
echo "This will take 2-3 minutes on first run..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Access your services:"
echo "   - Airflow: https://${CODESPACE_NAME}-8080.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
echo "   - FastAPI: https://${CODESPACE_NAME}-8000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}/docs"
echo "   - Grafana: https://${CODESPACE_NAME}-3000.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
echo "   - MinIO Console: https://${CODESPACE_NAME}-9001.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
echo ""
echo "📝 Next steps:"
echo "   1. Generate data: python scripts/data-generators/data-generator.py"
echo "   2. Open Airflow and trigger the DAG"
echo "   3. Run dbt: cd analytics/dbt_pyatiletka && dbt run"
echo ""