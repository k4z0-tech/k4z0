# Code with Claude

A Python project for learning and experimenting with Claude AI.

## Features

### Order Analysis Agent

An intelligent agent that analyzes order delivery delays, gathers feedback, and learns from past actions.

**Key Features:**
- Analyzes Delivery TAT from Excel files
- Identifies delayed orders (TAT > 3 days)
- Gathers user feedback for each delayed order
- Learns from feedback and remembers successful actions
- Provides guidance based on learned actions
- Generates comprehensive analysis reports

**Quick Start:**
```bash
# Windows
run_agent.bat

# Unix/Mac
./run_agent.sh
```

For more details, see [ORDER_AGENT_README.md](ORDER_AGENT_README.md)

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/k4z0-tech/k4z0.git
   cd k4z0
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Unix/Mac
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
k4z0/
├── .venv/                  # Virtual environment
├── .gitignore              # Git ignore rules
├── CHANGELOG.md            # Version history with timestamps
├── CLAUDE.md               # Claude Code guidance
├── CONTRIBUTING.md         # Contributing guidelines
├── LICENSE                 # MIT License
├── ORDER_AGENT_README.md   # Order agent documentation
├── README.md               # This file
├── VERSION                 # Current version
├── order_train_data.xlsx   # Order data file
├── requirements.txt        # Dependencies
├── run_agent.bat           # Windows run script
├── run_agent.sh            # Unix/Mac run script
├── scripts/                # Version management scripts
├── src/                    # Source code
│   ├── order_agent.py      # Main agent (with emojis)
│   ├── order_agent_simple.py  # Windows-compatible agent
│   └── config.py           # Configuration
└── tests/                  # Tests
```

## Versioning

This project follows [Semantic Versioning](https://semver.org/). See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
