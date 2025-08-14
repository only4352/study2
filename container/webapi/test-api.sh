#!/bin/bash

echo "=== WebAPI Service Test ==="
echo "Waiting for service to start..."

# サービスが起動するまで待機
sleep 10

# ヘルスチェック
echo "Testing health endpoint..."
curl -s http://localhost:8001/health | jq . 2>/dev/null || curl -s http://localhost:8001/health

echo -e "\nTesting root endpoint..."
curl -s http://localhost:8001/ | jq . 2>/dev/null || curl -s http://localhost:8001/

echo -e "\nTesting items endpoint..."
curl -s http://localhost:8001/items | jq . 2>/dev/null || curl -s http://localhost:8001/items

echo -e "\n=== Test completed ==="
