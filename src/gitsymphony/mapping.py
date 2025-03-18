import logging
from typing import Any, Dict, List


def map_events(
    grouped_events: List[Dict[str, Any]], mapping_rules: Dict[str, List[Dict[str, Any]]]
) -> List[Dict[str, Any]]:
    """
    Map grouped events to sound files based on action type only.

    Args:
        grouped_events: List of grouped event dictionaries
        mapping_rules: Dictionary with 'actions' mapping rules

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
    logging.info("Mapped %d groups to %d sound events", len(grouped_events), len(result))
    return result
