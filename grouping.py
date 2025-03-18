import logging
from typing import List, Dict, Any

def group_events(events: List[Dict[str, Any]], grouping_window: float) -> List[Dict[str, Any]]:
    """
    Group events that occur within a specified time window and share the same user and action.
    
    Args:
        events: List of event dictionaries
        grouping_window: Time window in seconds for grouping events
        
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
        if (event["timestamp"] - last_event["timestamp"] <= grouping_window and
                event["user"] == last_event["user"] and
                event["action"] == last_event["action"]):
            current_group.append(event)
        else:
            # Append group summary (e.g., count and earliest timestamp)
            grouped.append({
                "timestamp": current_group[0]["timestamp"],
                "user": current_group[0]["user"],
                "action": current_group[0]["action"],
                "file_count": len(current_group)
            })
            current_group = [event]
            
    if current_group:
        grouped.append({
            "timestamp": current_group[0]["timestamp"],
            "user": current_group[0]["user"],
            "action": current_group[0]["action"],
            "file_count": len(current_group)
        })
        
    logging.info("Grouped %d events into %d groups", len(events), len(grouped))
    return grouped
