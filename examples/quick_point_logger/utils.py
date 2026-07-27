from datetime import datetime, timezone


def utc_timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def safe_filename(value, fallback="captured_points"):
    import re
    clean = re.sub(r"[^\w\s-]", "", str(value), flags=re.UNICODE)
    clean = re.sub(r"[-\s]+", "_", clean).strip("_")
    return clean or fallback
