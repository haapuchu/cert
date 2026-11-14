import os
import uvicorn
from fastapi import FastAPI, Response, Body
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from certificate_engine import generate_pdf, DEFAULT_NAME, DEFAULT_DATE

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

@app.post("/api/export/pdf")
def export_pdf(payload: dict = Body(...)):
    name = payload.get("name", DEFAULT_NAME)
    date = payload.get("date", DEFAULT_DATE)
    pdf_bytes = generate_pdf(name, date)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="certificate.pdf"'}
    )

app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
