# Deployment Guide: ProVerBs Legal AI

---

# 🚀 PHASE 1: Create Cloudflare Account & Set Up Domain

**Time Required**: 15 minutes | **Cost**: Free

### Step 1a: Sign Up for Cloudflare

1. Go to https://cloudflare.com/
2. Click **Sign up**
3. Enter email & create password
4. Verify email
5. Choose **Free Plan**
6. You're in! ✅

### Step 1b: Add Your Domain to Cloudflare

If you **already own a domain** (GoDaddy, Namecheap, etc.):

1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Click **Add a site**
3. Enter your domain name (e.g., `yourdomain.com`)
4. Click **Continue**
5. Select **Free** plan
6. Cloudflare shows 2 **nameservers**:
   - `ns1.cloudflare.com`
   - `ns2.cloudflare.com`
7. Copy these nameservers
8. Go to your **domain registrar** (GoDaddy, Namecheap, etc.)
9. Find **DNS** or **Nameservers** settings
10. Replace old nameservers with Cloudflare's
11. Wait 24–48 hours for propagation (check status in Cloudflare dashboard)

**If you DON'T own a domain yet:**
- Buy one at: https://www.namecheap.com/ or https://www.godaddy.com/
- Then follow steps above to add to Cloudflare

### ✅ Phase 1 Checkpoint
- [ ] Cloudflare account created
- [ ] Domain added to Cloudflare
- [ ] Nameservers updated at registrar
- [ ] DNS propagating (or complete)

---

# 🚀 PHASE 2: Create Oracle Cloud Account & Launch Instance

**Time Required**: 20 minutes | **Cost**: $0 (Always Free)

### Step 2a: Create Oracle Cloud Account

1. Go to https://www.oracle.com/cloud/free/
2. Click **Start for free**
3. Fill out form:
   - Email
   - Country
   - Company (can be "Personal")
4. Click **Verify my email**
5. Check email, click verification link
6. Create Oracle Cloud password
7. Choose region closest to you (e.g., `us-phoenix-1`, `us-ashburn-1`)
8. Complete phone verification
9. **Select Always Free tier** (not trial)
10. Accept terms
11. Account created! ✅

### Step 2b: Launch Always Free Ampere Instance

1. Log in to [Oracle Cloud Console](https://cloud.oracle.com/)
2. Click **Compute** → **Instances**
3. Click **Create instance**

**Configure the instance:**

| Setting | Value |
|---------|-------|
| Name | `proverbs-legal-ai` |
| Region | Your chosen region (Phoenix/Ashburn) |
| **Image** | Ubuntu 24.04 LTS (Canonical) |
| **Shape** | Ampere (ARM-based) ⭐ |
| vCPUs | 4 |
| Memory | 24 GB |
| Boot Volume | 50 GB |

4. Scroll to **SSH Key**
5. Click **Generate a key pair**
6. Download `.key` file (save somewhere safe like `Documents/oracle-key.key`)
7. Copy public key to clipboard
8. Click **Create instance**
9. Wait 2–3 minutes for instance to start
10. Copy the **Public IP address** (e.g., `123.45.67.89`)

### ✅ Phase 2 Checkpoint
- [ ] Oracle Cloud account created
- [ ] Ampere instance launched
- [ ] SSH key downloaded (keep safe!)
- [ ] Public IP noted: `________________`

---

# 🚀 PHASE 3: Prepare .env File & API Keys

**Time Required**: 10 minutes | **Cost**: Depends on API keys

### Step 3a: Gather Your API Keys

You'll need tokens from these services. Get them now:

**HuggingFace Token**
1. Go to https://huggingface.co/settings/tokens
2. Create **New token** → Type: **read** (or write if needed)
3. Copy the token (starts with `hf_`)

**OpenAI API Key**
1. Go to https://platform.openai.com/api-keys
2. Click **+ Create new secret key**
3. Copy the key (starts with `sk-`)
4. ⚠️ Save securely (never share!)

**Google Gemini API Key** (if using)
1. Go to https://aistudio.google.com/app/apikey
2. Click **Create API Key** → **Create API Key in new project**
3. Copy the key

### Step 3b: Create .env File Locally

On your **local machine** (Windows/Mac/Linux):

1. Open file explorer to your repo:
   ```
   Proverbs_Law_MainPage_Official/
   ```

2. Find `.env.template` file
3. **Make a copy** of it:
   ```bash
   cp .env.template .env
   ```
4. **Open `.env` in a text editor** (VS Code, Notepad++, etc.)
5. **Fill in your API keys:**
   ```bash
   # --- Cloudflare Configuration ---
   CLOUDFLARE_TUNNEL_TOKEN=<you'll get this later from Cloudflare>

   # --- AI Providers ---
   GEMINI_API_KEY=<your-gemini-key>
   OPENAI_API_KEY=<your-openai-key>
   HF_TOKEN=<your-huggingface-token>

   # --- Application Settings ---
   GRADIO_SERVER_NAME=0.0.0.0
   GRADIO_SERVER_PORT=7860
   ```

6. **Save the file**
7. ⚠️ **NEVER commit .env to Git!** (Already in `.gitignore`)

### ✅ Phase 3 Checkpoint
- [ ] HuggingFace token collected
- [ ] OpenAI API key collected
- [ ] Gemini API key collected (if using)
- [ ] `.env` file created locally with API keys
- [ ] `.env` file NOT committed to Git

---

# 🚀 PHASE 4: Test Docker Locally

**Time Required**: 10–15 minutes | **Cost**: Free

### Prerequisites
- Docker Desktop installed ([download here](https://www.docker.com/products/docker-desktop))
- Your `.env` file from Phase 3
- Your repo cloned locally

### Step 4a: Build Docker Image

In your terminal/PowerShell:

```bash
# Navigate to repo
cd path/to/Proverbs_Law_MainPage_Official

# Build image (first time: 5–10 minutes)
docker build -t proverbs-legal-ai:latest .
```

✅ No errors? Continue!
❌ Error? Check Docker is running and all dependencies are installed.

### Step 4b: Run Container Locally

```bash
# Start container
docker run -p 7860:7860 \
  --env-file .env \
  proverbs-legal-ai:latest
```

**Watch for:**
- `INFO:     Uvicorn running on http://0.0.0.0:7860`
- No error messages

### Step 4c: Test the App

1. Open browser: http://localhost:7860
2. App should load ✅
3. Test a feature (chat, upload, etc.)
4. No errors? You're good!

### Step 4d: Stop Container

```bash
# Press Ctrl+C in terminal to stop
```

### ✅ Phase 4 Checkpoint
- [ ] Docker image built successfully
- [ ] Container ran without errors
- [ ] App accessible at localhost:7860
- [ ] Features working correctly

---

# 🚀 PHASE 5: Deploy to Oracle Cloud

**Time Required**: 20 minutes | **Cost**: $0

### Step 5a: Connect to Oracle Instance via SSH

**From your local machine**, open PowerShell/Terminal:

```bash
# Connect via SSH (replace IP with yours from Phase 2)
ssh -i path/to/oracle-key.key ubuntu@YOUR_ORACLE_PUBLIC_IP
```

**Example:**
```bash
ssh -i C:\Users\YourName\Documents\oracle-key.key ubuntu@123.45.67.89
```

**If you get permission error:**
```bash
# On Windows (PowerShell)
icacls C:\path\to\oracle-key.key /inheritance:r /grant:r "$env:username`:F"

# On Mac/Linux
chmod 600 /path/to/oracle-key.key
```

✅ You should see: `ubuntu@proverbs-legal-ai:~$`

### Step 5b: Install Docker on Oracle Instance

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io docker-compose

# Add ubuntu user to docker group (no sudo needed)
sudo usermod -aG docker ubuntu

# Verify installation
docker --version
docker-compose --version

# Exit and reconnect
exit
```

**Reconnect:**
```bash
ssh -i path/to/oracle-key.key ubuntu@YOUR_ORACLE_PUBLIC_IP
```

### Step 5c: Clone Repository on Oracle Instance

```bash
# Clone your repo
git clone https://github.com/your-username/proverbs-law.git

# Navigate to repo
cd proverbs-law/Proverbs_Law_MainPage_Official

# Verify files
ls -la
```

### Step 5d: Copy .env File to Oracle Instance

**Option 1: Use SCP** (from local machine):
```bash
scp -i path/to/oracle-key.key \
  path/to/local/.env \
  ubuntu@YOUR_ORACLE_PUBLIC_IP:~/proverbs-law/Proverbs_Law_MainPage_Official/.env
```

**Option 2: Create .env manually** (on Oracle instance):
```bash
# SSH into instance, then:
cd ~/proverbs-law/Proverbs_Law_MainPage_Official
cp .env.template .env
nano .env

# Paste your API keys
# Ctrl+X → Y → Enter to save
```

### Step 5e: Build & Deploy on Oracle Cloud

```bash
# Still on Oracle instance
docker-compose up -d --build

# Watch the build (takes 5–10 minutes)
docker-compose logs -f app

# Wait for: "Uvicorn running on http://0.0.0.0:7860"
# Then Ctrl+C to exit logs (container keeps running)
```

### Step 5f: Verify Deployment

```bash
# Check container status
docker ps

# You should see 2 containers: app + cloudflare-tunnel

# Check app logs
docker-compose logs app

# Test locally from Oracle instance
curl http://localhost:7860
```

✅ Getting HTML response? Deployment successful!

### ✅ Phase 5 Checkpoint
- [ ] SSH connection established
- [ ] Docker installed on Oracle instance
- [ ] Repository cloned
- [ ] `.env` file copied to instance
- [ ] Docker containers running (`docker ps` shows 2)
- [ ] App accessible at `<ORACLE_PUBLIC_IP>:7860`

---

# 🚀 PHASE 6: Connect Cloudflare Tunnel (Optional but Recommended)

**Time Required**: 5 minutes | **Cost**: Free

### If you want HTTPS + custom domain → Follow this phase

### Step 6a: Create Cloudflare Tunnel

1. Log in to [Cloudflare Zero Trust](https://one.dash.cloudflare.com/)
2. Click **Networks** → **Tunnels**
3. Click **Create a tunnel**
4. Choose **Cloudflared** as the connector
5. Name it: `proverbs-legal-ai`
6. Click **Save tunnel**

### Step 6b: Copy Tunnel Token

1. You see: **Install and run a connector**
2. Copy the full command (includes your token)
3. Extract just the TOKEN part (long string after `--token`)

### Step 6c: Update .env on Oracle Instance

```bash
# SSH into Oracle instance
ssh -i path/to/oracle-key.key ubuntu@YOUR_ORACLE_PUBLIC_IP

# Navigate to repo
cd ~/proverbs-law/Proverbs_Law_MainPage_Official

# Edit .env
nano .env

# Find this line:
# CLOUDFLARE_TUNNEL_TOKEN=your_token_here

# Replace with your actual token:
CLOUDFLARE_TUNNEL_TOKEN=eyJhbGciOiJSUzI1NiIsImtpZCI6I... (your token)

# Save: Ctrl+X → Y → Enter
```

### Step 6d: Restart Docker Containers

```bash
# Restart to apply new token
docker-compose restart

# Check tunnel is connected
docker-compose logs tunnel

# Look for: "Connected to Cloudflare!"
```

### Step 6e: Add Public Hostname in Cloudflare

1. Go to [Cloudflare Tunnels](https://one.dash.cloudflare.com/tunnels)
2. Click your tunnel name
3. Go to **Public Hostname** tab
4. Click **Add public hostname**
5. Fill in:
   - **Subdomain**: `ai` (or whatever you want)
   - **Domain**: `yourdomain.com` (must be added to Cloudflare)
   - **Service type**: `HTTP`
   - **Service URL**: `localhost:7860` (tunnel handles routing)
6. Click **Save hostname**

### Step 6f: Test Your Domain

1. Wait 1–2 minutes
2. Open browser: `https://ai.yourdomain.com`
3. App should load with 🔒 HTTPS ✅

### ✅ Phase 6 Checkpoint
- [ ] Cloudflare tunnel created
- [ ] Tunnel token added to `.env` on Oracle instance
- [ ] Public hostname configured in Cloudflare
- [ ] App accessible at `https://ai.yourdomain.com`
- [ ] HTTPS working (green lock icon)

---

## Choose your deployment strategy below.

---

## Quick Comparison

| Feature | Cloudflare Tunnel | Oracle Cloud |
|---------|-------------------|--------------|
| **Cost** | Free (HTTPS + CDN) | Always Free (4 vCPU, 24 GB RAM) |
| **Setup Time** | 10 minutes | 20 minutes |
| **Custom Domain** | ✅ Required | ✅ Optional |
| **Firewall Rules** | ❌ Not needed | ⚠️ May need SSH config |
| **Server Control** | Limited | Full root access |
| **Best For** | Quick deployment, custom domain | Persistent 24/7 hosting |
| **Local Machine** | ✅ Yes | ❌ No (needs VPS/Server) |
| **Auto SSL/HTTPS** | ✅ Yes | ❌ Need Cloudflare separately |

**TL;DR**:
- **Want to deploy from your local machine with HTTPS?** → Cloudflare Tunnel
- **Want always-free Linux server in the cloud?** → Oracle Cloud
- **Want both?** → Use Oracle Cloud + Cloudflare Tunnel (best combo!)

---

### Zero-Cost HTTPS Tunnel with Custom Domain

Perfect if you:
- Have a domain already
- Want HTTPS without opening ports on your router/firewall
- Can run Docker locally or on any Linux server
- Need zero-cost deployment with auto SSL

### Step 1: Set Up Cloudflare Account

1. Sign up at [cloudflare.com](https://cloudflare.com/) (free plan included)
2. Add your domain to Cloudflare (update nameservers at your registrar)
3. Wait 24–48 hours for DNS propagation (or use fast nameserver migration)

### Step 2: Create Cloudflare Tunnel

1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Go to **Zero Trust** → **Networks** → **Tunnels**
3. Click **Create a tunnel**
4. Choose **Cloudflared** as the connector
5. Name it (e.g., `proverbs-legal-ai`)
6. **Install and run** step:
   - Choose **Docker**
   - Copy the full command (it includes your unique **Token**)
7. **Add public hostname**:
   - Hostname: `ai` (or any subdomain)
   - Domain: `yourdomain.com`
   - Service type: `HTTP`
   - URL: `localhost:7860` (if running locally) or `<server-ip>:7860` (if on remote server)
8. Save the tunnel

### Step 3: Clone & Deploy with Git

**Option A1: Deploy Locally (Your Machine)**

```bash
# Clone repository
git clone https://github.com/your-username/proverbs-law.git
cd proverbs-law/Proverbs_Law_MainPage_Official

# Copy .env template
cp .env.template .env

# Edit .env with your API keys
nano .env
# Add: HUGGINGFACE_TOKEN, OPENAI_API_KEY, CLOUDFLARE_TUNNEL_TOKEN, etc.

# Start Docker containers
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop when done
docker-compose down
```

**Option A2: Deploy to Remote Server (VPS/Oracle Cloud)**

```bash
# SSH into your server
ssh user@server-ip

# Clone repository
git clone https://github.com/your-username/proverbs-law.git
cd proverbs-law/Proverbs_Law_MainPage_Official

# Copy .env template
cp .env.template .env

# Edit .env
nano .env

# Start Docker
docker-compose up -d --build

# Logs
docker-compose logs -f app
```

### Step 4: Access Your App

- **Local**: `https://ai.yourdomain.com` (via Cloudflare tunnel, no local IP needed)
- **Remote**: Same URL (Cloudflare routes to your server automatically)
- **Auto HTTPS**: Cloudflare provides free SSL certificate
- **No port forwarding**: No firewall rules needed

### Step 5: Update from Git

Deploy new versions without downtime:

```bash
# Pull latest code
git pull origin main

# Rebuild and restart containers
docker-compose up -d --build

# Check deployment
docker-compose logs -f app
```

### Step 6: Monitor & Logs

```bash
# View app logs
docker-compose logs -f app

# View all services
docker-compose logs -f

# View tunnel status (in Cloudflare dashboard under Tunnels)
# Check for "Connected" status
```

### Cloudflare Dashboard Monitoring

1. Go to **Zero Trust** → **Tunnels** → Your tunnel name
2. Check **Status**: Should show **Connected**
3. View **Analytics**: Bandwidth, requests, geo-location data
4. **DNS**: Configure additional subdomains anytime

### Cost & Benefits

✅ **Free**:
- Tunnel (unlimited)
- HTTPS/SSL certificate
- DDoS protection
- Global CDN
- Analytics dashboard

⚠️ **Limitations**:
- Free plan: Up to 5 million requests/month
- Rate limiting: 10 requests/second (free)
- **Upgrade to Pro/Business** if you need higher limits

---

## Option B: Oracle Cloud Deployment (Always Free)

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

---

## Option C: Oracle Cloud + Cloudflare Tunnel (Best Combo!)

### Maximum Performance + Always-Free Tier

Combine **Oracle Cloud** (persistent 24/7 server) with **Cloudflare** (HTTPS + CDN + Analytics):

1. Create Oracle Cloud Always Free instance (Section B, Steps 1–4)
2. Clone & deploy the app on Oracle Cloud (Section B, Step 5)
3. Use Cloudflare Tunnel to route your custom domain to Oracle Cloud

### Setup

**On your Oracle Cloud instance**:
```bash
# Clone repo
git clone https://github.com/your-username/proverbs-law.git
cd proverbs-law/Proverbs_Law_MainPage_Official

# Create .env
cp .env.template .env
nano .env

# Start Docker
docker-compose up -d --build
```

**On Cloudflare dashboard**:
1. Go to **Zero Trust** → **Tunnels** → **Create tunnel**
2. Choose **Cloudflared** → **Docker**
3. Copy the token
4. **Add public hostname**:
   - Hostname: `ai`
   - Domain: `yourdomain.com`
   - Service: `HTTP` → `<ORACLE_PUBLIC_IP>:7860`

**Result**:
- ✅ Always-free server (4 vCPU, 24 GB RAM)
- ✅ Auto HTTPS + SSL
- ✅ Global CDN caching
- ✅ DDoS protection
- ✅ Analytics dashboard
- ✅ Git-based deployment
- ✅ Zero port forwarding needed

**Update deployments**:
```bash
# SSH into Oracle instance
ssh -i key.pem ubuntu@<ORACLE_IP>

# Pull latest code & redeploy
cd proverbs-law/Proverbs_Law_MainPage_Official
git pull origin main
docker-compose up -d --build
docker-compose logs -f app
```

---

## Summary: Which Option for You?

| Your Situation | Best Option |
|---|---|
| I have a laptop/desktop & want to run 24/7 | **Cloudflare Tunnel** |
| I want always-free cloud server | **Oracle Cloud** |
| I want HTTPS + always-free cloud | **Oracle Cloud + Cloudflare** |
| I want easiest setup | **Cloudflare Tunnel** |
| I want most control & resources | **Oracle Cloud** |

---

## Next Steps

1. **Pick your option** (A, B, or C)
2. **Create accounts**: Cloudflare (free) and/or Oracle Cloud (always free)
3. **Clone this repo** with Git
4. **Copy `.env.template` → `.env`** and add your API keys
5. **Run `docker-compose up -d --build`** and visit your domain
6. **Update anytime** with `git pull && docker-compose up -d --build`

All options support **Git-based deployment** for easy updates! 🚀
