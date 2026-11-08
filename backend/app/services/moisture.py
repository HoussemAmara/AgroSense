# Placeholder ranges (% soil moisture), to be calibrated with real sensor data.
DEFAULT_RANGES = {
    "frequent": (60.0, 80.0),
    "average": (40.0, 60.0),
    "minimum": (20.0, 40.0),
}


def default_range(category: str | None) -> tuple[float, float] | None:
    if category is None:
        return None
    return DEFAULT_RANGES.get(category.strip().lower())