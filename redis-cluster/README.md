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
Cluster Architecture
3 Master nodes (ports: 7001-7003)

6 Replica nodes (ports: 7004-7009)

2 Replicas per master

Total: 9 nodes

Port Mapping
Master 1: 7001 → Replicas: 7004, 7005

Master 2: 7002 → Replicas: 7006, 7007

Master 3: 7003 → Replicas: 7008, 7009

