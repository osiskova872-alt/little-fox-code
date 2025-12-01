#!/bin/bash
# Create Redis Cluster from 9 Nodes

echo "🔄 Creating Redis Cluster..."
echo "========================================="

# Check if nodes are running
echo "Checking if all nodes are running..."
ALL_RUNNING=true

for port in {7001..7009}; do
    if ! redis-cli -p $port ping 2>/dev/null | grep -q "PONG"; then
        echo "❌ Node $port is not running"
        ALL_RUNNING=false
    fi
done

if [ "$ALL_RUNNING" = false ]; then
    echo ""
    echo "⚠️  Some nodes are not running."
    echo "Please start all nodes first:"
    echo "  ./start-cluster.sh"
    exit 1
fi

echo "✅ All 9 nodes are running"
echo ""

# Create the cluster
echo "Creating cluster with 3 masters and 6 replicas..."
echo "(This may take a moment)"
echo ""

# Build node list
NODES=""
for port in {7001..7009}; do
    NODES="$NODES 127.0.0.1:$port"
done

# Execute cluster create command
echo "Executing: redis-cli --cluster create $NODES --cluster-replicas 2"
echo ""
echo "When prompted, type 'yes' to accept the configuration"
echo ""

redis-cli --cluster create $NODES --cluster-replicas 2

echo ""
echo "⏳ Waiting for cluster to stabilize..."
sleep 5

echo ""
echo "========================================="
echo "Cluster creation complete!"
echo ""
echo "To verify the cluster, run:"
echo "  ./check-cluster.sh"
echo ""
echo "Or manually check with:"
echo "  redis-cli -c -p 7001 cluster nodes"
echo "  redis-cli -c -p 7001 cluster info"
echo "========================================="
