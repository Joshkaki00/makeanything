# AWS EC2 Basics

## What is EC2

Amazon EC2 (Elastic Compute Cloud) is a web service that provides secure, resizable compute capacity in the cloud. EC2 allows you to launch virtual servers (called instances) on demand, configure security and networking, and manage storage. You pay only for the compute capacity you use.

EC2 is ideal for:
- Hosting web applications and APIs
- Running batch processing jobs
- Hosting databases
- Running machine learning workloads
- Development and testing environments

## EC2 Instance Types

EC2 instances come in different types optimized for different use cases:

- **General Purpose (t3, m5)** — Balance of compute, memory, and networking. Good for most workloads
- **Compute Optimized (c5)** — High performance processors. Good for batch processing, web applications
- **Memory Optimized (r5)** — High memory. Good for databases, caches, in-memory databases
- **Storage Optimized (i3)** — High sequential I/O performance. Good for NoSQL, data warehousing
- **GPU Instances (p3)** — Graphics processors. Good for machine learning, video processing

For beginners, **t3.micro** is often sufficient and eligible for the AWS free tier.

## Launching an EC2 Instance

To launch an EC2 instance:

1. Go to the AWS Console and navigate to EC2
2. Click "Launch Instances"
3. Select an Amazon Machine Image (AMI) — Ubuntu 22.04 LTS is a popular choice for beginners
4. Choose an instance type (t3.micro for free tier eligibility)
5. Configure instance details (VPC, subnet, auto-assign public IP)
6. Add storage (default 8-30 GB is fine for most applications)
7. Add tags to identify your instance
8. Configure security group (firewall rules)
9. Review and launch
10. Create or select a key pair for SSH access

## Security Groups

A security group acts as a virtual firewall for your EC2 instance. It controls inbound and outbound traffic:

Common inbound rules:
- SSH (port 22) — For remote command execution
- HTTP (port 80) — For web traffic
- HTTPS (port 443) — For encrypted web traffic
- Custom ports — For application servers

When you create a new security group, all inbound traffic is denied by default. You must explicitly allow ports.

## Connecting to Your Instance

After launching, you can connect via SSH:

```bash
ssh -i /path/to/key.pem ubuntu@your-instance-public-ip
```

Or using the instance ID:
```bash
aws ec2-instance-connect send-ssh-public-key \
  --instance-id i-1234567890abcdef0 \
  --os-user ubuntu \
  --ssh-public-key file://my-key.pub \
  --region us-east-1
```

## Elastic IP Addresses

By default, EC2 instances have a public IP that changes when the instance stops. To keep a static IP, use an Elastic IP:

1. Allocate an Elastic IP in the AWS Console
2. Associate it with your running instance
3. Now the IP persists even if you stop/start the instance

## Elastic Block Store (EBS)

EBS provides persistent block-level storage volumes for EC2 instances:

- **Volume types**:
  - `gp3` (General Purpose) — Good for most workloads
  - `io1` (Provisioned IOPS) — High I/O performance
  - `st1` (Throughput Optimized) — Sequential reads/writes

- **Snapshots** — Point-in-time backups of your volumes. Can be used to create new volumes or AMIs

Create a snapshot:
```bash
aws ec2 create-snapshot --volume-id vol-1234567890abcdef0 --description "Backup"
```

## Monitoring Your Instance

Monitor CPU, network, and disk usage:

```bash
# View instance metrics in CloudWatch
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --statistics Average \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600
```

## Cost Optimization

- **Use t3 instances** for variable workloads (burst-capable, cheaper)
- **Stop instances** when not in use (you pay for storage but not compute)
- **Use AWS Free Tier** for t2.micro instances (up to 750 hours/month, 1 year)
- **Monitor with CloudWatch** to catch runaway costs
- **Use Reserved Instances** for steady-state workloads (up to 72% discount)
- **Spot Instances** for fault-tolerant workloads (up to 90% discount, but can be interrupted)

## Terminating an Instance

When you're done with an instance:

```bash
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

Or through the AWS Console. Terminating permanently deletes the instance and its data (unless you created snapshots).

## Auto Scaling

For production workloads, use Auto Scaling Groups to automatically launch/terminate instances based on demand:

1. Create a Launch Template with your desired instance configuration
2. Create an Auto Scaling Group with min/max instance counts
3. Define scaling policies (scale up when CPU > 80%, scale down when CPU < 20%)
4. Attach a load balancer to distribute traffic

This ensures your application can handle traffic spikes without manual intervention.
