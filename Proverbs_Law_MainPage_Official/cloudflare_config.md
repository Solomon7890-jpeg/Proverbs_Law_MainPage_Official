# Cloudflare "Pro Set Up" Configuration Guide

Fronting your **GCP Cloud Run** instance with **Cloudflare** ensures maximum speed for your 3D Hero brain and robust protection for your "Status-Aware" intelligence.

## 1. Domain Setup
1.  Log in to [Cloudflare](https://dash.cloudflare.com).
2.  Add your domain (e.g., `proverbslegal.ai`).
3.  Update your domain's nameservers at your registrar to point to Cloudflare.

## 2. DNS Configuration
Add a **CNAME** record to map your domain to your **Cloud Run** service:
- **Type**: CNAME
- **Name**: `@` (for root) or `www`
- **Target**: Paste your Cloud Run service URL (e.g., `proverbs-ultimate-brain-uxtfjsl.a.run.app`).
- **Proxy Status**: **Proxied (Orange Cloud)**.

## 3. SSL/TLS Settings
To ensure the highest level of privacy and performance:
*   Go to **SSL/TLS > Overview**.
*   Select **Full (Strict)**. This encrypts traffic between Cloudflare and Google Cloud.
*   Enable **Always Use HTTPS** in **SSL/TLS > Edge Certificates**.

## 4. Performance & WAF
*   **WAF (Security)**: Go to **Security > WAF** and enable Managed Rules to block common exploits.
*   **Caching (3D Speed)**: Go to **Caching > Configuration** and set **Browser Cache TTL** to 1 month (optimizes the Hero3D brain loading).
*   **Auto Minify**: Under **Speed > Optimization**, check **JavaScript, CSS, and HTML** to shrink your 3D assets.

## 5. Environment Readiness
Once your DNS has propagated (usually 5-10 minutes), your ProVerBs "Ultimate Brain" will be live on your professional domain with **Global Edge Security**.

> [!NOTE]
> If you encounter a "Direct IP Access" error from Cloud Run, ensure you have enabled **Custom Domain Mapping** in the GCP Console under Cloud Run > [Service] > Manage Custom Domains.
