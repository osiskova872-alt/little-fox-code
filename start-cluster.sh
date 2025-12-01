#!/bin/bash
# Start Redis Cluster with 9 Nodes

echo "🚀 Starting Redis Cluster (9 nodes)..."
echo "========================================="

# Check if Redis is installed
if ! command -v redis-server &> /dev/null; then
    echo "❌ Redis is not installed!"
    echo "Install Redis first:"
    echo "  Ubuntu/Debian: sudo apt install redis-server"
    echo "  Mac: brew install redis"
    echo "  Windows: Download from https://redis.io"
    exit 1
fi

# Create data directories
echo "Creating data directories..."
for port in {7001..7009}; do
    mkdir -p "data-$port"
    echo "  ✓ Created data-$port"
done

# Generate configs if they don't exist
if [ ! -f "redis-cluster-configs/redis-7001.conf" ]; then
    echo "Configuration files not found!"
    echo "Generating them first..."
    ./generate-configs.sh
fi

# Start Redis instances
echo ""
echo "Starting Redis instances..."

PORTS=(7001 7002 7003 7004 7005 7006 7007 7008 7009)

for port in "${PORTS[@]}"; do
    CONFIG_FILE="redis-cluster-configs/redis-$port.conf"
    
    echo -n "Starting node on port $port... "
    
    # Check if already running
    if redis-cli -p $port ping 2>/dev/null | grep -q "PONG"; then
        echo "⚠️  Already running"
    else
        # Start Redis
        redis-server "$CONFIG_FILE" &
        sleep 1
        
        # Verify startup
        if redis-cli -p $port ping 2>/dev/null | grep -q "PONG"; then
            echo "✅ Started"
        else
            echo "❌ Failed to start"
        fi
    fi
done

echo ""
echo "========================================="
echo "All nodes started!"
echo ""
echo "To create the cluster, run:"
echo "  ./create-cluster.sh"
echo ""
echo "To check node status, run:"
echo "  ./check-cluster.sh"
echo ""
echo "Master nodes: 7001, 7002, 7003"
echo "Replica nodes: 7004-7009"
echo "========================================="
