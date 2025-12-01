#!/bin/bash
# Check Redis Cluster Status

echo "🔍 Redis Cluster Status Check"
echo "========================================="

# Check cluster info
echo "1. Cluster Information:"
echo "-----------------------"
redis-cli -c -p 7001 cluster info | grep -E "(cluster_state|cluster_slots|cluster_size|cluster_known_nodes)"
echo ""

# List all nodes
echo "2. Cluster Nodes:"
echo "-----------------"
redis-cli -c -p 7001 cluster nodes | head -15
echo ""

# Check slots distribution
echo "3. Slot Distribution:"
echo "---------------------"
redis-cli -c -p 7001 cluster slots | head -20
echo ""

# Test write/read
echo "4. Data Test:"
echo "-------------"
echo "Writing test data..."
redis-cli -c -p 7001 SET "test:cluster" "Redis Cluster is working!" > /dev/null
echo "Reading test data..."
redis-cli -c -p 7002 GET "test:cluster"
echo ""

# Check each node
echo "5. Individual Node Status:"
echo "--------------------------"
for port in {7001..7009}; do
    echo -n "Port $port: "
    if redis-cli -p $port ping 2>/dev/null | grep -q "PONG"; then
        # Get role
        ROLE=$(redis-cli -c -p $port cluster nodes 2>/dev/null | grep ":$port" | awk '{print $3}')
        if [ -n "$ROLE" ]; then
            echo "✅ $ROLE"
        else
            echo "✅ Running"
        fi
    else
        echo "❌ Not responding"
    fi
done

echo ""
echo "========================================="
echo "Check complete!"
echo "========================================="
