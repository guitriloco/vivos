#!/bin/bash

# Deployment script for new Landing Pages
PROJECT_NAME=$1
# Use relative path to boilerplate
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SOURCE_DIR="$SCRIPT_DIR/../boilerplate"
TARGET_DIR="$HOME/$PROJECT_NAME"

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./deploy-lp.sh <project-name>"
    exit 1
fi

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory $SOURCE_DIR not found. Make sure boilerplate is prepared."
    exit 1
fi

echo "Deploying new Landing Page: $PROJECT_NAME..."
mkdir -p "$TARGET_DIR"
cp -r "$SOURCE_DIR"/* "$TARGET_DIR/"

cd "$TARGET_DIR"
echo "Initializing repository..."
git init
git add .
git commit -m "Initial deploy for $PROJECT_NAME"

echo "New Landing Page project created at $TARGET_DIR"
echo "To start development:"
echo "cd $TARGET_DIR && npm install && npm run dev"
