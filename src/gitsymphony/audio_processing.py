import logging
from datetime import datetime
from typing import Any, Dict, List

from pydub import AudioSegment


def process_audio(
    mapped_events: List[Dict[str, Any]],
    scaling_factor: float,
    sound_folder: str,
    output: str,
    input_basename: str,
):
    """
    Create an audio track by placing sound clips at scaled timestamps.

    Args:
        mapped_events: List of mapped event dictionaries
        scaling_factor: Factor to scale timestamps (seconds in log to milliseconds in audio)
        sound_folder: Folder containing sound files
        output: Output directory for the final audio file
        input_basename: Base name of the input file for naming the output
    """
    logging.info("Starting audio processing with %d mapped events", len(mapped_events))
    
    # Check if there are any events to process
    if not mapped_events:
        logging.warning("No mapped events to process, skipping audio generation")
        return
    # Create a silent base audio track; length can be computed based on max scaled timestamp.
    try:
        max_time = (
            max(e["timestamp"] for e in mapped_events) * scaling_factor * 1000
        )  # in ms
        logging.info("Creating silent base track with duration: %d ms", max_time + 1000)
        final_track = AudioSegment.silent(duration=max_time + 1000)  # extra buffer
    except Exception as e:
        logging.error("Failed to create base audio track: %s", e)
        return

    # Keep track of processed events
    processed_count = 0
    error_count = 0
    
    for event in mapped_events:
        # Calculate the placement time in milliseconds (scaled)
        place_time = int(event["timestamp"] * scaling_factor * 1000)
        sound_path = f"{sound_folder}/{event['sound_file']}"
        
        logging.debug("Processing event at time %d ms with sound file: %s", place_time, sound_path)

        try:
            clip = AudioSegment.from_wav(sound_path)
            # Overlay the sound clip
            final_track = final_track.overlay(clip, position=place_time)
            processed_count += 1
            
            # Log progress periodically
            if processed_count % 1000 == 0:
                logging.info("Processed %d events so far...", processed_count)
        except FileNotFoundError:
            logging.error("Sound file not found: %s", sound_path)
            error_count += 1
        except Exception as e:
            logging.error("Error processing event with sound file '%s': %s", sound_path, e)
            error_count += 1
            continue

    # Define final audio filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_audio_name = f"{output}/{input_basename}_soundtrack_{timestamp}.wav"

    logging.info("Successfully processed %d events with %d errors", processed_count, error_count)
    
    try:
        logging.info("Exporting final audio track to: %s", final_audio_name)
        final_track.export(final_audio_name, format="wav")
        logging.info("Final audio file created: %s", final_audio_name)
    except Exception as e:
        logging.error("Failed to export audio file: %s", e)
