# Changelog

## [1.2.0] - 2026-06-11

### Added
- `--ver` option: prints the installed PyFish version and exits.
- Automatic column matching for both input tables. Column names are matched case-insensitively, and `Id`/`ChildId` are interchangeable. If the names cannot be matched, columns are assigned by position and the chosen mapping is reported.
- Self-parent roots: a node that lists itself as its own parent in the parent tree is treated as a root.

## [1.1.1] - 2026-04-23

### Fixed
- `--curved` and `--smooth` are now enforced as mutually exclusive in the CLI.
- Passing an invalid `color_by` column name now raises a clear `ValueError`.

## [1.1.0] - 2026-04-15

### Added
- `-V, --curved` option: smooths filled areas using piecewise Hermite interpolation with S-curve transitions. Adds a gray background and centers the plot when population is empty at the first step.
- `-E, --separate` option: places children equidistant from each other within their parent band. By default, children now emerge from the center of the parent.
- Linear interpolation mode: `-I 0` now performs linear interpolation between known data points. Negative values (default) fill missing values with 0.
- Default smooth value changed to `-1` (no smoothing). Negative values disable smoothing explicitly.
- `--curved` and `--smooth` are now mutually exclusive.
- Automatic root creation: if multiple nodes have no parent, or if population IDs are not listed in the parent tree, a synthetic root with zero population is created to parent them all.
- `tests/generate_doc_images.py` script to regenerate all documentation images.

### Fixed
- FutureWarning for pandas `fillna(inplace=True)` on DataFrame slices.

### Changed
- Migrated repository URLs from Bitbucket to GitHub.

## [1.0.3] - Initial tracked version
