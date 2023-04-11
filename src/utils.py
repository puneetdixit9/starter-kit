from datetime import datetime


def update_class_object(obj, updated_dict):
    for k, v in updated_dict.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    if hasattr(obj, "updated_at"):
        setattr(obj, "updated_at", datetime.now())
    return obj
