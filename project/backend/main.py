from fastapi import FastAPI, HTTPException, Body, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import io
from bson.objectid import ObjectId
from models import UserCreate
from db import user_collection, file_collection
from email_utils import send_verification_email
from uuid import uuid4
from passlib.context import CryptContext

api_app = FastAPI()
password_handler = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Allow frontend to talk to backend without issues
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api_app.post("/register")
async def create_account(new_user: UserCreate):
    # See if this email's already taken
    existing_account = await user_collection.find_one({"email": new_user.email})
    if existing_account:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Make sure role is legit, either 'ops' or 'client'
    if new_user.role not in ["ops", "client"]:
        raise HTTPException(status_code=400, detail="Invalid role. Must be 'ops' or 'client'.")

    # Hash the password before saving
    secure_password = password_handler.hash(new_user.password)

    # Generate a verification code
    verification_code = str(uuid4())

    # Prepare data to store in DB
    new_user_info = {
        "email": new_user.email,
        "password": secure_password,
        "role": new_user.role,
        "is_verified": False,
        "verification_token": verification_code
    }
    await user_collection.insert_one(new_user_info)

    # Send out that verification email
    send_verification_email(new_user.email, verification_code)
    return {"message": "Check your email for a verification link"}

@api_app.get("/verify")
async def confirm_email(token: str):
    account = await user_collection.find_one({"verification_token": token})
    if not account:
        raise HTTPException(status_code=400, detail="Invalid token")

    await user_collection.update_one(
        {"_id": account["_id"]},
        {"$set": {"is_verified": True}, "$unset": {"verification_token": ""}}
    )
    return {"message": "Email verified successfully"}

@api_app.post("/login")
async def sign_in(email: str = Body(...), password: str = Body(...)):
    account = await user_collection.find_one({"email": email})
    if not account:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not account.get("is_verified"):
        raise HTTPException(status_code=403, detail="Please verify your email before logging in")

    if not password_handler.verify(password, account["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "role": account.get("role", "client")  # Default to client if no role
    }

# Helper to grab user info by email (passed in header or param)
async def fetch_current_user(email: str):
    account = await user_collection.find_one({"email": email})
    if not account or not account.get("is_verified"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return account

# Ensure user is ops
async def ops_only(user=Depends(fetch_current_user)):
    if user.get("role") != "ops":
        raise HTTPException(status_code=403, detail="Ops users only")
    return user

# Ensure user is client
async def client_only(user=Depends(fetch_current_user)):
    if user.get("role") != "client":
        raise HTTPException(status_code=403, detail="Client users only")
    return user

# Upload file (ops users only)
@api_app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    client_email: str = Body(...),
    user=Depends(ops_only),
):
    file_bytes = await file.read()
    file_record = {
        "filename": file.filename,
        "owner": client_email,
        "content": file_bytes,
    }
    await file_collection.insert_one(file_record)
    return {"message": f"File '{file.filename}' uploaded for client {client_email}"}

# List files (clients only)
@api_app.get("/files")
async def get_files(user=Depends(client_only)):
    user_files = await file_collection.find({"owner": user["email"]}).to_list(100)
    # Just send the filename and id for listing
    return [{"id": str(f["_id"]), "filename": f["filename"]} for f in user_files]

# Download a file (clients only)
@api_app.get("/files/download/{file_id}")
async def download_document(file_id: str, user=Depends(client_only)):
    file_doc = await file_collection.find_one({"_id": ObjectId(file_id), "owner": user["email"]})
    if not file_doc:
        raise HTTPException(status_code=404, detail="File not found")

    return StreamingResponse(
        io.BytesIO(file_doc["content"]),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file_doc['filename']}"},
    )
