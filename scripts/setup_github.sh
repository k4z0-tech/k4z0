#!/bin/bash
# Setup GitHub repository
# Usage: ./scripts/setup_github.sh [repository_name]

set -e

REPO_NAME="${1:-code_with_claude}"

echo "Setting up GitHub repository: $REPO_NAME"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI (gh) is not installed."
    echo ""
    echo "Please install it from: https://cli.github.com/"
    echo ""
    echo "After installation, run:"
    echo "  gh auth login"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "Please authenticate with GitHub first:"
    echo "  gh auth login"
    exit 1
fi

# Create repository
echo "Creating repository..."
gh repo create "$REPO_NAME" --public --description "A Python project for learning and experimenting with Claude AI" --source=. --remote=origin --push

echo ""
echo "Repository created successfully!"
echo "URL: https://github.com/$(gh api user --jq .login)/$REPO_NAME"
echo ""
echo "Next steps:"
echo "1. Update README.md with your GitHub username"
echo "2. Update LICENSE with your name"
echo "3. Start coding!"
