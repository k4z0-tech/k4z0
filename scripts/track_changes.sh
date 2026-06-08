#!/bin/bash
# Track changes with timestamps
# Usage: ./scripts/track_changes.sh [commit_message]

set -e

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
DATE=$(date "+%Y-%m-%d")

# Get the commit message
if [ -z "$1" ]; then
    echo "Usage: $0 <commit_message>"
    exit 1
fi

COMMIT_MSG="$1"

# Add timestamp to commit message
FULL_MSG="$COMMIT_MSG

Timestamp: $TIMESTAMP"

# Stage all changes
git add .

# Commit with timestamp
git commit -m "$FULL_MSG"

# Update CHANGELOG.md
echo ""
echo "Updating CHANGELOG.md..."
echo ""

# Read current version
VERSION=$(cat VERSION | tr -d '[:space:]')

# Add entry to CHANGELOG
sed -i "/## \[Unreleased\]/a\\
\\
### Changed\\
- $COMMIT_MSG ($TIMESTAMP)" CHANGELOG.md

echo "Changes tracked and committed."
echo "Version: $VERSION"
echo "Timestamp: $TIMESTAMP"
