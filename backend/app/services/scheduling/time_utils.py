"""Time conversion and interval arithmetic utility functions."""

def parse_time(time_str: str) -> int:
    """
    Convert a 24-hour time string 'HH:MM' into integer minutes from midnight.
    Example: '09:30' -> 9 * 60 + 30 = 570
    """
    parts = time_str.strip().split(":")
    if len(parts) != 2:
        raise ValueError(f"Invalid time format '{time_str}', expected 'HH:MM'")
    hours, minutes = int(parts[0]), int(parts[1])
    if not (0 <= hours <= 23 and 0 <= minutes <= 59):
        raise ValueError(f"Time out of 24h range: '{time_str}'")
    return hours * 60 + minutes

def format_time(minutes_from_midnight: int) -> str:
    """
    Convert integer minutes from midnight back into a 24-hour time string 'HH:MM'.
    Example: 570 -> '09:30'
    """
    if minutes_from_midnight < 0:
        minutes_from_midnight = 0
    hours = (minutes_from_midnight // 60) % 24
    mins = minutes_from_midnight % 60
    return f"{hours:02d}:{mins:02d}"

def duration_between(start_minutes: int, end_minutes: int) -> int:
    """Return the duration in minutes between start and end."""
    return max(0, end_minutes - start_minutes)

def overlaps(start1: int, end1: int, start2: int, end2: int) -> bool:
    """
    Standard interval overlap condition:
    Two intervals [start1, end1) and [start2, end2) overlap if:
    start1 < end2 and start2 < end1
    Boundary touching (e.g. end1 == start2) is NOT considered an overlap.
    """
    return (start1 < end2) and (start2 < end1)
