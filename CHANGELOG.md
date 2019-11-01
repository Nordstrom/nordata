# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.3] - 2019-11-01
### Fixed
- Bumped urllib3 from 1.24.1 to 1.24.2

## [0.2.2] - 2019-02-25
### Fixed
- Improved error messages for Redshift functions

## [0.2.1] - 2019-01-02
### Fixed
- Corrected `README.md` and docstring for `s3_download()`

## [0.2.0] - 2019-01-02
### Added
- Informative error message for the env_var argument in the `redshift_execute()` and `redshift_get_conn()` functions
- A `boto_get_creds()` function was created to allow the user to obtain credentials strings for purposes such as `COPY` and `UNLOAD` SQL statements
- Version documentation in the `CHANGELOG.md` file
### Changed
- The `create_session()` function was renamed to `boto_create_session()` to highlight that the session object can be used to access a wide variety of AWS tools

## [0.1.1] - 2018-12-14
### Fixed
- Docstrings and `README.md` documentation for S3 functions

## [0.1] - 2018-12-11
- Initial release
