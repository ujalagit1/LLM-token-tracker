from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv
from google import genai

from datetime import datetime
import time
import os

from pricing import MODEL_PRICING
from database import (
    save_request,
    get_history,
    get_analytics,
    most_used_model,
    delete_request
)

app = FastAPI()

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# -----------------------------
# Home
# -----------------------------

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "result": None
        }
    )


# -----------------------------
# HTML Chat
# -----------------------------

@app.post("/chat")
async def chat(
    request: Request,
    model: str = Form(...),
    prompt: str = Form(...)
):

    try:

        start_time = time.time()

        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        end_time = time.time()

        response_time = round(end_time - start_time, 2)

        generated_at = datetime.now().strftime(
            "%d %b %Y %I:%M:%S %p"
        )

        input_tokens = response.usage_metadata.prompt_token_count
        output_tokens = response.usage_metadata.candidates_token_count
        thinking_tokens = response.usage_metadata.thoughts_token_count
        total_tokens = response.usage_metadata.total_token_count

        price = MODEL_PRICING[model]

        input_cost = (
            input_tokens / 1_000_000
        ) * price["input"]

        output_cost = (
            output_tokens / 1_000_000
        ) * price["output"]

        total_cost = input_cost + output_cost

        save_request(
            model,
            prompt,
            response.text,
            input_tokens,
            output_tokens,
            thinking_tokens,
            total_tokens,
            total_cost
        )

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "result": {

                    "model": model,

                    "prompt": prompt,

                    "response": response.text,

                    "input_tokens": input_tokens,

                    "output_tokens": output_tokens,

                    "thinking_tokens": thinking_tokens,

                    "total_tokens": total_tokens,

                    "estimated_cost": f"₹ {total_cost:.6f}",

                    "response_time": response_time,

                    "generated_at": generated_at
                }
            }
        )

    except Exception as e:

        return JSONResponse(
            {
                "error": str(e)
            }
        )


# -----------------------------
# History
# -----------------------------

@app.get("/history")
async def history(request: Request):

    history = get_history()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "history": history
        }
    )


# -----------------------------
# Delete Request
# -----------------------------

@app.get("/delete/{request_id}")
async def delete(request_id: int):

    delete_request(request_id)

    return RedirectResponse(
        url="/history",
        status_code=303
    )


# -----------------------------
# Analytics
# -----------------------------

@app.get("/analytics")
async def analytics(request: Request):

    analytics = get_analytics()

    model = most_used_model()

    return templates.TemplateResponse(
        request=request,
        name="analytics.html",
        context={
            "analytics": analytics,
            "model": model
        }
    )


# -----------------------------
# AJAX API
# -----------------------------

@app.post("/api/chat")
async def api_chat(

    model: str = Form(...),

    prompt: str = Form(...)

):

    try:

        start_time = time.time()

        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        end_time = time.time()

        response_time = round(
            end_time - start_time,
            2
        )

        generated_at = datetime.now().strftime(
            "%d %b %Y %I:%M:%S %p"
        )

        input_tokens = response.usage_metadata.prompt_token_count
        output_tokens = response.usage_metadata.candidates_token_count
        thinking_tokens = response.usage_metadata.thoughts_token_count
        total_tokens = response.usage_metadata.total_token_count

        price = MODEL_PRICING[model]

        input_cost = (
            input_tokens / 1_000_000
        ) * price["input"]

        output_cost = (
            output_tokens / 1_000_000
        ) * price["output"]

        total_cost = input_cost + output_cost

        save_request(
            model,
            prompt,
            response.text,
            input_tokens,
            output_tokens,
            thinking_tokens,
            total_tokens,
            total_cost
        )

        return {

            "model": model,

            "prompt": prompt,

            "response": response.text,

            "input_tokens": input_tokens,

            "output_tokens": output_tokens,

            "thinking_tokens": thinking_tokens,

            "total_tokens": total_tokens,

            "estimated_cost": f"₹ {total_cost:.6f}",

            "response_time": response_time,

            "generated_at": generated_at

        }

    except Exception as e:

        return {

            "error": str(e)

        }