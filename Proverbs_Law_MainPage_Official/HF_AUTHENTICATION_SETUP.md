# ⚖️ ProVerBs Legal AI - HuggingFace Authentication Setup Guide

## 🔐 Why HuggingFace Authentication is Required

The ProVerBs Legal AI platform uses HuggingFace's Inference API to power the AI legal assistant. Authentication ensures:

- **Personalized experience** with your account
- **Rate limiting protection** for all users- **Secure access** to premium AI models (Llama 3.3 70B Instruct)
- **Responsible AI usage** tracking

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Create a HuggingFace Account
If you don't have one:
1. Go to https://huggingface.co/join
2. Sign up with email or GitHub/Google
3. Verify your email address

### Step 2: Generate an API Token
1. Log in to HuggingFace: https://huggingface.co/
2. Click your **profile icon** (top right) → **Settings**
3. Select **Access Tokens** from the left menu
4. Click **New token**
5. Configure:
   - **Name**: `ProVerBs Legal AI`
   - **Type**: Select `read`
   - **Description**: `Access for ProVerBs legal chatbot`
6. Click **Create** and copy the token

### Step 3: Login to ProVerBs
1. Open the ProVerBs Legal AI application
2. Click the **"Sign in with Hugging Face"** button (top of page)
3. You'll be redirected to HuggingFace login
4. Grant permission when prompted
5. You'll be redirected back to the app
6. ✅ You're authenticated! Start asking legal questions

---

## ❌ Troubleshooting

### "Please log in with your Hugging Face account"
**Problem**: You haven't logged in yet

**Solution**:
1. Click the "Sign in with Hugging Face" button at the top
2. Complete the login process
3. Refresh the page if needed
4. Try your question again

### "Authentication token not found"
**Problem**: Login session expired

**Solution**:
1. Refresh the page
2. Click "Sign in" again
3. Make sure to grant permissions when prompted

### "You must provide an api_key"
**Problem**: Old error message from previous versions (now fixed!)

**Solution**:
- This error no longer occurs in updated versions
- Make sure you're on the latest version
- Login with HuggingFace as described above

### "Invalid token" or "Expired token"
**Problem**: Your HuggingFace token is invalid or expired

**Solution**:
1. Generate a new token:
   - Go to https://huggingface.co/settings/tokens
   - Delete the old token if still listed
   - Click "New token"
   - Create with "read" permission
2. Re-login to ProVerBs with your HuggingFace account

### "Network connection error"
**Problem**: Can't reach HuggingFace servers

**Solution**:
- Check your internet connection
- Try refreshing the page
- Wait a moment and try again
- HuggingFace might be temporarily down

---

## 🎯 What Each Mode Requires

All modes require HuggingFace authentication:

| Mode | Purpose | Requirements |
|------|---------|--------------|
| **Navigation Guide** | Find features in the app | HF Login ✅ |
| **General Legal Assistant** | Broad legal questions | HF Login ✅ |
| **Document Validator** | Analyze documents | HF Login ✅ |
| **Legal Research** | Find case law & statutes | HF Login ✅ |
| **Etymology Expert** | Explain legal terms | HF Login ✅ |
| **Case Management** | Organize case info | HF Login ✅ |
| **Regulatory Updates** | Track legal changes | HF Login ✅ |

---

## 🔒 Security & Privacy

### Your Data is Safe
- We only store your session token (not your password)
- All communication is encrypted (HTTPS)
- We don't share your data with third parties
- HuggingFace handles your account security

### Token Permissions
- We request only **"read" permission**
- This allows us to use the Inference API
- We cannot modify your account or models
- You can revoke access anytime

### Revoking Access
To remove ProVerBs access anytime:
1. Go to https://huggingface.co/settings/tokens
2. Find the `ProVerBs Legal AI` token
3. Click the delete button (trash icon)
4. Done! Access is immediately revoked

---

## 📱 Using Different Devices

### Mobile Devices
1. Open the ProVerBs app on your mobile browser
2. Click "Sign in with Hugging Face"
3. Complete login on mobile
4. Grant permissions
5. Use the app normally

### Switching Devices
- Your login session is device-specific
- You need to login separately on each device
- Each session lasts 24 hours
- Re-login automatically when expired

### Desktop Applications
- If using locally: follow "Running Locally" instructions
- Set HF_TOKEN environment variable:
  ```bash
  # Windows PowerShell
  $env:HF_TOKEN = "your_token_here"
  


  # Linux/Mac Bash


  
  export HF_TOKEN="your_token_here"
  ```

---

## 🛠️ Technical Details

### What We Access
We access the **HuggingFace Inference API**:
- Model: `meta-llama/Llama-3.3-70B-Instruct`
- Endpoint: `https://api-inference.huggingface.co/`
- Rate limits apply based on your HF account

### Rate Limits
- **Free accounts**: Limited requests per day
- **Pro accounts**: Higher limits
- Upgrade on HuggingFace if you hit limits

### Streaming Responses
- Responses stream in real-time
- You see the answer as it's generated
- Faster perceived performance
- Better user experience

---

## ❓ Common Questions

**Q: Do I need a paid HuggingFace account?**
A: No! The free account works fine. You might hit rate limits if you use it very heavily, but for normal use it's fine.

**Q: Is my data shared with HuggingFace?**
A: Yes, your legal questions go to HuggingFace's servers for the AI to process. All data is handled securely and deleted after processing. Don't ask about sensitive personal information.

**Q: Can I use ProVerBs offline?**
A: No, it requires HuggingFace's API which is cloud-based. You need an internet connection.

**Q: How long are sessions valid?**
A: Sessions last 24 hours. You'll need to re-login after that.

**Q: Can I share my account with others?**
A: Yes, but they'll need their own HuggingFace account. Don't share your API token directly.

**Q: What if I forget my HF password?**
A: Use the "Forgot password?" link on https://huggingface.co/login

---

## 📞 Need Help?

### Resources
- **HuggingFace Docs**: https://huggingface.co/docs
- **HuggingFace Support**: https://huggingface.co/support
- **ProVerBs Issues**: See the GitHub repository

### Check Your HF Account
1. Log in at https://huggingface.co/
2. Go to Settings → Access Tokens
3. Verify you have an active token
4. Check token hasn't been revoked

---

## ✅ Verification Checklist

- [ ] HuggingFace account created
- [ ] API token generated with "read" permission
- [ ] Token copied and saved somewhere safe
- [ ] Logged in to ProVerBs via "Sign in" button
- [ ] See "Welcome" or "AI Legal Chatbot" tab without login prompt
- [ ] Can submit a test question successfully

**Done! You're all set! 🎉**

---

**Last Updated**: December 2025  
**Version**: 1.0  
⚖️ Made with ❤️ for legal professionals worldwide
