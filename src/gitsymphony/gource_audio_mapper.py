import json
import logging
from datetime import datetime

import typer

from gitsymphony.audio_processing import process_audio
from gitsymphony.grouping import group_events
from gitsymphony.mapping import map_events
from gitsymphony.parser import parse_log_file

app = typer.Typer()


def write_intermediate_log(data, filepath: str):
    with open(filepath, "w") as f:
        for entry in data:
            # For grouping log: timestamp, user, file_count, action; for mapping log: add sound_file if present
            line = f"{entry['timestamp']} | {entry['user']} | {entry['action']} | {entry.get('file_count', '?')}"
            if "sound_file" in entry:
                line += f" | {entry['sound_file']}"
            f.write(line + "\n")
    logging.info("Intermediate log written: %s", filepath)


def main():
    """Process a Gource log file and generate audio based on git events."""
    app_inner = typer.Typer()
    
    @app_inner.command()
    def process(
        input: str = typer.Argument(..., help="Path to the Gource log file"),
        config: str = typer.Argument(..., help="Path to the JSON configuration file"),
        output: str = typer.Argument(..., help="Output directory for logs and WAV file"),
        verbose: bool = typer.Option(False, help="Enable detailed logging"),
        dry_run: bool = typer.Option(False, help="Process log without writing output files"),
    ):
        # Setup logging
        log_level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

        # Load and validate configuration
        try:
            with open(config, "r") as cfg_file:
                cfg = json.load(cfg_file)
        except Exception as e:
            logging.error("Error reading configuration: %s", e)
            raise

        for key in [
            "grouping_window",
            "sound_files_folder",
            "mapping_rules",
        ]:
            if key not in cfg:
                logging.error("Missing configuration key: %s", key)
                raise KeyError(f"Missing configuration key: {key}")

        # Process log: parsing, grouping, and mapping
        events = parse_log_file(input)
        min_files = cfg.get("min_files", 4)  # Default to 4 if not specified
        min_sound_gap = cfg.get("min_sound_gap_seconds", None)  # Get the minimum gap between sounds
        grouped_events = group_events(events, grouping_window=cfg["grouping_window"], min_files=min_files)
        mapped_events = map_events(
            grouped_events, 
            mapping_rules=cfg["mapping_rules"],
            min_sound_gap_seconds=min_sound_gap
        )

        # Write intermediate logs with naming based on input basename and current timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        grouping_log = f"{output}/{input.rsplit('/', 1)[-1]}_grouping_{timestamp}.log"
        mapping_log = f"{output}/{input.rsplit('/', 1)[-1]}_mapping_{timestamp}.log"

        write_intermediate_log(grouped_events, grouping_log)
        write_intermediate_log(mapped_events, mapping_log)  # Use appropriate writer for mapping log

        # Audio processing (only if not a dry run)
        if not dry_run:
            # Get target duration and seconds per day from config or use defaults
            target_duration = cfg.get("target_audio_duration_seconds", 60)
            seconds_per_day = cfg.get("seconds_per_day", 0.01)
            process_audio(
                mapped_events,
                sound_folder=cfg["sound_files_folder"],
                output=output,
                input_basename=input.rsplit("/", 1)[-1],
                target_duration_seconds=target_duration,
                seconds_per_day=seconds_per_day,
            )


    return app_inner()

if __name__ == "__main__":
    main()
