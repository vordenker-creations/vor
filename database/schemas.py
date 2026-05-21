import json

# 1. RAW INPUT SCHEMA (What the user types into the Profile Form)
# This will be stored in student_context.raw_input
RAW_INPUT_SCHEMA = {
    "student_info": {
        "full_name": "",
        "major": "",
        "current_semester": 1,
        "gpa": 0.0,
        "skills": []
    },
    "academic_context": {
        "current_courses": [],
        "completed_courses": [],
        "timetable_manual": []
    },
    "career_goals": {
        "target_role": "",
        "interests": []
    }
}

# 2. AI GENERATED PROFILE SCHEMA (What the backend returns from /analyze-context)
# This will be stored in student_context.ai_generated_profile
# The UI (Dashboard/Timetable) must render strictly from this object.
AI_GENERATED_PROFILE_SCHEMA = {
    "student_summary": "", # e.g. "A dedicated CS freshman focusing on backend systems."
    "skill_analysis": {
        "strengths": [],
        "weaknesses": [],
        "recommended_focus": []
    },
    "weekly_study_plan": [
        {
            "day": "Monday",
            "tasks": [
                {"title": "", "type": "study", "duration_min": 60, "priority": "high"}
            ]
        }
    ],
    "academic_roadmap": [
        {
            "title": "Data Structures",
            "status": "in_progress",
            "progress_pct": 45,
            "ai_insight": "Critical for your target Software Engineer role."
        }
    ],
    "metrics": {
        "academic_progress": 0, # 0-100
        "career_readiness": 0,   # 0-100
        "task_completion": 0    # 0-100
    }
}

def get_default_context_json():
    """Returns a fresh, empty context payload."""
    return {
        "raw_input": RAW_INPUT_SCHEMA,
        "ai_generated_profile": AI_GENERATED_PROFILE_SCHEMA,
        "ai_status": "EMPTY"
    }
