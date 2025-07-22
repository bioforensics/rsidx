# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [0.3.1] 2025-07-22
- Upgraded vendored code for Python 3.12+ compatibility (#9)


## [0.3] 2022-04-08

### Added
- New `--file` flag to enable search using a file of rsIDs (#7)


## [0.2] 2020-04-21

### Added
- Added support for multiple rsIDs in the VCF ID column
- Added support for rsIDs appearing in multiple records (forbidden by VCF spec but used in some popularpopulation survey data)
- Configured continuous integration (CI) with GitHub actions

### Changed
- Changed `rsidx index` so that it now fails if index already exists; provided a `--force` flag to override


## [0.1.1] 2019-05-21

Bugfix release with updated file manifest.


## [0.1] 2019-05-21

Initial release!

- Command-line entry point: `rsidx`
- Command-line operations:
    - `rsidx index`: index a VCF file
    - `rsidx search`: query a VCF file by rsID
