import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = None


class ChatResponse(BaseModel):
    reply: str


PROFILE = {
    "name": "Meezab Momin",
    "title": "Full Stack & Application Developer",
    "tag": "Building immersive web experiences, powerful AI tools, and modern applications",
    "skills": {
        "frontend": [
            "React", "Next.js", "TailwindCSS", "TypeScript", "JavaScript", "HTML5", "CSS3", "Styled Components", "Sass", "Less", "CSS Modules"
        ],
        "backend": ["Node.js", "Express.js", "REST APIs", "SSR", "Full Stack Architecture"],
        "ai": [
            "ChatGPT", "Claude", "Deepseek", "Gemini", "Kimi", "Workik", "Cody", "Firebase Studio AI", "Cursor IDE", "Windsurf IDE", "Trae IDE", "Void IDE", "Google AI Studio", "Google Labs", "Stitch", "Lovable", "Builder.io", "OpenRouter", "Vercel-V0"
        ],
        "database": ["MongoDB", "Firebase", "Firestore", "LocalStorage"],
        "others": ["Git", "GitHub", "Vercel", "Netlify", "Postman", "Figma", "VS Code", "IntelliJ", "PWA", "Android Studio", "Unity", "Unreal Engine"]
    },
    "projects": [
        {
            "name": "UniToolBox",
            "period": "2024/2–2024/10",
            "highlights": [
                "Full-stack toolkit with 30+ free tools",
                "Next.js + React + TypeScript + Tailwind",
                "AI features (summarizer, translator)",
                "SSR for SEO",
                "Deployed on Vercel",
                "Privacy & accessibility focused",
                "Ad-supported monetization"
            ]
        },
        {
            "name": "Anonymous Messenger",
            "period": "2022/9–2023/6",
            "highlights": [
                "Android chat app",
                "Java + XML",
                "Firebase Realtime DB",
                "Live messaging",
                "Clean responsive UI"
            ]
        },
        {
            "name": "Hustle Finder",
            "period": "2023/5–2023/11",
            "highlights": [
                "600+ side hustles",
                "Search + pagination",
                "Next.js, React, TailwindCSS",
                "Adsterra integration",
                "Bookmarks + theme system"
            ]
        },
        {
            "name": "Matty AI",
            "period": "2024/5–2024/8",
            "highlights": [
                "Chat-based AI companion",
                "Node.js + Express backend",
                "No login",
                "Voice input, file share, emoji support",
                "Anonymous, private experience"
            ]
        }
    ],
    "about": [
        "50+ global client projects",
        "Web, mobile, and game development",
        "Expertise in React, Next.js, Node.js, MongoDB, and AI tools",
        "Strong UI/UX understanding",
        "Experience building portfolio sites, resume builders, and full-stack apps",
        "Built AI assistants, chat apps, and custom tools",
        "Fast learner with deep technical research skills",
        "Active collaborator on GitHub"
    ],
}


def simple_answer(prompt: str) -> str:
    q = prompt.lower().strip()
    # Greeting
    if any(k in q for k in ["hello", "hi", "hey"]):
        return f"Hey! I'm {PROFILE['name']}, a {PROFILE['title']}. I build immersive web experiences, AI tools, and modern applications. How can I help?"
    # Skills
    if "skill" in q or "stack" in q or "tech" in q:
        return (
            "Here’s my core stack:\n"
            f"- Frontend: {', '.join(PROFILE['skills']['frontend'])}\n"
            f"- Backend: {', '.join(PROFILE['skills']['backend'])}\n"
            f"- Databases: {', '.join(PROFILE['skills']['database'])}\n"
            f"- AI & IDEs: {', '.join(PROFILE['skills']['ai'][:8])}…\n"
            f"- Others: {', '.join(PROFILE['skills']['others'][:8])}…"
        )
    # Projects
    if "project" in q or "portfolio" in q or "work" in q:
        lines = []
        for p in PROFILE["projects"]:
            lines.append(f"• {p['name']} ({p['period']}): {p['highlights'][0]}")
        return "Some highlights:\n" + "\n".join(lines)
    # Contact
    if "contact" in q or "email" in q or "reach" in q:
        return "You can reach me at mmm045762s@gmail.com or +91 8983135250 (Maharashtra, IN)."
    # Default
    return (
        f"I'm {PROFILE['name']} — {PROFILE['title']}. "
        "I’ve delivered 50+ projects across web, mobile, and games. "
        "Ask me about my stack, projects, or availability."
    )


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    reply = simple_answer(req.message)
    return ChatResponse(reply=reply)


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
