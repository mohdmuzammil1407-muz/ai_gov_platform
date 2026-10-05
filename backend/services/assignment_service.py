from db import complaints_collection, users_collection


DEPARTMENT_ALIASES = {
    "Electricity": ["Electricity", "Electricity Board"],
    "Fire and Rescue": ["Fire and Rescue", "Fire Department"],
    "Health": ["Health", "Health Department"],
    "Local Self Government": [
        "Local Self Government",
        "Local Self-Government",
        "Sanitation",
    ],
    "Public Works": ["Public Works"],
    "Transport": ["Transport"],
    "Police": ["Police"],
}


def _department_filters(department):
    aliases = DEPARTMENT_ALIASES.get(department, [department])
    return aliases


def find_assignee_for_department(department):
    staff_members = list(
        users_collection.find(
            {
                "role": "staff",
                "department": {"$in": _department_filters(department)},
                "$or": [{"is_active": {"$exists": False}}, {"is_active": True}],
            },
            {"_id": 0, "user_id": 1},
        )
    )

    if not staff_members:
        return None

    staff_ids = [member["user_id"] for member in staff_members]
    complaint_counts = {
        staff_id: complaints_collection.count_documents({"assigned_to": staff_id})
        for staff_id in staff_ids
    }

    return min(complaint_counts, key=complaint_counts.get)
