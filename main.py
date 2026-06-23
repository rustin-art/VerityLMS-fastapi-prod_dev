from fastapi import FastAPI

from contextlib import asynccontextmanager

from .database import Base, engine

from .core.openocr_manager import ocr_manager
from .api.jobs import router as jobs_router



from .api.detect import router as detect_router
from .api.ocr import router as ocr_router
from .api.document import router as document_router
from .api.unirec import router as unirec_router

from .api.notes import router as notes_router
from .api.assessments import router as assessments_router
from .api.homeworks import router as homeworks_router
from .api.extracted_documents import router as extracted_documents_router
from .api.cleaned_documents import router as cleaned_documents_router
from .api.learning_assets import router as learning_assets_router


from .models.note import NoteModel
from .models.assessment import AssessmentModel
from .models.homework import HomeworkModel
from .models.extracted_document import ExtractedDocumentModel
from .models.cleaned_document import CleanedDocumentModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ocr = ocr_manager
    yield

app = FastAPI(
    title= "content Generation",
    description="API is for AI to generate content",
    lifespan=lifespan
)

print("#################################################\n")
print("##                                             ##\n")
print("## VERITYLMS CONTENT GENERATION APP            ##\n")
print("##                                             ##\n")
print("##             By: Rustin Alpin, Rishi Lalwani ##\n")
print("#################################################\n")




print("<!---- Initializing API for Text & OCR Recognition ----!>")
print("<!---- Initializing Text Detection API ----!>")
app.include_router(detect_router)
print("<!---- Initializing OCR API ----!>")
app.include_router(ocr_router)
print("<!---- Initializing Document parsing API ----!>")
app.include_router(document_router)
print("<!---- Initializing Uni-Rec API ----!>")
app.include_router(unirec_router)
print("<!---- API for Text & OCR Recognition is Running ... ----!>")

print("<!---- Initializing extracted documents API ----!>")
app.include_router(extracted_documents_router)
print("<!---- API for extracted documents is Running ... ----!>")

print("<!---- Initializing Cleaned documents API ----!>")
app.include_router(cleaned_documents_router)
print("<!---- API for Cleaned documents is Running ... ----!>")

print("<!---- Initializing Redis & Celery Jobs API ----!>")
app.include_router(jobs_router)
print("<!---- API for Redis & Celery Jobs is Running ... ----!>")

print("<!---- Initializing router Learning Assests Pipeline API ----!>")
app.include_router(learning_assets_router)
print("<!---- API for Learning Assests Pipeline is Running ... ----!>")


Base.metadata.create_all(bind=engine)


print("!<----Sanity check for GET request API---->!")
@app.get('/')
def sanity():
    return {"message":"API is working"}


print("<!---- Notes API for creating Notes ----!>")
app.include_router(notes_router)
print("<!---- Assessment API for creating MCQ's ----!>")
app.include_router(assessments_router)
print("<!---- HomeWork API for creating HomeWork Questions ----!>")
app.include_router(homeworks_router)
print("<!---- LMS Modules Initialized ----!>")

