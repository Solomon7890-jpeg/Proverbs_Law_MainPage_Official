# Deployment Guide: Cloudflare + Docker

This guide explains how to deploy the **ProVerBs Legal AI** application using a zero-cost strategy with Cloudflare Tunnels.

## 1. Cloudflare Zero Trust Setup (Free)

To expose your application to the internet without opening ports on your router or server:

1.  Log in to the [Cloudflare Dashboard](https://dash.cloudflare.com/).
2.  Go to **Zero Trust** -> **Networks** -> **Tunnels**.
3.  Click **Create a tunnel**.
4.  Choose **Cloudflared** as the connector.
5.  Give it a name (e.g., `proverbs-legal-ai`).
6.  In the **Install and run a connector** step:
    *   Choose **Docker**.
    *   Copy the **Token** (found at the end of the provided `docker run` command).
7.  Add a **Public Hostname**:
    *   Hostname: `ai` (or any subdomain)
    *   Domain: `yourdomain.com`
    *   Service: Type: `HTTP`, URL: `app:7860` (This matches the Docker service name and port).
8.  Save the tunnel.

## 2. Local Environment Setup

1.  Rename `.env.template` to `.env`:
    ```bash
    cp .env.template .env
    ```
2.  Paste your **Cloudflare Tunnel Token** into the `CLOUDFLARE_TUNNEL_TOKEN` field in `.env`.
3.  Add any necessary AI API keys.

## 3. Deployment

Run the following command to build and start the containers in the background:

```bash
docker-compose up -d --build
```

### Useful Commands:
- **Check logs**: `docker-compose logs -f app`
- **Check tunnel status**: `docker-compose logs -f tunnel`
- **Stop everything**: `docker-compose down`

## 4. Verification

1.  Wait about 30 seconds for the containers to initialize.
2.  Visit `https://ai.yourdomain.com` (or the subdomain you configured).
3.  The app should load securely with an SSL certificate provided automatically by Cloudflare.

---

## 5. Oracle Cloud Deployment (Always Free)

### Overview
Oracle Cloud's Always Free tier includes:
- **Ampere A1 Compute**: 4 vCPUs, 24 GB RAM (always free)
- **Flexible networking** with public IP
- **100 GB storage** (volume + object storage)
- No credit card required after free credits expire

### Step 1: Create Oracle Cloud Account

1. Go to [oracle.com/cloud/free](https://www.oracle.com/cloud/free/)
2. Click **Start for free**
3. Sign up with email and create account
4. Choose **Always Free** tier (no credit card required after trial)
5. Select region closest to you (e.g., `us-phoenix-1`, `us-ashburn-1`)

### Step 2: Create an Always Free Ampere Instance

1. In Oracle Cloud Console, go to **Compute** → **Instances**
2. Click **Create instance**
3. Configure:
   - **Name**: `proverbs-legal-ai`
   - **Image**: Ubuntu 24.04 LTS (Canonical)
   - **Shape**: **Ampere** (ARM-based, Always Free eligible)
   - **vCPUs**: 4
   - **Memory**: 24 GB
   - **Boot volume**: 50 GB
4. **Add SSH Key**:
   - Click **Generate a key pair**
   - Download the `.key` file (save securely)
   - Copy public key to clipboard
5. Click **Create instance**
6. Wait 2–3 minutes for instance to start
7. Note the **Public IP** address

### Step 3: Connect via SSH

From your local machine:
```bash
# Adjust path to your downloaded .key file
ssh -i path/to/your-instance.key ubuntu@<PUBLIC_IP>
```

If you get `bad permissions` error:
```bash
chmod 600 path/to/your-instance.key
```

### Step 4: Install Docker & Docker Compose

On the Oracle Cloud instance:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io docker-compose

# Add ubuntu user to docker group (no sudo needed)
sudo usermod -aG docker ubuntu

# Verify
docker --version
docker-compose --version

# Exit and reconnect to apply group changes
exit
# Then SSH back in
```

### Step 5: Clone Repository & Deploy

```bash
# Clone the repo
git clone https://github.com/your-username/proverbs-law.git
cd proverbs-law/Proverbs_Law_MainPage_Official

# Create .env file from template
cp .env.template .env

# Edit .env with your API keys (vi, nano, or your preferred editor)
nano .env
# Add: HUGGINGFACE_TOKEN, OPENAI_API_KEY, etc.

# Build and start containers
docker-compose up -d --build

# View logs
docker-compose logs -f app

# Stop if needed
docker-compose down
```

### Step 6: Access Your App

1. **Direct IP**: `http://<PUBLIC_IP>:7860`
2. **Firewall rules**: By default, port 7860 should be open
   - If blocked, go to **Compute** → **Instances** → **Instance Details** → **Virtual Cloud Network (VCN)** → **Security Lists** → Add **Ingress Rule**:
     - **Source CIDR**: `0.0.0.0/0`
     - **Destination Port Range**: `7860`
     - **Protocol**: TCP

### Step 7: Optional - Set Up Custom Domain (Cloudflare + Git)

If you own a domain, use **Cloudflare** to add HTTPS and route to your Oracle instance:

1. In Cloudflare DNS, add an **A record**:
   - **Name**: `ai` (or your subdomain)
   - **IPv4 address**: `<PUBLIC_IP>`
   - **Proxied**: Yes (orange cloud)
2. Access via `https://ai.yourdomain.com`

### Step 8: Automated Restart on Reboot

Ensure Docker containers start automatically:
```bash
# Enable Docker service on startup
sudo systemctl enable docker

# Add restart policy to containers (already in docker-compose.yml)
# Verify in docker-compose.yml:
# services:
#   app:
#     restart: always
```

### Step 9: Monitor & Maintain

**Check logs**:
```bash
docker-compose logs -f app
```

**Restart containers**:
```bash
docker-compose restart
```

**Update from Git**:
```bash
git pull origin main
docker-compose up -d --build
```

**Stop & cleanup**:
```bash
docker-compose down -v  # -v removes volumes
```

### Cost & Limits
- ✅ **Always Free**: 4 vCPU + 24 GB RAM + 50 GB storage
- ⚠️ **Outbound bandwidth**: 10 TB/month free per instance
- ⚠️ **Inbound**: Unlimited
- 📊 Monitor usage in **Billing** → **Usage** dashboard

### Troubleshooting

**Port not accessible**:
```bash
# Check if port 7860 is listening
sudo netstat -tlnp | grep 7860
# or
sudo ss -tlnp | grep 7860
```

**Out of disk space**:
```bash
df -h
docker system prune -a  # Remove unused images/containers
```

**Can't connect via SSH**:
- Verify instance is running (console shows green status)
- Check security group allows port 22 (should be default)
- Ensure you're using correct `.key` file and IP

---
> [!TIP]
> **Free Hosting Recommendation**: Oracle Cloud's Always Free tier gives you **4 vCPUs, 24 GB RAM, and 50 GB storage permanently free**—perfect for this Docker app. Use Git to clone & deploy; stop/start the instance anytime at no cost.
