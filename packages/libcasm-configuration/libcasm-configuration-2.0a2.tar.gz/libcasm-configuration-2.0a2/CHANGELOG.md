# Changelog

All notable changes to `libcasm-configuration` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.0a2] - 2023-12-11

### Fixed

- Fix bug in irrep decomposition
- Fix comparison of Configuration with equivalent but distinct supercell

### Added

- Added more irrep decomposition, DoF space analysis, and config space analysis tests
- Added options to config_space_analysis and dof_space_analysis methods to specify default occupation mode on a site or sublattice basis
- Added CASM::config::make_dof_space_rep and libcasm.configuration.make_dof_space_rep
- Added libcasm.configuration.ConfigurationWithProperties, and methods for libcasm.configuration.SupercellSymOp to act on ConfigurationWithProperties
- Added site_index_converter and unitcell_index_converter accessors to libcasm.Supercell.
- Added to_structure and from_structure to libcasm.configuration.Configuration and libcasm.configuration.ConfigurationWithProperties for conversions between atomic structures and configuration
- Added more access to matrix reps from PrimSymInfo in libcasm.configuration.Prim
- Added to_index_list, to_index_set, sort, sorted, is_sorted, __rmul__ to libcasm.clusterography.Cluster
- Added make_periodic_equivalence_map, make_periodic_equivalence_map_indices, make_local_equivalence_map, and make_local_equivalence_map_indices to libcasm.clusterography
- Added to_dict and from_dict methods to libcasm.configuration.Prim

### Changed

- Changed libcasm.clusterography.make_prim_periodic_orbits to make_periodic_orbits

### Deprecated

- Deprecated to_json and from_json methods of libcasm.configuration.Prim


## [v2.0a1] - 2023-08-21

This release creates the libcasm-configuration comparison and enumeration module. It includes:

- Classes for representing supercells, configurations, clusters, and occupation events
- Methods for comparing and enumerating unique configurations, clusters, occupation events, and local environments
- Methods for generating orbits of symmetrically equivalent configurations, clusters, and occupation events
- Methods for copying configurations to make sub- or super-configurations
- Methods for generating symmetry groups, and constructing and applying symmetry representations
- Methods for performing irreducible space decompositions and finding symmetry adapted order parameters

This distribution package libcasm-configuration contains several Python packages of use for configuration comparison and enumeration:

- libcasm.sym_info
- libcasm.irreps
- libcasm.clusterography
- libcasm.configuration
- libcasm.occ_events
- libcasm.enumerate

This package may be installed via pip install, using scikit-build, CMake, and pybind11. This release also includes usage examples and API documentation, built using Sphinx.
