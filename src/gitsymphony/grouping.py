import logging
from typing import Any, Dict, List


def group_events(
    events: List[Dict[str, Any]], grouping_window: float, min_files: int = 4
) -> List[Dict[str, Any]]:
    """
    Group events that occur within a specified time window and share the same user and action.
    Only groups with more than the minimum number of files are included.

    Args:
        events: List of event dictionaries
        grouping_window: Time window in seconds for grouping events
        min_files: Minimum number of files required for a group to be included (default: 4)

    Returns:
        List of grouped event dictionaries
    """
    events.sort(key=lambda e: e["timestamp"])
    grouped, current_group = [], []

    for event in events:
        if not current_group:
            current_group.append(event)
            continue

        last_event = current_group[-1]
        # Check grouping criteria: time difference and same user/action
        if (
            event["timestamp"] - last_event["timestamp"] <= grouping_window
            and event["user"] == last_event["user"]
            and event["action"] == last_event["action"]
        ):
            current_group.append(event)
        else:
            # Append group summary only if it meets the minimum file count threshold
            if len(current_group) >= min_files:
                grouped.append(
                    {
                        "timestamp": current_group[0]["timestamp"],
                        "user": current_group[0]["user"],
                        "action": current_group[0]["action"],
                        "file_count": len(current_group),
                    }
                )
            current_group = [event]

    if current_group and len(current_group) >= min_files:
        grouped.append(
            {
                "timestamp": current_group[0]["timestamp"],
                "user": current_group[0]["user"],
                "action": current_group[0]["action"],
                "file_count": len(current_group),
            }
        )

    logging.info("Grouped %d events into %d groups", len(events), len(grouped))
    return grouped
