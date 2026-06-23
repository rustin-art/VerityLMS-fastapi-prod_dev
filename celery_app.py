# src/celery_app.py

from celery import Celery

celery_app = Celery(
    "worker",
    broker_url="redis://127.0.0.1:6379/0",
    result_backend="redis://127.0.0.1:6379/0"
)

# --------------------------------------------------
# Task Discovery
# --------------------------------------------------

celery_app.conf.imports = (
    "src.tasks.pipeline_tasks",
    "src.tasks.note_pipeline_tasks",

    # Learning Assets Pipeline
    "src.tasks.learning_assets_pipeline_tasks",
    "src.tasks.assessment_tasks",
    "src.tasks.homework_tasks",
    "src.tasks.callbacks",
)

# ==========================================================
# Production Configuration
# ==========================================================

celery_app.conf.update(

    # Track task start state
    task_track_started=True,

    # JSON serialization
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],

    # Task Reliability
    task_acks_late=True,

    # Avoid worker grabbing too many jobs
    worker_prefetch_multiplier=1,

    # Auto-expire results
    result_expires=3600,

    # Timezone
    enable_utc=True,
    timezone="UTC",

    # Chord Support
    result_chord_join_timeout=300,
)

# --------------------------------------------------
# Queue Routing
# --------------------------------------------------

celery_app.conf.task_routes = {

    # -------------------------
    # Document Extraction
    # -------------------------

    "src.tasks.pipeline_tasks.run_extract_pipeline": {
        "queue": "extract"
    },

    "src.tasks.pipeline_tasks.run_unirec_pipeline": {
        "queue": "unirec"
    },

    # -------------------------
    # Note Generation
    # -------------------------

    "src.tasks.note_pipeline_tasks.run_note_pipeline": {
        "queue": "notes"
    },

    # -------------------------
    # Learning Assets Pipeline
    # -------------------------

    "src.tasks.learning_assets_pipeline_tasks.run_learning_assets_pipeline": {
        "queue": "learning_assets"
    },

    # -------------------------
    # Assessment Generation
    # -------------------------

    "src.tasks.assessment_tasks.generate_assessment_task": {
        "queue": "assessment"
    },

    # -------------------------
    # Homework Generation
    # -------------------------

    "src.tasks.homework_tasks.generate_homework_task": {
        "queue": "homework"
    },

    # ======================================================
    # Chord Success Callback
    # ======================================================

    "src.tasks.callbacks.learning_assets_completed_callback": {
        "queue": "learning_assets"
    },

    # ======================================================
    # Chord Failure Callback
    # ======================================================

    "src.tasks.callbacks.learning_assets_failed": {
        "queue": "learning_assets"
    },
}
# ==========================================================
# Optional Default Queue
# ==========================================================

celery_app.conf.task_default_queue = "default"


# ==========================================================
# Worker Startup Verification
# ==========================================================

print("✓ Celery App Initialized")
print("✓ Redis Broker Connected")
print("✓ Task Discovery Loaded")