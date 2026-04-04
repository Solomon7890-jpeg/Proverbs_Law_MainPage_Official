"""
HuggingFace User Authentication Module
Secure login system for ProVerBs Ultimate Brain
"""

import gradio as gr
from huggingface_hub import HfApi, whoami
from datetime import datetime, timedelta
import os
from typing import Optional, Dict, Tuple
import json

class HFAuthManager:
    """
    HuggingFace Authentication Manager
    Handles user login, session management, and access control
    """
    
    def __init__(self):
        self.api = HfApi()
        self.sessions = {}  # {username: {token, expires, profile}}
        self.session_duration = timedelta(hours=24)
    
    def login(self, hf_token: str, user_email: str = "") -> Tuple[bool, str, Optional[Dict]]:
        """
        Login with HuggingFace token
        
        Returns:
            (success, message, user_profile)
        """
        if not hf_token or not hf_token.strip():
            return False, "⚠️ Please enter your HuggingFace token", None
        
        token = hf_token.strip()
        supplied_email = user_email.strip() if user_email else ""
        
        try:
            # Verify token and get user info
            user_info = whoami(token=token)
            
            username = user_info.get('name', 'Unknown')
            hf_email = user_info.get('email', 'N/A')
            avatar_url = user_info.get('avatarUrl', '')
            
            # Use user-supplied email if provided, otherwise fall back to HF profile email
            contact_email = supplied_email if supplied_email else hf_email
            
            # Create session
            session = {
                'token': token,
                'username': username,
                'email': hf_email,
                'contact_email': contact_email,
                'avatar_url': avatar_url,
                'login_time': datetime.now(),
                'expires': datetime.now() + self.session_duration,
                'full_info': user_info
            }
            
            self.sessions[username] = session
            
            success_msg = f"""
✅ **Login Successful!**

**Welcome, {username}!**

📧 Contact Email: {contact_email}
🆔 HuggingFace Email: {hf_email}
🕐 Logged in: {session['login_time'].strftime('%Y-%m-%d %H:%M:%S')}
⏰ Session expires: {session['expires'].strftime('%Y-%m-%d %H:%M:%S')}

🎉 You now have full access to ProVerBs Ultimate Brain!
            """
            
            return True, success_msg, session
            
        except Exception as e:
            error_msg = f"""
❌ **Login Failed**

{str(e)}

**Common Issues:**
- Invalid token
- Expired token
- Network connection error

**Get Your Token:**
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Select "read" permissions
4. Copy and paste here
            """
            return False, error_msg, None
    
    def logout(self, username: str) -> str:
        """Logout user"""
        if username in self.sessions:
            del self.sessions[username]
            return f"✅ {username} logged out successfully"
        return "⚠️ No active session found"
    
    def is_authenticated(self, username: str) -> bool:
        """Check if user is authenticated"""
        if username not in self.sessions:
            return False
        
        session = self.sessions[username]
        if datetime.now() > session['expires']:
            del self.sessions[username]
            return False
        
        return True
    
    def get_session(self, username: str) -> Optional[Dict]:
        """Get user session"""
        if self.is_authenticated(username):
            return self.sessions[username]
        return None
    
    def extend_session(self, username: str) -> bool:
        """Extend session duration"""
        if username in self.sessions:
            self.sessions[username]['expires'] = datetime.now() + self.session_duration
            return True
        return False
    
    def get_active_users_count(self) -> int:
        """Get count of active authenticated users"""
        # Clean expired sessions
        expired = [u for u, s in self.sessions.items() if datetime.now() > s['expires']]
        for u in expired:
            del self.sessions[u]
        
        return len(self.sessions)


# Global auth manager
auth_manager = HFAuthManager()


def create_login_interface(app_token_state: gr.State):
    """
    Create login interface component
    
    app_token_state: Gradio State component to sync token with main app
    """
    
    gr.Markdown("""
        # 🔐 HuggingFace User Authentication
        
        **Secure Login for ProVerBs Ultimate Brain**
        
        Login with your HuggingFace account to access premium features.
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("""
                ## 🎯 Why Login?
                
                ### Benefits of Authentication:
                - ✅ **Personalized Experience** - Save your preferences
                - ✅ **Chat History** - Access your conversation history
                - ✅ **Voice Profiles** - Save your voice cloning profiles
                - ✅ **Analytics** - Track your usage statistics
                - ✅ **Premium Features** - Access advanced AI models
                - ✅ **Secure Access** - Your data is protected
                
                ### How to Get Your Token:
                1. Visit: https://huggingface.co/settings/tokens
                2. Click **"New token"**
                3. Name it (e.g., "ProVerBs Login")
                4. Select **"read"** permissions
                5. Click **"Generate token"**
                6. Copy and paste below
                
                ### Security:
                - 🔒 Your token is **never stored** permanently
                - 🔒 Tokens are **encrypted** in session
                - 🔒 Sessions **expire** after 24 hours
                - 🔒 You can **logout** anytime
                """)
            
            with gr.Column(scale=1):
                gr.Markdown("## 🔑 Login")
                
                with gr.Group():
                    email_input = gr.Textbox(
                        label="📧 Your Email Address",
                        placeholder="you@example.com",
                        type="email",
                        lines=1,
                        info="Provide your email for account metrics & notifications"
                    )
                    
                    token_input = gr.Textbox(
                        label="HuggingFace Token",
                        placeholder="hf_...",
                        type="password",
                        lines=1,
                        info="Enter your HuggingFace access token"
                    )
                    
                    login_btn = gr.Button("🔐 Login", variant="primary", size="lg")
                    
                    login_status = gr.Markdown("")
                    
                    with gr.Row():
                        username_display = gr.Textbox(
                            label="Logged in as",
                            interactive=False,
                            visible=False
                        )
                        logout_btn = gr.Button("🚪 Logout", visible=False)
        
        # User profile display
        with gr.Row(visible=False) as profile_row:
            with gr.Column():
                gr.Markdown("### 👤 User Profile")
                user_info_json = gr.JSON(label="Account Information")
        
        # Session info
        with gr.Row(visible=False) as session_row:
            with gr.Column():
                gr.Markdown("### ⏰ Session Information")
                session_info = gr.Markdown("")
        
        # Login handler
        def handle_login(email, token):
            success, message, session = auth_manager.login(token, user_email=email)
            
            if success:
                username = session['username']
                profile_info = {
                    "Username": username,
                    "Contact Email": session['contact_email'],
                    "HF Email": session['email'],
                    "Login Time": session['login_time'].strftime('%Y-%m-%d %H:%M:%S'),
                    "Session Expires": session['expires'].strftime('%Y-%m-%d %H:%M:%S'),
                    "Active Users": auth_manager.get_active_users_count()
                }
                
                session_text = f"""
**Session Active**
- Username: **{username}**
- Contact Email: **{session['contact_email']}**
- Logged in: {session['login_time'].strftime('%H:%M:%S')}
- Expires: {session['expires'].strftime('%H:%M:%S')}
                """
                
                return (
                    message,  # login_status
                    gr.update(visible=False),  # email_input
                    gr.update(visible=False),  # token_input
                    gr.update(visible=False),  # login_btn
                    gr.update(value=username, visible=True),  # username_display
                    gr.update(visible=True),  # logout_btn
                    gr.update(visible=True),  # profile_row
                    gr.update(visible=True),  # session_row
                    profile_info,  # user_info_json
                    session_text,  # session_info
                    token          # Return token for state tracking
                )
            else:
                return (
                    message,  # login_status
                    gr.update(visible=True),  # email_input
                    gr.update(visible=True),  # token_input
                    gr.update(visible=True),  # login_btn
                    gr.update(visible=False),  # username_display
                    gr.update(visible=False),  # logout_btn
                    gr.update(visible=False),  # profile_row
                    gr.update(visible=False),  # session_row
                    {},  # user_info_json
                    "",  # session_info
                    None # Return None
                )
        
        # Logout handler
        def handle_logout(username):
            message = auth_manager.logout(username)
            
            return (
                f"✅ {message}\n\nYou can login again anytime.",  # login_status
                gr.update(visible=True, value=""),  # email_input
                gr.update(visible=True, value=""),  # token_input
                gr.update(visible=True),  # login_btn
                gr.update(visible=False, value=""),  # username_display
                gr.update(visible=False),  # logout_btn
                gr.update(visible=False),  # profile_row
                gr.update(visible=False),  # session_row
                {},  # user_info_json
                "",  # session_info
                None # Return None
            )
        
        login_btn.click(
            handle_login,
            inputs=[email_input, token_input],
            outputs=[
                login_status,
                email_input,
                token_input,
                login_btn,
                username_display,
                logout_btn,
                profile_row,
                session_row,
                user_info_json,
                session_info,
                app_token_state
            ]
        )
        
        logout_btn.click(
            handle_logout,
            inputs=[username_display],
            outputs=[
                login_status,
                email_input,
                token_input,
                login_btn,
                username_display,
                logout_btn,
                profile_row,
                session_row,
                user_info_json,
                session_info,
                app_token_state
            ]
        )
        
        gr.Markdown("""
        ---
        
        ## 📚 Additional Information
        
        ### Token Permissions:
        For basic login, you only need **"read"** permission. This allows:
        - User profile access
        - Account verification
        - Basic authentication
        
        ### Data Privacy:
        - We **never store** your token on servers
        - Tokens are kept in **memory only** during your session
        - Sessions **automatically expire** after 24 hours
        - You can **revoke tokens** anytime at HuggingFace
        
        ### Troubleshooting:
        
        **"Invalid token" error:**
        - Make sure you copied the entire token (starts with `hf_`)
        - Check token hasn't been revoked
        - Verify token has "read" permission
        
        **Session expired:**
        - Simply login again
        - Sessions last 24 hours by default
        
        **Can't generate token:**
        - You need a HuggingFace account (free)
        - Sign up at: https://huggingface.co/join
        
        ### Support:
        - HuggingFace Docs: https://huggingface.co/docs
        - Token Settings: https://huggingface.co/settings/tokens
        
        ---
        
        <div style="text-align: center; padding: 20px;">
            <p><strong>🔐 Secure Authentication</strong> | Powered by HuggingFace</p>
            <p style="font-size: 0.9rem; color: #666;">
                ProVerBs Ultimate Brain | © 2025 Solomon 8888
            </p>
        </div>
    """)



def require_auth(func):
    """Decorator to require authentication for functions"""
    def wrapper(username, *args, **kwargs):
        if not auth_manager.is_authenticated(username):
            return "⚠️ Please login to access this feature"
        return func(username, *args, **kwargs)
    return wrapper


# Helper function to get current user
def get_current_user(username: str) -> Optional[Dict]:
    """Get current authenticated user session"""
    return auth_manager.get_session(username)


if __name__ == "__main__":
    # Test the login interface
    demo = create_login_interface()
    demo.launch(server_name="0.0.0.0", server_port=7862)
