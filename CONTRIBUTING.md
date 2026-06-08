# Contributing to Code with Claude

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Version Control Workflow

### Tracking Changes

All changes should be tracked with timestamps. Use the provided scripts:

1. **Track a change:**
   ```bash
   ./scripts/track_changes.sh "Description of your change"
   ```

2. **View version history:**
   ```bash
   ./scripts/show_changes.sh
   ```

3. **View specific version:**
   ```bash
   ./scripts/show_changes.sh 0.1.0
   ```

### Versioning

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for adding functionality in a backwards-compatible manner
- **PATCH** version for backwards-compatible bug fixes

To bump the version:
```bash
./scripts/version.sh [major|minor|patch]
```

### Commit Messages

Write clear, descriptive commit messages. The tracking script will automatically add timestamps.

Example:
```
Added user authentication feature

Timestamp: 2026-06-08 14:30:00
```

## Development Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and track them:
   ```bash
   ./scripts/track_changes.sh "Description of changes"
   ```

3. **Update documentation** if needed:
   - Update CHANGELOG.md with your changes
   - Update README.md if adding new features
   - Update CLAUDE.md if changing project structure

4. **Submit a pull request** with a clear description of your changes.

## Code Style

- Follow PEP 8 guidelines for Python code
- Write docstrings for all public functions and classes
- Include type hints where appropriate
- Write tests for new functionality

## Questions?

If you have questions about contributing, please open an issue in the repository.
