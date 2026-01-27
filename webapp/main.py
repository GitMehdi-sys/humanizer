"""
FastAPI Web Application for Humanize Library

This web app provides a user-friendly interface to access all humanize functions
through forms and interactive demos.
"""
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta, date
import sys
from pathlib import Path

# Add src directory to Python path so we can import humanize
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import humanize

app = FastAPI(
    title="Humanize Web App",
    description="Interactive web interface for Python humanize library",
    version="1.0.0"
)

# Mount static files
static_path = Path(__file__).parent / "static"
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Initialize OpenAI client with API key
try:
    from openai import OpenAI
    openai_client = OpenAI(api_key="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")
    OPENAI_AVAILABLE = True
except Exception as e:
    print(f"Warning: OpenAI not available: {e}")
    OPENAI_AVAILABLE = False
    openai_client = None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main landing page with navigation to all features"""
    return templates.TemplateResponse("index.html", {"request": request})


# ==================== INTEGER HUMANIZATION ====================

@app.get("/integers", response_class=HTMLResponse)
async def integers_page(request: Request):
    """Page for integer humanization functions"""
    return templates.TemplateResponse("integers.html", {
        "request": request,
        "result": None
    })


@app.post("/integers/intcomma", response_class=HTMLResponse)
async def intcomma_post(request: Request, value: str = Form(...), ndigits: str = Form("")):
    """Process intcomma form submission"""
    try:
        ndigits_val = int(ndigits) if ndigits else None
        result = humanize.intcomma(value, ndigits_val)
        success = True
    except Exception as e:
        result = f"Error: {str(e)}"
        success = False
    
    return templates.TemplateResponse("integers.html", {
        "request": request,
        "result": {"function": "intcomma", "output": result, "success": success, "input": value}
    })


@app.post("/integers/intword", response_class=HTMLResponse)
async def intword_post(request: Request, value: str = Form(...), format_str: str = Form("%.1f")):
    """Process intword form submission"""
    try:
        result = humanize.intword(value, format_str)
        success = True
    except Exception as e:
        result = f"Error: {str(e)}"
        success = False
    
    return templates.TemplateResponse("integers.html", {
        "request": request,
        "result": {"function": "intword", "output": result, "success": success, "input": value}
    })


@app.post("/integers/apnumber", response_class=HTMLResponse)
async def apnumber_post(request: Request, value: str = Form(...)):
    """Process apnumber form submission"""
    try:
        result = humanize.apnumber(value)
        success = True
    except Exception as e:
        result = f"Error: {str(e)}"
        success = False
    
    return templates.TemplateResponse("integers.html", {
        "request": request,
        "result": {"function": "apnumber", "output": result, "success": success, "input": value}
    })


@app.post("/integers/ordinal", response_class=HTMLResponse)
async def ordinal_post(request: Request, value: str = Form(...)):
    """Process ordinal form submission"""
    try:
        result = humanize.ordinal(value)
        success = True
    except Exception as e:
        result = f"Error: {str(e)}"
        success = False
    
    return templates.TemplateResponse("integers.html", {
        "request": request,
        "result": {"function": "ordinal", "output": result, "success": success, "input": value}
    })


# ==================== DATE & TIME HUMANIZATION ====================

@app.get("/datetime", response_class=HTMLResponse)
async def datetime_page(request: Request):
    """Page for date/time humanization functions"""
    return templates.TemplateResponse("datetime.html", {
        "request": request,
        "result": None
    })


@app.post("/datetime/naturaltime", response_class=HTMLResponse)
async def naturaltime_post(request: Request, 
                          time_type: str = Form(...),
                          seconds: str = Form(""),
                          minutes: str = Form(""),
                          hours: str = Form(""),
                          days: str = Form("")):
    """Process naturaltime form submission"""
    try:
        if time_type == "now":
            delta = timedelta(seconds=0)
        else:
            total_seconds = 0
            if seconds:
                total_seconds += int(seconds)
            if minutes:
                total_seconds += int(minutes) * 60
            if hours:
                total_seconds += int(hours) * 3600
            if days:
                total_seconds += int(days) * 86400
            
            if time_type == "past":
                delta = timedelta(seconds=total_seconds)
                result = humanize.naturaltime(datetime.now() - delta)
            else:  # future
                delta = timedelta(seconds=total_seconds)
                result = humanize.naturaltime(datetime.now() + delta, future=True)
        
        if time_type == "now":
            result = "now"
        
        success = True
    except Exception as e:
        result = f"Error: {str(e)}"
        success = False
    
    return templates.TemplateResponse("datetime.html", {
        "request": request,
        "result": {"function": "naturaltime", "output": result, "success": success}
    })


@app.post("/datetime/naturaldelta", response_class=HTMLResponse)
async def naturaldelta_post(request: Request,
                           seconds: str = Form(""),
                           minutes: str = Form(""),
                           hours: str = Form(""),
                           days: str = Form("")):
    """Process naturaldelta form submission"""
    try:
        total_seconds = 0
        if seconds:
            total_seconds += int(seconds)
        if minutes:
            total_seconds += int(minutes) * 60
        if hours:
            total_seconds += int(hours) * 3600
        if days:
            total_seconds += int(days) * 86400
        
        delta = timedelta(seconds=total_seconds)
        result = humanize.naturaldelta(delta)
        success = True
    except Exception as e:
        result = f"Error: {str(e)}"
        success = False
    
    return templates.TemplateResponse("datetime.html", {
        "request": request,
        "result": {"function": "naturaldelta", "output": result, "success": success}
    })


@app.post("/datetime/naturalday", response_class=HTMLResponse)
async def naturalday_post(request: Request, 
                         date_type: str = Form(...),
                         custom_date: str = Form("")):
    """Process naturalday form submission"""
    try:
        if date_type == "today":
            value = date.today()
        elif date_type == "yesterday":
            value = date.today() - timedelta(days=1)
        elif date_type == "tomorrow":
            value = date.today() + timedelta(days=1)
        else:  # custom
            value = datetime.strptime(custom_date, "%Y-%m-%d").date()
        
        result = humanize.naturalday(value)
        success = True
    except Exception as e:
        result = f"Error: {str(e)}"
        success = False
    
    return templates.TemplateResponse("datetime.html", {
        "request": request,
        "result": {"function": "naturalday", "output": result, "success": success}
    })


@app.post("/datetime/naturaldate", response_class=HTMLResponse)
async def naturaldate_post(request: Request, custom_date: str = Form(...)):
    """Process naturaldate form submission"""
    try:
        value = datetime.strptime(custom_date, "%Y-%m-%d").date()
        result = humanize.naturaldate(value)
        success = True
    except Exception as e:
        result = f"Error: {str(e)}"
        success = False
    
    return templates.TemplateResponse("datetime.html", {
        "request": request,
        "result": {"function": "naturaldate", "output": result, "success": success}
    })


@app.post("/datetime/precisedelta", response_class=HTMLResponse)
async def precisedelta_post(request: Request,
                           days: str = Form(""),
                           hours: str = Form(""),
                           minutes: str = Form(""),
                           seconds: str = Form("")):
    """Process precisedelta form submission"""
    try:
        delta = timedelta(
            days=int(days) if days else 0,
            hours=int(hours) if hours else 0,
            minutes=int(minutes) if minutes else 0,
            seconds=int(seconds) if seconds else 0
        )
        result = humanize.precisedelta(delta)
        success = True
    except Exception as e:
        result = f"Error: {str(e)}"
        success = False
    
    return templates.TemplateResponse("datetime.html", {
        "request": request,
        "result": {"function": "precisedelta", "output": result, "success": success}
    })


# ==================== FILE SIZE HUMANIZATION ====================

@app.get("/filesize", response_class=HTMLResponse)
async def filesize_page(request: Request):
    """Page for file size humanization"""
    return templates.TemplateResponse("filesize.html", {
        "request": request,
        "result": None
    })


@app.post("/filesize/naturalsize", response_class=HTMLResponse)
async def naturalsize_post(request: Request, 
                          value: str = Form(...),
                          binary: bool = Form(False),
                          gnu: bool = Form(False)):
    """Process naturalsize form submission"""
    try:
        result = humanize.naturalsize(value, binary=binary, gnu=gnu)
        success = True
    except Exception as e:
        result = f"Error: {str(e)}"
        success = False
    
    return templates.TemplateResponse("filesize.html", {
        "request": request,
        "result": {"function": "naturalsize", "output": result, "success": success, "input": value}
    })


# ==================== SCIENTIFIC & FRACTIONAL ====================

@app.get("/scientific", response_class=HTMLResponse)
async def scientific_page(request: Request):
    """Page for scientific and fractional notation"""
    return templates.TemplateResponse("scientific.html", {
        "request": request,
        "result": None
    })


@app.post("/scientific/fractional", response_class=HTMLResponse)
async def fractional_post(request: Request, value: str = Form(...)):
    """Process fractional form submission"""
    try:
        result = humanize.fractional(value)
        success = True
    except Exception as e:
        result = f"Error: {str(e)}"
        success = False
    
    return templates.TemplateResponse("scientific.html", {
        "request": request,
        "result": {"function": "fractional", "output": result, "success": success, "input": value}
    })


@app.post("/scientific/scientific", response_class=HTMLResponse)
async def scientific_post(request: Request, 
                         value: str = Form(...),
                         precision: str = Form("2")):
    """Process scientific form submission"""
    try:
        prec = int(precision) if precision else 2
        result = humanize.scientific(value, precision=prec)
        success = True
    except Exception as e:
        result = f"Error: {str(e)}"
        success = False
    
    return templates.TemplateResponse("scientific.html", {
        "request": request,
        "result": {"function": "scientific", "output": result, "success": success, "input": value}
    })


# ==================== AI TEXT HUMANIZATION ====================

@app.get("/ai-humanize", response_class=HTMLResponse)
async def ai_humanize_page(request: Request):
    """Page for AI text humanization"""
    return templates.TemplateResponse("ai_humanize.html", {
        "request": request,
        "result": None
    })


@app.post("/ai-humanize/process", response_class=HTMLResponse)
async def ai_humanize_post(request: Request, 
                           text: str = Form(...),
                           style: str = Form("natural")):
    """Process AI text humanization"""
    if not OPENAI_AVAILABLE or openai_client is None:
        result = {
            "error": "OpenAI is not installed. Run: pip install openai",
            "success": False
        }
        return templates.TemplateResponse("ai_humanize.html", {
            "request": request,
            "result": result
        })
    
    try:
        # Create the prompt based on selected style
        style_prompts = {
            "natural": "Rewrite the following text to sound more natural and human-like, removing any robotic or AI-like patterns. Keep the meaning the same but make it conversational:",
            "casual": "Rewrite the following text in a casual, friendly tone as if you're talking to a friend. Remove formal language and make it relatable:",
            "professional": "Rewrite the following text in a professional yet approachable tone. Remove AI-like patterns while maintaining clarity and professionalism:",
            "creative": "Rewrite the following text in a creative and engaging way. Add personality and flair while keeping the core message:",
            "simple": "Rewrite the following text in simple, easy-to-understand language. Break down complex ideas and make it accessible to everyone:"
        }
        
        prompt = style_prompts.get(style, style_prompts["natural"])
        
        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that humanizes AI-generated text by making it sound more natural, conversational, and human-written."},
                {"role": "user", "content": f"{prompt}\n\n{text}"}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        humanized_text = response.choices[0].message.content.strip()
        
        # Calculate some stats
        original_length = len(text.split())
        humanized_length = len(humanized_text.split())
        
        result = {
            "original": text,
            "humanized": humanized_text,
            "style": style,
            "original_words": original_length,
            "humanized_words": humanized_length,
            "success": True
        }
        
    except Exception as e:
        result = {
            "error": str(e),
            "success": False
        }
    
    return templates.TemplateResponse("ai_humanize.html", {
        "request": request,
        "result": result
    })


# ==================== API ENDPOINTS (JSON) ====================

@app.get("/api/intcomma/{value}")
async def api_intcomma(value: str):
    """API endpoint for intcomma"""
    return {"input": value, "output": humanize.intcomma(value)}


@app.get("/api/intword/{value}")
async def api_intword(value: str):
    """API endpoint for intword"""
    return {"input": value, "output": humanize.intword(value)}


@app.get("/api/naturalsize/{value}")
async def api_naturalsize(value: int, binary: bool = False):
    """API endpoint for naturalsize"""
    return {"input": value, "output": humanize.naturalsize(value, binary=binary)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)