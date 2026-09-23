# 🐦‍⬛ Raven's Rummager

A small Discord bot runner for Raven's Sanctuary that checks the THGL Palia Rummage Pile page and posts an update in the configured Discord channel.

## GitHub setup

1. Create a new GitHub repository.
2. Upload all files from this folder.
3. Open **Settings → Secrets and variables → Actions**.
4. Add these **Repository secrets**:
   - `DISCORD_TOKEN` = your Discord bot token
   - `CHANNEL_ID` = the ID of `#rummage-piles`
5. Open **Actions** and run **Raven's Rummager** manually once.

### Never put the Discord token in the code or README.

If the Discord token has ever been exposed publicly, regenerate it in the Discord Developer Portal.

## Important

THGL's Rummage page is a live web page and its internal data structure can change. This starter version deliberately links to the live tracker rather than pretending a private/undocumented API exists.

The next refinement is to parse the four location cards directly once the live page DOM/API response is confirmed in the GitHub runner.
