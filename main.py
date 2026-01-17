from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from geofence import verify_geofence
from jose import jwt # This is for your digital keycard
from datetime import datetime, timedelta

app = FastAPI(title="Civic-Shield Security Gateway")
from fastapi.security import APIKeyHeader
oauth2_scheme = APIKeyHeader(name="Authorization")

SECRET_KEY = "TORONTO_SECRET_KEY" # Your private signing key

# --- DOOR 1: LOGIN (Get your Keycard) ---
@app.post("/login")
async def login(username: str):
    # This creates a digital keycard that lasts 30 minutes
    expire = datetime.utcnow() + timedelta(minutes=30)
    token = jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

# --- DOOR 2: PROTECTED TTC DATA ---
# This checks BOTH the Bouncer (Geofence) and your Keycard (JWT)
@app.get("/ttc-data", dependencies=[Depends(verify_geofence)])
async def get_ttc_data(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {
            "user": payload["sub"],
            "status": "Secure Access Granted",
            "data": "TTC Line 1 is operating normally."
        }
    except:
        raise HTTPException(status_code=401, detail="Invalid Keycard")