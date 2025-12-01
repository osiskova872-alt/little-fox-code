# Redis Cluster Configuration Files

This directory contains scripts and configuration files for deploying a 9-node Redis Cluster.

## File Structure

### Configuration Generation
- `generate-configs.sh` - Generates Redis config files for 9 nodes

### Cluster Management
- `start-cluster.sh` - Starts all 9 Redis instances
- `create-cluster.sh` - Creates the Redis cluster
- `check-cluster.sh` - Checks cluster status
- `stop-cluster.sh` - Stops all Redis instances

### Templates
- `redis-base.conf` - Base Redis configuration template

## Quick Start

```bash
# 1. Make scripts executable
chmod +x *.sh

# 2. Generate configuration files
./generate-configs.sh

# 3. Start Redis instances
./start-cluster.sh

# 4. Create the cluster
./create-cluster.sh

# 5. Verify cluster status
./check-cluster.sh


\
Cluster Architecture
3 Master nodes (ports: 7001-7003)

6 Replica nodes (ports: 7004-7009)

2 Replicas per master

Total: 9 nodes

Port Mapping
Master 1: 7001 → Replicas: 7004, 7005

Master 2: 7002 → Replicas: 7006, 7007

Master 3: 7003 → Replicas: 7008, 7009


---

## 🎯 **ШАГ 2: СОЗДАДИМ СКРИПТЫ В ПАПКЕ `redis-cluster`**

### 📄 **Файл 1: `generate-configs.sh`**
**Нажмите:** `Add file` → `Create new file`
**Имя файла:** `redis-cluster/generate-configs.sh`
**Содержимое:**
```bash
#!/bin/bash
# Redis Cluster Configuration Generator for 9 Nodes

echo "========================================="
echo "Redis Cluster Configuration Generator"
echo "Creating configs for 9 nodes (3 masters + 6 replicas)"
echo "========================================="
echo ""

# Create directory if it doesn't exist
mkdir -p redis-cluster-configs

# Port configuration
MASTER_PORTS=(7001 7002 7003)
REPLICA_PORTS=(7004 7005 7006 7007 7008 7009)

# Master to replica mapping
# Replica 7004-7005 → Master 7001
# Replica 7006-7007 → Master 7002  
# Replica 7008-7009 → Master 7003

echo "Generating configuration files..."
echo ""

# Function to create config file
create_config() {
    local port=$1
    local role=$2
    local master_of_replica=$3
    
    local config_file="redis-cluster-configs/redis-$port.conf"
    
    echo "Creating: $config_file (Role: $role)"
    
    cat > "$config_file" << EOF
# Redis Cluster Configuration
# Node: $role
# Port: $port

port $port
cluster-enabled yes
cluster-config-file nodes-$port.conf
cluster-node-timeout 5000
appendonly yes
daemonize no
protected-mode no
bind 0.0.0.0
dir ./data-$port
logfile "redis-$port.log"
pidfile /var/run/redis_$port.pid

# Performance settings
maxmemory 512mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000

# Authentication (uncomment if needed)
# requirepass RedisCluster2024
# masterauth RedisCluster2024

# Replica configuration
EOF
    
    if [ "$role" = "replica" ] && [ -n "$master_of_replica" ]; then
        echo "replicaof 127.0.0.1 $master_of_replica" >> "$config_file"
    fi
    
    echo "  ✓ Created successfully"
    echo ""
}

# Create master configurations
echo "=== MASTER NODES ==="
for port in "${MASTER_PORTS[@]}"; do
    create_config "$port" "master"
done

# Create replica configurations
echo "=== REPLICA NODES ==="
# Replicas for master 7001
create_config 7004 "replica" 7001
create_config 7005 "replica" 7001

# Replicas for master 7002  
create_config 7006 "replica" 7002
create_config 7007 "replica" 7002

# Replicas for master 7003
create_config 7008 "replica" 7003
create_config 7009 "replica" 7003

echo "========================================="
echo "SUMMARY"
echo "========================================="
echo "Total configurations created: 9"
echo ""
echo "Master nodes:"
echo "  - redis-7001.conf (Master 1)"
echo "  - redis-7002.conf (Master 2)"
echo "  - redis-7003.conf (Master 3)"
echo ""
echo "Replica nodes:"
echo "  - redis-7004.conf → Replica of Master 1"
echo "  - redis-7005.conf → Replica of Master 1"
echo "  - redis-7006.conf → Replica of Master 2"
echo "  - redis-7007.conf → Replica of Master 2"
echo "  - redis-7008.conf → Replica of Master 3"
echo "  - redis-7009.conf → Replica of Master 3"
echo ""
echo "Next steps:"
echo "1. Run: chmod +x redis-cluster-configs/*.sh"
echo "2. Run: ./start-cluster.sh"
echo "========================================="
