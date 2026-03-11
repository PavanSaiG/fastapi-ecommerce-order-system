from fastapi import APIRouter, Cookie, Header
from typing import Optional

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/preferences")
def get_notification_preferences(
    user_agent: Optional[str] = Header(None),
    track_id: Optional[str] = Cookie(None)
):
    """
    WHY: Read user preferences to decide how to notify them.
    HOW: Demonstrates Header and Cookie parsing.
    """
    return {
        "user_agent": user_agent,
        "track_id": track_id,
        "message": "Preferences fetched via headers and cookies."
    }
