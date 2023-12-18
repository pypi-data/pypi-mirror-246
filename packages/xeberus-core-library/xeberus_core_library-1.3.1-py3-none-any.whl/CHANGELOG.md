# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.1] - 2023-12-17
### Changed
- Rename the attribute "event_ref" with "event_id"

## [1.2.11] - 2022-12-23
### Changed
- Migrate to Poetry

## [1.2.10] - 2022-05-13
### Added
- Add the attribute `event_ref` to the battery state update and location update events
- Add the attribute `event_time` to the location update events

## [1.2.2] - 2022-05-10
### Changed
- Update the parameters of the constructor of the class `LocationUpdate`

## [1.2.1] - 2022-05-08
### Changed
- Replace package `majormode.xeberus.tracker` with `majormode.xeberus.device`
- Remove the attribute `event_id` from the class `BatteryStateChangeEvent`

## [1.1.0] - 2020-11-13
### Changed
- Replace package `majormode.perseus` with `marjomode.xeberus`
