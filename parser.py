import logging
from typing import List, Dict, Any

def parse_log_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse a Gource log file and return a list of event dictionaries.
    
    Each event contains:
    - timestamp: float
    - user: str
    - action: str (A=Added, M=Modified, D=Deleted)
    - file_path: str
    
    Args:
        file_path: Path to the Gource log file
        
    Returns:
        List of event dictionaries
    """
    events = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) != 4:
                    logging.warning("Skipping malformed line: %s", line.strip())
                    continue
                timestamp_str, user, action, file_path = parts
                if action not in ('A', 'M', 'D'):
                    logging.warning("Unknown action type '%s' in line: %s", action, line.strip())
                    continue
                # Convert timestamp (ensure proper type, e.g., float or int)
                try:
                    timestamp = float(timestamp_str)
                except ValueError:
                    logging.warning("Invalid timestamp '%s' in line: %s", timestamp_str, line.strip())
                    continue
                # Create and append the event object/dict
                events.append({
                    "timestamp": timestamp,
                    "user": user,
                    "action": action,
                    "file_path": file_path
                })
    except Exception as e:
        logging.error("Error reading log file: %s", e)
        raise
        
    logging.info("Parsed %d events from log file", len(events))
    return events
