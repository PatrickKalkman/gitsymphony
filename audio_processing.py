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
    # Create a silent base audio track; length can be computed based on max scaled timestamp.
    max_time = (
        max(e["timestamp"] for e in mapped_events) * scaling_factor * 1000
    )  # in ms
    final_track = AudioSegment.silent(duration=max_time + 1000)  # extra buffer

    for event in mapped_events:
        # Calculate the placement time in milliseconds (scaled)
        place_time = int(event["timestamp"] * scaling_factor * 1000)
        sound_path = f"{sound_folder}/{event['sound_file']}"

        try:
            clip = AudioSegment.from_wav(sound_path)
        except Exception as e:
            logging.error("Could not load sound file '%s': %s", sound_path, e)
            continue

        # Overlay the sound clip
        final_track = final_track.overlay(clip, position=place_time)

    # Define final audio filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_audio_name = f"{output}/{input_basename}_soundtrack_{timestamp}.wav"

    final_track.export(final_audio_name, format="wav")
    logging.info("Final audio file created: %s", final_audio_name)
