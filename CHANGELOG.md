# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2022-03-28

### Added
- Button support to hide the top banner and allow 4 trains
- Button support to switch between alternating groups, showing two groups, or one at a time
- Heading.bdf font (small height for the banner)

### Changed

- Use main.py instead of code.py
- Moved personal information into secrets.py, because it reduces the chance I accidentally upload a config.py with API keys

- Forked from u/erikrrodriguez, who included:
    - Walking distance modifier
    - Updated to CircutPython 8
    - Incorporated u/scottiecarcia's off-hours and Metrohero API
    - Incorporated u/ScottKekoaShay's auto-swapping of stations
- Also stole u/GJT-34's Metroesque.bdf font
- All based on u/dc-metro's original work
