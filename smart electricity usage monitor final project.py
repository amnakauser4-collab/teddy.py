from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import uuid
from datetime import datetime

app = FastAPI(title="Smart Electricity Usage Monitor")

# ----------------------------------
# Fake Databases (In-Memory)
# ----------------------------------

users_db = {}          # username -> password
tokens_db = {}         # token -> username
usage_db = {}          # username -> list of dicts

TARIFF = (10, 15)

# ----------------------------------
# Models
# ----------------------------------

class AuthModel(BaseModel):
    username: str
    password: str


class UsageModel(BaseModel):
    units: float


# ----------------------------------
# Authentication Dependency
# ----------------------------------

def get_current_user(authorization: str = Header(...)):
    if authorization not in tokens_db:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return tokens_db[authorization]


# ----------------------------------
# Auth Routes
# ----------------------------------

@app.post("/signup")
def signup(data: AuthModel):
    if data.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    users_db[data.username] = data.password
    usage_db[data.username] = []

    return {"message": "Signup successful"}


@app.post("/login")
def login(data: AuthModel):
    if users_db.get(data.username) != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = str(uuid.uuid4())
    tokens_db[token] = data.username

    return {"token": token}


@app.post("/logout")
def logout(user: str = Depends(get_current_user), authorization: str = Header(...)):
    tokens_db.pop(authorization)
    return {"message": "Logged out successfully"}


# ----------------------------------
# Helper Functions
# ----------------------------------

def total_units(user):
    return sum(entry["units"] for entry in usage_db[user])


def calculate_bill(units):
    if units <= 100:
        return units * TARIFF[0]
    return (100 * TARIFF[0]) + ((units - 100) * TARIFF[1])


def usage_status(units):
    if units <= 100:
        return "Low"
    elif units <= 200:
        return "Medium"
    return "High ⚠️"


# ----------------------------------
# Electricity APIs (Protected)
# ----------------------------------

@app.post("/add-usage")
def add_usage(data: UsageModel, user: str = Depends(get_current_user)):
    if data.units <= 0:
        raise HTTPException(status_code=400, detail="Units must be positive")

    usage_db[user].append({
        "units": data.units,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    return {"message": "Usage added successfully"}


@app.get("/report")
def report(user: str = Depends(get_current_user)):
    if not usage_db[user]:
        return {"message": "No usage data available"}

    units = total_units(user)
    bill = calculate_bill(units)

    return {
        "user": user,
        "days_recorded": len(usage_db[user]),
        "total_units": units,
        "estimated_bill_rs": bill,
        "status": usage_status(units)
    }


@app.get("/history")
def usage_history(user: str = Depends(get_current_user)):
    return {"history": usage_db[user]}


@app.delete("/delete-last")
def delete_last_entry(user: str = Depends(get_current_user)):
    if not usage_db[user]:
        raise HTTPException(status_code=400, detail="No data to delete")

    removed = usage_db[user].pop()
    return {"deleted_entry": removed}


@app.delete("/reset-usage")
def reset_usage(user: str = Depends(get_current_user)):
    usage_db[user] = []
    return {"message": "All usage data reset"}


@app.get("/profile")
def profile(user: str = Depends(get_current_user)):
    return {
        "username": user,
        "total_entries": len(usage_db[user])
    }


@app.get("/")
def home():
    return {
        "project": "Smart Electricity Usage Monitor",
        "features": [
            "Signup / Login / Logout",
            "Token Authorization",
            "Usage Tracking",
            "Billing System",
            "Usage History",
            "Reset & Delete",
            "Fake Database"
        ]
    }

