# Unreleased — draft

This is an internal staging file, not a Nexus release. Move only confirmed
release changes into `nexus/<version>/changelog.md` after the version is set.
The version label previously proposed as 1.0.4 was reported as a numbering
mistake and is intentionally not used here.

## Added

- Added a Bandit Overhaul settings screen for configuring party limits, base
  party size, respawn intervals, and parties spawned per interval for each
  bandit family.
- Added automatic battle division assignment for companions based on their
  equipment, while preserving manually assigned divisions.
- Added a Camp Hub welcome panel and access to customize the player's armor
  from the hub.
- Added WSE support for restoring custom kingdom troop trees across saves.

## Changed

- Reworked bandit party spawning and party-size adjustment, with configurable
  behavior and diagnostics.
- Updated Camp Hub settings and layout, including a single-column Main Settings
  panel.
- Optimized several strategic-map alarm and hero-AI trigger paths.

## Fixed

- Fixed the siege option to wait until tomorrow being canceled by the automatic
  menu system.
- Fixed autoloot settings being corrupted by custom armor troop-slot
  initialization and improved handling of invalid saved values.
- Fixed custom troop tree save/load restoration for WSE and native saves,
  including load-marker handling and user feedback.
- Fixed equipment handling and companion inventory navigation edge cases.
- Fixed filtering in the All Items browser.
- Fixed native auto-upgrade and Camp Hub opcode errors.
