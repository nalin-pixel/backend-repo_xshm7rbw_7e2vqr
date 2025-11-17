import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Lead, Contact

app = FastAPI(title="Fledge API", description="Backend for Fledge marketing site")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utilities
class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if ObjectId.is_valid(str(v)):
            return str(v)
        raise ValueError("Invalid ObjectId")


@app.get("/")
def read_root():
    return {"message": "Fledge API running"}


@app.get("/test")
def test_database():
    """Connection check with DB context"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set",
        "database_name": "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:120]}"
    return response


# Public content endpoints (static for now)
class Service(BaseModel):
    title: str
    description: str
    outcome: str
    bullets: List[str]


@app.get("/content/services", response_model=List[Service])
def get_services():
    return [
        Service(
            title="Social Media Management",
            description="Always-on content, community, and channel ops across key platforms.",
            outcome="Consistent growth in reach, engagement, and brand affinity.",
            bullets=[
                "Editorial calendars",
                "Community management",
                "Platform strategy",
                "Monthly reporting",
            ],
        ),
        Service(
            title="Creative Production",
            description="Agile production for short-form, campaigns, and brand assets.",
            outcome="Best-in-class content shipped at the speed of culture.",
            bullets=["Short-form video", "Brand design", "Campaign toolkits", "UGC production"],
        ),
        Service(
            title="Influencer Marketing",
            description="Creator sourcing, contracting, and performance tracking.",
            outcome="High-impact creators aligned with brand and objectives.",
            bullets=["Creator mapping", "Contracts & usage", "Briefing & QA", "Performance dashboard"],
        ),
        Service(
            title="Paid Advertising (Meta, TikTok, Google, YouTube)",
            description="Full-funnel paid strategy and execution across major platforms.",
            outcome="Efficient CAC and measurable revenue growth.",
            bullets=["Account structure", "Creative testing", "Attribution & pixels", "Weekly optimizations"],
        ),
        Service(
            title="PR & Digital Press Features",
            description="Narratives that travel across media and culture.",
            outcome="Earned visibility and credibility with your audiences.",
            bullets=["Story angles", "Press outreach", "Thought leadership", "Press kits"],
        ),
        Service(
            title="Training & Coaching",
            description="Upskill internal teams with modern social and content practices.",
            outcome="Faster execution and higher content quality in-house.",
            bullets=["Workshops", "Playbooks", "1:1 coaching", "Team audits"],
        ),
        Service(
            title="Strategy & Consulting",
            description="Brand, content, and growth strategy guided by research and data.",
            outcome="Clear direction and a prioritized roadmap to scale.",
            bullets=["Audience research", "Positioning", "Content architecture", "Measurement plan"],
        ),
    ]


# Lead capture endpoints
@app.post("/leads")
def submit_lead(lead: Lead):
    try:
        inserted_id = create_document("lead", lead)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/contact")
def submit_contact(contact: Contact):
    try:
        inserted_id = create_document("contact", contact)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
