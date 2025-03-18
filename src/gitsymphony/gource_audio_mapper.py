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


@app.command()
def main(
    input: str = typer.Option(..., help="Path to the Gource log file"),
    config: str = typer.Option(..., help="Path to the JSON configuration file"),
    output: str = typer.Option(..., help="Output directory for logs and WAV file"),
    verbose: bool = typer.Option(False, help="Enable detailed logging"),
    dry_run: bool = typer.Option(False, help="Process log without writing output files"),
):
    # Setup logging
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

    # Load and validate configuration
    try:
        # Handle cases where config might be Ellipsis or OptionInfo
        if config is ...:
            typer.echo("Error: Configuration file path is required")
            raise typer.Exit(1)
        
        # If config is a string, use it directly
        if isinstance(config, str):
            config_path = config
        # Otherwise, it's likely an OptionInfo object with a default
        elif hasattr(config, "default") and config.default is not ...:
            config_path = str(config.default)
        else:
            typer.echo("Error: Invalid configuration file path")
            raise typer.Exit(1)
            
        with open(config_path, "r") as cfg_file:
            cfg = json.load(cfg_file)
    except Exception as e:
        logging.error("Error reading configuration: %s", e)
        raise

    for key in [
        "timeline_scaling_factor",
        "grouping_window",
        "sound_files_folder",
        "mapping_rules",
    ]:
        if key not in cfg:
            logging.error("Missing configuration key: %s", key)
            raise KeyError(f"Missing configuration key: {key}")

    # Process log: parsing, grouping, and mapping
    # Handle cases where parameters might be Ellipsis or OptionInfo
    if input is ...:
        typer.echo("Error: Input file path is required")
        raise typer.Exit(1)
    if output is ...:
        typer.echo("Error: Output directory is required")
        raise typer.Exit(1)
        
    # Process input path
    if isinstance(input, str):
        input_path = input
    elif hasattr(input, "default") and input.default is not ...:
        input_path = str(input.default)
    else:
        typer.echo("Error: Invalid input file path")
        raise typer.Exit(1)
        
    # Process output path
    if isinstance(output, str):
        output_path = output
    elif hasattr(output, "default") and output.default is not ...:
        output_path = str(output.default)
    else:
        typer.echo("Error: Invalid output directory")
        raise typer.Exit(1)

    events = parse_log_file(input_path)
    grouped_events = group_events(events, grouping_window=cfg["grouping_window"])
    mapped_events = map_events(grouped_events, mapping_rules=cfg["mapping_rules"])

    # Write intermediate logs with naming based on input basename and current timestamp:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    grouping_log = f"{output_path}/{input_path.rsplit('/', 1)[-1]}_grouping_{timestamp}.log"
    mapping_log = f"{output_path}/{input_path.rsplit('/', 1)[-1]}_mapping_{timestamp}.log"

    write_intermediate_log(grouped_events, grouping_log)
    write_intermediate_log(mapped_events, mapping_log)  # Use appropriate writer for mapping log

    # Audio processing (only if not a dry run)
    if not dry_run:
        process_audio(
            mapped_events,
            scaling_factor=cfg["timeline_scaling_factor"],
            sound_folder=cfg["sound_files_folder"],
            output=output_path,
            input_basename=input_path.rsplit("/", 1)[-1],
        )


if __name__ == "__main__":
    app()
