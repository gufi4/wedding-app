# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based Telegram bot for wedding-related purposes. The project is in early development stages.

## Environment Setup

The bot uses a Telegram API token stored in `.env`:
```python
API_TOKEN = "8391694362:AAE5hEbiYqmKH_67HxnyALV5JPfXb_OcuiI"
```

**Security**: The `.env` file contains sensitive credentials. Ensure it is added to `.gitignore` before committing to version control.

## Running the Bot

Since this project is in early development, there are no established build commands yet. Typical Python bot development would involve:

```bash
# Install dependencies (when requirements.txt is created)
pip install -r requirements.txt

# Run the bot
python main.py
```

## Code Architecture

The project is currently minimal:
- `main.py` - Entry point (currently empty)
- `.env` - Environment configuration with Telegram API token

As development progresses, a typical Telegram bot architecture may include:
- Handler functions for different commands and message types
- Conversation flow management for user interactions
- Database integration for storing wedding-related data
- Utility modules for common functionality

## Development Notes

- This is not currently a git repository - consider initializing one for version control
- No package management file (requirements.txt, pyproject.toml) exists yet
- No testing framework is configured
- No linting or formatting tools are set up
