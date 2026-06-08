# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CHANGELOG.md for version history tracking
- VERSION file for version management
- Version management scripts (version.sh, track_changes.sh, show_changes.sh)
- Contributing guidelines (CONTRIBUTING.md)
- MIT License (Copyright 2026 k4z0)
- README.md with project documentation
- requirements.txt with pandas and openpyxl dependencies
- GitHub setup script (setup_github.sh)
- Order Analysis Agent (order_agent_simple.py)
  - Analyzes Delivery TAT from Excel files
  - Identifies delayed orders (>3 days TAT)
  - Gathers user feedback for each delayed order
  - Learns from feedback and remembers successful actions
  - Provides guidance based on learned actions
  - Generates comprehensive analysis reports
- Agent configuration file (config.py)
- Agent documentation (ORDER_AGENT_README.md)
- Test file (test_agent.py)
- Run scripts (run_agent.bat, run_agent.sh)

### Changed
- Initial project setup with full structure (2026-06-08 18:45:00)
- Git repository initialization (2026-06-08 18:45:00)
- Basic project structure setup (2026-06-08 18:45:00)
- CLAUDE.md documentation created (2026-06-08 18:45:00)
- Git configuration with user email (k4z0@outlook.com) (2026-06-08 18:45:00)
- Updated README.md with GitHub repository URL (2026-06-08 18:50:00)
- Installed pandas and openpyxl dependencies (2026-06-08 19:15:00)

## [0.1.0] - 2026-06-08

### Added
- Project initialization (2026-06-08 14:09:00)
- Virtual environment setup (2026-06-08 14:09:00)
- IDE configuration (2026-06-08 14:59:00)
