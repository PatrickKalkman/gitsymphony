import logging
from typing import Any, Dict, List, Optional


def map_events(
    grouped_events: List[Dict[str, Any]], 
    mapping_rules: Dict[str, List[Dict[str, Any]]],
    min_sound_gap_seconds: Optional[float] = None
) -> List[Dict[str, Any]]:
    """
    Map grouped events to sound files based on action type only.

    Args:
        grouped_events: List of grouped event dictionaries
        mapping_rules: Dictionary with 'actions' mapping rules
        min_sound_gap_seconds: Minimum time gap between sounds in seconds (optional)

    Returns:
        List of mapped event dictionaries with sound_file attribute
    """
    mapped_events = []

    for group in grouped_events:
        action = group["action"]
        chosen_sound = None

        # Check action patterns
        for action_rule in mapping_rules.get("actions", []):
            if action == action_rule["pattern"]:
                chosen_sound = action_rule["sound_file"]
                break

        if chosen_sound is None:
            logging.warning("No mapping found for action: %s", action)
            continue

        group_copy = group.copy()
        group_copy["sound_file"] = chosen_sound
        mapped_events.append(group_copy)

    # If events overlap (same timestamp), retain the one with the larger file count.
    mapped_events.sort(key=lambda e: (e["timestamp"], -e["file_count"]))
    deduped = {}
    for event in mapped_events:
        ts = event["timestamp"]
        if ts not in deduped or event["file_count"] > deduped[ts]["file_count"]:
            deduped[ts] = event

    result = list(deduped.values())
    
    # Apply minimum gap between sounds if specified
    if min_sound_gap_seconds is not None and min_sound_gap_seconds > 0:
        result.sort(key=lambda e: e["timestamp"])
        filtered_events = []
        last_timestamp = None
        
        for event in result:
            if last_timestamp is None or (event["timestamp"] - last_timestamp) >= min_sound_gap_seconds:
                filtered_events.append(event)
                last_timestamp = event["timestamp"]
            else:
                logging.debug(f"Skipping event at {event['timestamp']} due to minimum gap constraint")
        
        logging.info("Applied minimum sound gap: reduced from %d to %d events", 
                    len(result), len(filtered_events))
        result = filtered_events

    logging.info("Mapped %d groups to %d sound events", len(grouped_events), len(result))
    return result
