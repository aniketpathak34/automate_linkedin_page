from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
import os
import requests
from requests_oauthlib import OAuth2Session
from typing import Optional
import logging
import base64
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# LinkedIn OAuth2 configuration
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
LINKEDIN_REDIRECT_URI = "http://localhost:8000/callback"
LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
LINKEDIN_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
LINKEDIN_SCOPE = ["w_member_social", "openid", "profile", "email"]  # Updated scopes

# Store the OAuth2 session
oauth = OAuth2Session(
    LINKEDIN_CLIENT_ID,
    redirect_uri=LINKEDIN_REDIRECT_URI,
    scope=LINKEDIN_SCOPE
)

@app.get("/")
async def root():
    return {"message": "LinkedIn Automation API"}

@app.get("/auth")
async def auth():
    """Redirect to LinkedIn authorization page"""
    authorization_url, _ = oauth.authorization_url(LINKEDIN_AUTH_URL)
    logger.info(f"Generated authorization URL: {authorization_url}")
    return {"authorization_url": authorization_url}

@app.get("/callback")
async def callback(code: str):
    """Handle LinkedIn OAuth2 callback"""
    try:
        token = oauth.fetch_token(
            LINKEDIN_TOKEN_URL,
            client_secret=LINKEDIN_CLIENT_SECRET,
            code=code,
            include_client_id=True
        )
        return {"message": "Authentication successful", "token": token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/post")
async def create_post(
    text: str = Query(..., description="The text content of the post"),
    token: str = Query(..., description="LinkedIn access token")
):
    """Create a LinkedIn post"""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        # First, get the member ID from userinfo endpoint
        userinfo_response = requests.get(
            "https://api.linkedin.com/v2/userinfo",
            headers=headers
        )
        
        if userinfo_response.status_code != 200:
            print(userinfo_response.json(), "--------------------------------userinfo response")
            raise HTTPException(status_code=userinfo_response.status_code, detail="Failed to get member ID")
            
        member_id = userinfo_response.json().get('sub')
        if not member_id:
            raise HTTPException(status_code=400, detail="Could not get member ID")
            
        # Create the post with the correct author URN
        post_data = {
            "author": f"urn:li:person:{member_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        # Create the post
        response = requests.post(
            "https://api.linkedin.com/v2/ugcPosts",
            headers=headers,
            json=post_data
        )
        
        print("Post creation response:", response.json(), "--------------------------------response")
        
        if response.status_code == 201:
            post_id = response.json().get('id')
            if not post_id:
                raise HTTPException(status_code=500, detail="Post created but no ID returned")
                
            # Verify the post was created
            verify_response = requests.get(
                f"https://api.linkedin.com/v2/ugcPosts/{post_id}",
                headers=headers
            )
            
            print("Post verification response:", verify_response.json(), "--------------------------------verify response")
            
            if verify_response.status_code == 200:
                return {
                    "message": "Post created and verified successfully",
                    "post_id": post_id,
                    "post_url": f"https://www.linkedin.com/feed/update/{post_id}"
                }
            else:
                return {
                    "message": "Post created but verification failed",
                    "post_id": post_id,
                    "verification_error": verify_response.text
                }
        else:
            error_detail = response.text
            raise HTTPException(status_code=response.status_code, detail=error_detail)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 