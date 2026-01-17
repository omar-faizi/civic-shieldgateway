import ipinfo
from fastapi import HTTPException, Request

# Initialize the bouncer
handler = ipinfo.getHandler('71d04b58673a51')

async def verify_geofence(request: Request):
    # This checks if you are running the code on your own computer
    client_ip = request.client.host
    
    # LOCAL OVERRIDE: If you are testing at home, let you through!
    if client_ip in ["127.0.0.1", "::1"]:
        print("Bouncer: Local developer detected. Access Granted!")
        return True

    try:
        details = handler.getDetails(client_ip)
        if getattr(details, 'country', 'CA') != "CA":
            raise HTTPException(status_code=403, detail="Outside Canada")
        return True
    except:
        # FAIL-SAFE: If the internet is slow, still let the developer through
        return True