# GitSymphony: Transform Git History into Musical Visualizations

![GitSymphony Demo](https://img.shields.io/badge/Demo-Scene%20Inspired-blueviolet)

[![GitHub stars](https://img.shields.io/github/stars/PatrickKalkman/gitsymphony)](https://github.com/PatrickKalkman/gitsymphony/stargazers)
[![GitHub contributors](https://img.shields.io/github/contributors/PatrickKalkman/gitsymphony)](https://github.com/PatrickKalkman/gitsymphony/graphs/contributors)
[![GitHub last commit](https://img.shields.io/github/last-commit/PatrickKalkman/gitsymphony)](https://github.com/PatrickKalkman/gitsymphony)
[![open issues](https://img.shields.io/github/issues/PatrickKalkman/gitsymphony)](https://github.com/PatrickKalkman/gitsymphony/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

What if you could see the evolution of AI not as code but as a colorful explosion of human creativity? GitSymphony transforms Git repository history into stunning audiovisual experiences, inspired by the 80s and 90s demo scene.

## 🎵 Overview

GitSymphony turns your Git repositories into musical visualizations that reveal the hidden rhythms and patterns of software development. Watch and hear how projects evolve over time, with each commit transformed into visual elements and sound effects that bring your code's history to life.

## ✨ Key Features

- **Visual Git History**: Transform repositories into mesmerizing visual displays
- **Audio Generation**: Create soundtracks from Git commit patterns
- **Demo Scene Aesthetics**: Retro-inspired visuals reminiscent of the 80s/90s demo scene
- **Customizable**: Adjust visualization parameters and sound mappings
- **Support for Any Repository**: Works with any Git repository
- **Retro "Greetz" Section**: Classic demo scene-style credits

## 🏗️ Architecture

GitSymphony consists of several components:

1. **Git Log Parser**: Extracts commit history from repositories
2. **Event Grouper**: Organizes related commits into meaningful clusters
3. **Audio Mapper**: Maps Git events to sound effects
4. **Visualization Generator**: Creates visual representations using Gource
5. **Audio Processor**: Generates the final soundtrack

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Gource
- FFmpeg
- Sound files (included in the repository)

### Installation

1. **Clone & Navigate**:
```bash
git clone https://github.com/PatrickKalkman/gitsymphony
cd gitsymphony
```

2. **Install Dependencies**:
```bash
uv pip install -r requirements.txt
```

3. **Install Gource and FFmpeg** (if not already installed):
```bash
# For macOS
brew install gource ffmpeg

# For Ubuntu/Debian
sudo apt-get install gource ffmpeg
```

### Usage Examples

```bash
# Process a Git repository and generate visualization with audio
uv run -m src.gitsymphony.gource_audio_mapper process \
  --input /path/to/repo/.git/logs/HEAD \
  --config config.json \
  --output ./output \
  --verbose

# Just generate the audio from an existing Gource log
uv run -m src.gitsymphony.gource_audio_mapper process \
  --input gource.log \
  --config config.json \
  --output ./output \
  --dry-run
```

## ⚙️ Configuration

The `config.json` file controls how GitSymphony processes Git history:

```json
{
    "grouping_window": 15.0,        // Group events within this time window (seconds)
    "min_files": 25,                // Minimum files for a significant event
    "sound_files_folder": "sounds", // Folder containing sound effects
    "target_audio_duration_seconds": 58, // Target duration for output audio
    "seconds_per_day": 0.01,        // Time scaling factor
    "min_sound_gap_seconds": 2.0,   // Minimum gap between sounds
    "mapping_rules": {
        "actions": [
            {
                "pattern": "A",     // Added files
                "sound_file": "swoosh.wav"
            },
            {
                "pattern": "M",     // Modified files
                "sound_file": "explosion3.wav"
            },
            {
                "pattern": "D",     // Deleted files
                "sound_file": "explosion1.wav"
            }
        ]
    }
}
```

## 🎬 Example Visualizations

GitSymphony has been used to visualize the evolution of major AI frameworks:

- **PyTorch**: From quiet beginnings to explosive community growth in 2017
- **TensorFlow**: Google's strategic launch and steady development
- **LangChain**: The rapid rise of LLM connectors since late 2022
- **Hugging Face Transformers**: A shimmering web of collaboration since 2018
- **Scikit-learn**: The foundation of machine learning in Python since 2010

Check out [this Medium article](https://medium.com/generative-ai/watch-5-ai-frameworks-evolve-a-stunning-visual-history-7e7268766a82) for more context and to see videos of these visualizations in action.

## 🛠️ Extending GitSymphony

You can extend GitSymphony by:

1. Adding new sound effects to the `sounds` directory
2. Customizing the mapping rules in `config.json`
3. Implementing new event processing logic in the Python code
4. Creating custom visualization styles with Gource parameters

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🔮 Future Plans

- Support for more visualization styles
- Additional sound mapping options
- Interactive web-based visualizations
- Integration with CI/CD pipelines
- Support for other version control systems

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- The demo scene community for inspiration
- Classic demo scene musicians like Skaven/Future Crew, Elwood, Vincenzo, SunSpire
- The open-source AI community
- All the contributors to the visualized frameworks
- Gource developers for the visualization engine

---

Built with ❤️ by code enthusiasts, for code enthusiasts. Star us on GitHub if you find this useful!
