from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from docx import Document
import re

app = FastAPI()

# allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- CA SKILLS ----------------
CA_SKILLS = {
    "GST": ["gst", "gstr", "itc", "rule 42", "rule 43"],
    "Direct Tax": ["income tax", "tds", "tcs", "assessment", "scrutiny", "43b", "44ad"],
    "Audit": ["audit", "internal audit", "statutory audit", "controls"],
    "Ind AS": ["ind as", "indas", "financial reporting"],
}

# ---------------- HELPERS ----------------
def read_docx(file):
    doc = Document(file)
    lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    text = " ".join(lines).lower()
    return lines, text

def score(text, keywords, max_score):
    hits = sum(1 for k in keywords if k in text)
    return min(int(hits * max_score / len(keywords)), max_score)

# ---------------- API ----------------
@app.post("/evaluate")
async def evaluate(jd_text: str = Form(...), cv: UploadFile = File(...)):
    cv_lines, cv_text = read_docx(cv.file)
    jd_text = jd_text.lower()

    scores = {
        "GST": score(cv_text, CA_SKILLS["GST"], 20),
        "Direct Tax": score(cv_text, CA_SKILLS["Direct Tax"], 15),
        "Audit": score(cv_text, CA_SKILLS["Audit"], 15),
        "Ind AS": score(cv_text, CA_SKILLS["Ind AS"], 15),
    }

    jd_words = set(re.findall(r"\b[a-z]{4,}\b", jd_text))
    cv_words = set(re.findall(r"\b[a-z]{4,}\b", cv_text))
    scores["JD Alignment"] = min(int(len(jd_words & cv_words) / max(len(jd_words),1) * 20), 20)
    scores["Formatting"] = 15 if len(cv_lines) > 12 else 8

    total = sum(scores.values())

    feedback = []
    for line in cv_lines:
        l = line.lower()
        if any(x in l for x in ["responsible", "handled", "worked on"]) and not re.search(r"\d", l):
            feedback.append(
                f"Rewrite '{line}' to include numbers, scale, and impact."
            )

    if total < 50:
        feedback.append("Overall CV lacks depth. Add quantified achievements and JD keywords.")

    return JSONResponse({
        "total": total,
        "scores": scores,
        "feedback": feedback
    })
