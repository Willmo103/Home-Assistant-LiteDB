# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial release of Home-Assistant LiteDB with functionalities to:
  - Fetch entities from Home Assistant and save them to a SQLite database.
  - Purge the database and recreate it.
  - Display the last 50 rows of logs.
  - Configurable polling interval.
  - Logging to file and/or console.

## [0.1.0] - 2024-08-04

### Added

- Renamed the project to `Home-Assistant LiteDB`.
- Added unit tests for all major functionalities.
- Created a GitHub Actions workflow for automated testing.
- Packaged the project for distribution via pip.
- Initial release of Home-Assistant LiteDB.

### Changed

- Updated README.md to reflect the new project name and usage instructions.

### Fixed

- Fixed timestamp logging issue in unit tests by using regex pattern matching.

### Deprecated

- N/A

### Removed

- N/A

### Security

- N/A
