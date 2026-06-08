#!/bin/bash
# Show latest changes for each version
# Usage: ./scripts/show_changes.sh [version]

set -e

CHANGELOG_FILE="CHANGELOG.md"

if [ -n "$1" ]; then
    # Show specific version
    VERSION="$1"
    echo "Changes for version $VERSION:"
    echo "=============================="
    sed -n "/## \[$VERSION\]/,/^## \[/p" "$CHANGELOG_FILE" | head -n -1
else
    # Show all versions
    echo "Version History:"
    echo "================"
    grep -E "^## \[" "$CHANGELOG_FILE" | while read -r line; do
        VERSION=$(echo "$line" | sed 's/## \[\(.*\)\].*/\1/')
        echo ""
        echo "Version $VERSION:"
        echo "----------------"
        sed -n "/## \[$VERSION\]/,/^## \[/p" "$CHANGELOG_FILE" | head -n -1
    done
fi
