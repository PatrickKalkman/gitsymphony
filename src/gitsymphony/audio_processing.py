import logging
from datetime import datetime
from typing import Any, Dict, List

from pydub import AudioSegment


def process_audio(
    mapped_events: List[Dict[str, Any]],
    sound_folder: str,
    output: str,
    input_basename: str,
    target_duration_seconds: int = 60,
    seconds_per_day: float = 0.01,
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
        
    # Normalize timestamps relative to the first event
    try:
        if mapped_events:
            first_timestamp = min(e["timestamp"] for e in mapped_events)
            logging.info(f"Normalizing timestamps relative to first event at {first_timestamp}")
            
            # Calculate the total duration in seconds from first to last event
            last_timestamp = max(e["timestamp"] for e in mapped_events)
            duration_seconds = last_timestamp - first_timestamp
            logging.info(f"Total timeline duration: {duration_seconds} seconds")
            
            # Calculate duration in days and then in Gource seconds
            duration_days = duration_seconds / (24*60*60)
            gource_duration_seconds = duration_days * seconds_per_day
            logging.info(f"Duration in days: {duration_days:.2f}")
            logging.info(f"Gource duration at {seconds_per_day} seconds per day: {gource_duration_seconds:.2f} seconds")
            
            # Calculate a dynamic scaling factor to keep audio length reasonable
            target_duration_ms = target_duration_seconds * 1000
            logging.info(f"Target audio duration: {target_duration_seconds} seconds")
            
            # Calculate scaling factor based on Gource duration
            scaling_ratio = target_duration_seconds / gource_duration_seconds
            effective_scaling_factor = scaling_ratio / 1000  # Convert to ms scale
            logging.info(f"Using Gource-based scaling with ratio: {scaling_ratio:.4f}")
            logging.info(f"Effective scaling factor: {effective_scaling_factor}")
            
            # Calculate the scaled duration in milliseconds
            scaled_duration_ms = gource_duration_seconds * 1000
            logging.info(f"Scaled audio duration: {scaled_duration_ms:.2f} ms ({scaled_duration_ms/1000:.2f} seconds)")
            
            # Create a silent base audio track with appropriate length
            final_track = AudioSegment.silent(duration=scaled_duration_ms + 1000)  # extra buffer
    except Exception as e:
        logging.error("Failed to create base audio track: %s", e)
        return

    # Keep track of processed events
    processed_count = 0
    error_count = 0
    
    for event in mapped_events:
        # Calculate the placement time in milliseconds (scaled)
        # Normalize the timestamp relative to the first event before scaling
        relative_timestamp = event["timestamp"] - first_timestamp
        place_time = int(relative_timestamp * effective_scaling_factor * 1000)
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
