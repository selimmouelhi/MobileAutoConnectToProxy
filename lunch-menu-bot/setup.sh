#!/bin/bash
# Setup script for Lunch Menu Slack Bot

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Setting up Lunch Menu Bot..."

# Create virtual environment
python3 -m venv "$SCRIPT_DIR/.venv"
source "$SCRIPT_DIR/.venv/bin/activate"

# Install dependencies
pip install -r "$SCRIPT_DIR/requirements.txt"

# Create logs directory
mkdir -p "$SCRIPT_DIR/logs"

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Create a .env file (copy from .env.example) and fill in your credentials"
echo "  2. Test with: source .venv/bin/activate && OG_PASSWORD=xxx SLACK_WEBHOOK_URL=xxx python lunch_menu_slack.py --dry-run"
echo "  3. To schedule for every Monday at 8 AM:"
echo "     - Edit com.lunch-menu-bot.plist and replace REPLACE_WITH_YOUR_PASSWORD and REPLACE_WITH_YOUR_WEBHOOK_URL"
echo "     - cp com.lunch-menu-bot.plist ~/Library/LaunchAgents/"
echo "     - launchctl load ~/Library/LaunchAgents/com.lunch-menu-bot.plist"
echo ""
echo "  To unload: launchctl unload ~/Library/LaunchAgents/com.lunch-menu-bot.plist"
echo "  To test manually: launchctl start com.lunch-menu-bot"
