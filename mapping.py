import logging
from typing import Any, Dict, List


def map_events(
    grouped_events: List[Dict[str, Any]], mapping_rules: Dict[str, List[Dict[str, Any]]]
) -> List[Dict[str, Any]]:
    """
    Map grouped events to sound files based on mapping rules.

    Args:
        grouped_events: List of grouped event dictionaries
        mapping_rules: Dictionary of mapping rules by action type

    Returns:
        List of mapped event dictionaries with sound_file attribute
    """
    mapped_events = []

    for group in grouped_events:
        action_rules = mapping_rules.get(group["action"], [])
        chosen_sound = None

        for rule in action_rules:
            lower = rule.get("min", 1)  # defaults can be set as needed
            upper = rule.get("max", float("inf"))
            if lower <= group["file_count"] <= upper:
                chosen_sound = rule["file"]
                break

        if chosen_sound is None:
            logging.warning("No mapping found for group: %s", group)
            continue

        group["sound_file"] = chosen_sound
        mapped_events.append(group)

    # If events overlap (same timestamp), retain the one with the larger file count.
    mapped_events.sort(key=lambda e: (e["timestamp"], -e["file_count"]))
    deduped = {}
    for event in mapped_events:
        ts = event["timestamp"]
        if ts not in deduped or event["file_count"] > deduped[ts]["file_count"]:
            deduped[ts] = event

    result = list(deduped.values())
    logging.info(
        "Mapped %d groups to %d sound events", len(grouped_events), len(result)
    )
    return result
