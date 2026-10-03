# Zashboard Config

Personal configuration backup for [Zashboard](https://github.com/Zephyruso/zashboard).

## Usage

Import this URL in Zashboard:

```text
https://raw.githubusercontent.com/zzpice/zashboard-config/main/zashboard-settings.json
```

Then enable:

- Import settings from URL
- Auto import settings from URL

## Update

When Zashboard settings are changed:

1. Export settings from Zashboard.
2. Replace `zashboard-settings.json` in this repository.
3. Commit the change.
4. Other devices will load the latest configuration automatically.

## Notes

This repository contains Zashboard UI settings only.

Do not upload:

- sing-box server configuration
- Reality private keys
- UUIDs
- API secrets
- SSH credentials
- subscription URLs containing tokens

## Current preferences

- Font: MiSans
- Emoji: noto-color-emoji
- Base font size: 17.5px
- Automatic light/dark theme switching
- Custom proxy-group icons
- Source IP device labels
