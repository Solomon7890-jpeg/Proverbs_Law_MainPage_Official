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
> [!TIP]
> **Free Hosting Recommendation**: If you aren't hosting locally, use **Oracle Cloud (Always Free)**. Their ARM-based Ampere instances give you 4 CPUs and 24 GB of RAM for free, which is more than enough to run multiple Docker containers!
