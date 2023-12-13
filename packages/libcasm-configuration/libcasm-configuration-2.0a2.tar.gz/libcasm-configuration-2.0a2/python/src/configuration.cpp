#include <pybind11/eigen.h>
#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// nlohmann::json binding
#define JSON_USE_IMPLICIT_CONVERSIONS 0
#include "casm/casm_io/Log.hh"
#include "casm/casm_io/json/InputParser_impl.hh"
#include "casm/casm_io/json/jsonParser.hh"
#include "casm/clexulator/ConfigDoFValuesTools_impl.hh"
#include "casm/configuration/ConfigCompare.hh"
#include "casm/configuration/ConfigurationSet.hh"
#include "casm/configuration/FromStructure.hh"
#include "casm/configuration/Prim.hh"
#include "casm/configuration/Supercell.hh"
#include "casm/configuration/SupercellSet.hh"
#include "casm/configuration/SupercellSymInfo.hh"
#include "casm/configuration/SupercellSymOp.hh"
#include "casm/configuration/canonical_form.hh"
#include "casm/configuration/config_space_analysis.hh"
#include "casm/configuration/copy_configuration.hh"
#include "casm/configuration/dof_space_analysis.hh"
#include "casm/configuration/io/json/Configuration_json_io.hh"
#include "casm/configuration/io/json/Supercell_json_io.hh"
#include "casm/configuration/irreps/VectorSpaceSymReport.hh"
#include "casm/configuration/make_simple_structure.hh"
#include "casm/crystallography/SimpleStructure.hh"
#include "casm/crystallography/UnitCellCoord.hh"
#include "casm/crystallography/io/BasicStructureIO.hh"
#include "pybind11_json/pybind11_json.hpp"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

/// CASM - Python binding code
namespace CASMpy {

using namespace CASM;

// // SymGroup
//
// std::shared_ptr<config::SymGroup> make_symgroup(
//     std::vector<xtal::SymOp> const &element,
//     group::MultiplicationTable const &multiplication_table) {
//   return std::make_shared<config::SymGroup>(element, multiplication_table);
// }
//
// std::shared_ptr<config::SymGroup> make_symgroup_subgroup(
//     std::shared_ptr<config::SymGroup const> const &head_group,
//     std::set<Index> const &head_group_index,
//     std::optional<std::vector<xtal::SymOp>> element = std::nullopt) {
//   if (!element.has_value()) {
//     return std::make_shared<config::SymGroup>(head_group, head_group_index);
//   }
//   return std::make_shared<config::SymGroup>(head_group, *element,
//                                             head_group_index);
// }

// Prim

std::shared_ptr<config::Prim> make_prim(
    std::shared_ptr<xtal::BasicStructure const> const &xtal_prim) {
  std::shared_ptr<xtal::BasicStructure const> basicstructure(xtal_prim);
  std::map<DoFKey, xtal::DoFSet> global_dof_info(
      clexulator::make_global_dof_info(*basicstructure));
  std::map<DoFKey, std::vector<xtal::SiteDoFSet>> local_dof_info(
      clexulator::make_local_dof_info(*basicstructure));
  config::PrimSymInfo sym_info(*basicstructure);
  return std::make_shared<config::Prim>(xtal_prim);
}

/// \brief Construct config::Prim from JSON string
std::shared_ptr<config::Prim> prim_from_json(std::string const &prim_json_str,
                                             double xtal_tol) {
  PyErr_WarnEx(PyExc_DeprecationWarning,
               "libcasm.configuration.Prim.from_json() is deprecated. Use "
               "libcasm.configuration.Prim.from_dict() instead.",
               2);

  jsonParser json = jsonParser::parse(prim_json_str);
  ParsingDictionary<AnisoValTraits> const *aniso_val_dict = nullptr;
  auto basicstructure = std::make_shared<xtal::BasicStructure>(
      read_prim(json, xtal_tol, aniso_val_dict));
  return std::make_shared<config::Prim>(basicstructure);
}

/// \brief Format xtal::BasicStructure as JSON string
std::string prim_to_json(std::shared_ptr<config::Prim const> const &prim) {
  PyErr_WarnEx(PyExc_DeprecationWarning,
               "libcasm.configuration.Prim.to_json() is deprecated. Use "
               "libcasm.configuration.Prim.to_dict() instead.",
               2);

  jsonParser json;
  write_prim(*prim->basicstructure, json, FRAC);
  std::stringstream ss;
  ss << json;
  return ss.str();
}

// Supercell
std::shared_ptr<config::Supercell> make_supercell(
    std::shared_ptr<config::Prim const> const &prim,
    Eigen::Matrix3l const &transformation_matrix_to_super,
    Index max_n_translation_permutations) {
  return std::make_shared<config::Supercell>(
      prim, transformation_matrix_to_super, max_n_translation_permutations);
}

// SupercellSymOp
config::SupercellSymOp make_supercell_symop(
    std::shared_ptr<config::Supercell> const &supercell,
    Index supercell_factor_group_index, std::optional<Index> translation_index,
    std::optional<Eigen::Vector3l> translation_frac,
    std::optional<Eigen::Vector3d> translation_cart) {
  if (translation_index.has_value()) {
    return config::SupercellSymOp(supercell, supercell_factor_group_index,
                                  *translation_index);
  } else if (translation_frac.has_value()) {
    xtal::UnitCell _translation_frac(*translation_frac);
    return config::SupercellSymOp(supercell, supercell_factor_group_index,
                                  _translation_frac);
  } else if (translation_cart.has_value()) {
    return config::SupercellSymOp(supercell, supercell_factor_group_index,
                                  *translation_cart);
  } else {
    throw std::runtime_error(
        "Error constructing SupercellSymOp: one of translation_index, "
        "translation_frac, or translation_cart must be provided");
  }
}

config::ConfigSpaceAnalysisResults make_ConfigSpaceAnalysisResults(
    clexulator::DoFSpace const &_standard_dof_space,
    std::map<std::string, std::vector<Eigen::VectorXd>> _equivalent_dof_values,
    std::map<std::string, std::vector<config::Configuration>>
        _equivalent_configurations,
    Eigen::MatrixXd const &_projector, Eigen::VectorXd const &_eigenvalues,
    clexulator::DoFSpace const &_symmetry_adapted_dof_space) {
  return config::ConfigSpaceAnalysisResults(
      _standard_dof_space, _equivalent_dof_values, _equivalent_configurations,
      _projector, _eigenvalues, _symmetry_adapted_dof_space);
}

}  // namespace CASMpy

PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);

PYBIND11_MODULE(_configuration, m) {
  using namespace CASMpy;

  m.doc() = R"pbdoc(
        Configuration comparison and enumeration

        libcasm.configuration
        ---------------------

        The libcasm.configuration package contains data structures and methods
        for representing configurations, applying symmetry to configurations,
        and comparing configurations.

    )pbdoc";
  py::module::import("libcasm.xtal");
  py::module::import("libcasm.clexulator");
  py::module::import("libcasm.irreps");
  py::module::import("libcasm.sym_info");

  py::class_<config::Prim, std::shared_ptr<config::Prim>>(m, "Prim", R"pbdoc(
      A data structure that includes a shared `libcasm.xtal.Prim` specifying the
      parent crystal structure and allowed degrees of freedom (DoF),
      along with the symmetry representations needed for applying symmetry to
      `libcasm.configuration.Configuration`.

      )pbdoc")
      .def(py::init(&make_prim), py::arg("xtal_prim"),
           R"pbdoc(

      .. _prim-init:

      Parameters
      ----------
      xtal_prim : libcasm.xtal.Prim
          A :class:`~libcasm.xtal.Prim`
      )pbdoc")
      .def(
          "xtal_prim",
          [](std::shared_ptr<config::Prim const> const &prim) {
            return prim->basicstructure;
          },
          "Returns the internal shared :class:`~libcasm.xtal.Prim`")
      .def(
          "factor_group",
          [](std::shared_ptr<config::Prim const> const &prim) {
            return prim->sym_info.factor_group;
          },
          "Returns the factor group.")
      .def(
          "crystal_point_group",
          [](std::shared_ptr<config::Prim const> const &prim) {
            return prim->sym_info.point_group;
          },
          "Returns the crystal point group.")
      .def(
          "has_occupation_dofs",
          [](std::shared_ptr<config::Prim const> const &prim) {
            return prim->sym_info.has_occupation_dofs;
          },
          R"pbdoc(
          Returns True if >1 occupant allowed on any sublattice, False otherwise.
          )pbdoc")
      .def(
          "has_anisotropic_occupants",
          [](std::shared_ptr<config::Prim const> const &prim) {
            return prim->sym_info.has_aniso_occs;
          },
          R"pbdoc(
          Returns True if any permutation in :func:`Prim.occ_symgroup_rep` is
          non-trivial, False otherwise.
          )pbdoc")
      .def(
          "global_dof_basis",
          [](std::shared_ptr<config::Prim const> const &prim, std::string key) {
            return prim->global_dof_info.at(key).basis();
          },
          "Returns the prim DoF basis matrix, `B`, for global DoF values of "
          "type `key`. The basis matrix converts from DoF values in the prim "
          "basis, `x_prim`, to DoF values in the standard basis, `x_standard`, "
          "according to `x_standard = B @ x_prim`.")
      .def(
          "global_dof_basis_inv",
          [](std::shared_ptr<config::Prim const> const &prim, std::string key,
             Index b) { return prim->global_dof_info.at(key).inv_basis(); },
          "Returns the prim DoF basis matrix inverse, `B_inv`, for local DoF "
          "values of type `key` on sublattice `b`. The basis matrix inverse "
          "converts from DoF values in the standard basis, `x_standard`, to "
          "DoF values in the prim basis, `x_prim`, according to `x_prim = "
          "B_inv @ x_standard`.")
      .def(
          "local_dof_basis",
          [](std::shared_ptr<config::Prim const> const &prim, std::string key,
             Index b) {
            auto const &dof_info = prim->local_dof_info.at(key);
            return dof_info[b].basis();
          },
          "Returns the prim DoF basis matrix, `B`, for local DoF values of "
          "type `key` on sublattice `b`. The basis matrix converts from DoF "
          "values in the prim basis, `x_prim`, to DoF values in the standard "
          "basis, `x_standard`, according to `x_standard = B @ x_prim`.")
      .def(
          "local_dof_basis_inv",
          [](std::shared_ptr<config::Prim const> const &prim, std::string key,
             Index b) {
            auto const &dof_info = prim->local_dof_info.at(key);
            return dof_info[b].inv_basis();
          },
          "Returns the prim DoF basis matrix inverse, `B_inv`, for local DoF "
          "values of type `key` on sublattice `b`. The basis matrix inverse "
          "converts from DoF values in the standard basis, `x_standard`, to "
          "DoF values in the prim basis, `x_prim`, according to `x_prim = "
          "B_inv @ x_standard`.")
      .def(
          "integral_site_coordinate_symgroup_rep",
          [](std::shared_ptr<config::Prim const> const &prim) {
            return prim->sym_info.unitcellcoord_symgroup_rep;
          },
          "Returns the symmetry group representation that describes how "
          "IntegralSiteCoordinate transform under symmetry.")
      .def(
          "occ_symgroup_rep",
          [](std::shared_ptr<config::Prim const> const &prim) {
            return prim->sym_info.occ_symgroup_rep;
          },
          "Returns the symmetry group representation that describes how "
          "occupant indices transform under symmetry.")
      .def(
          "atom_position_symgroup_rep",
          [](std::shared_ptr<config::Prim const> const &prim) {
            return prim->sym_info.atom_position_symgroup_rep;
          },
          "Returns the symmetry group representation that describes how atom "
          "position indices transform under symmetry.")
      .def(
          "local_dof_matrix_rep",
          [](std::shared_ptr<config::Prim const> const &prim, std::string key) {
            return prim->sym_info.local_dof_symgroup_rep.at(key);
          },
          R"pbdoc(
          Returns the symmetry group representation that describes how local "
          continuous DoF transform under symmetry.

          Notes
          -----

          - For each factor group element there is one matrix representation per
            sublattice
          - Local DoF values transform using these symrep matrices *before*
            permuting among sites.
          - If ``has_occupation_dofs() is True``, a matrix rep for transforming
            occupation indicator variables is included with key "occ".


          Parameters
          ----------
          key: str
              Specifies the type of DoF

          Returns
          -------
          local_dof_matrix_rep: list[list[numpy.ndarray[numpy.float64[m,m]]]]
              The array ``local_dof_matrix_rep[factor_group_index][sublattice_index]``
              is the matrix representation for transforming values of DoF `key`, in the
              prim basis, on `sublattice_index`-th sublattice, by the
              `factor_group_index`-th prim factor group operation.

              Note that it is possible for the matrices associated with different
              sublattices to be different sizes, including size zero, depending on the
              corresponding :class:`~libcasm.xtal.DoFSetBasis`.
          )pbdoc",
          py::arg("key"))
      .def(
          "global_dof_matrix_rep",
          [](std::shared_ptr<config::Prim const> const &prim, std::string key) {
            return prim->sym_info.global_dof_symgroup_rep.at(key);
          },
          R"pbdoc(
          Returns the symmetry group representation that describes how global "
          continuous DoF transform under symmetry.

          Notes
          -----

          - For each factor group element there is one matrix representation


          Parameters
          ----------
          key: str
              Specifies the type of DoF

          Returns
          -------
          global_dof_matrix_rep: list[numpy.ndarray[numpy.float64[m,m]]]
              The array ``global_dof_matrix_rep[factor_group_index]``
              is the matrix representation for transforming values of DoF `key`, in the
              prim basis, by the `factor_group_index`-th prim factor group operation.
          )pbdoc",
          py::arg("key"))
      .def_static(
          "from_dict",
          [](const nlohmann::json &data, double xtal_tol) {
            jsonParser json{data};
            ParsingDictionary<AnisoValTraits> const *aniso_val_dict = nullptr;
            return std::make_shared<config::Prim>(
                std::make_shared<xtal::BasicStructure>(
                    read_prim(json, xtal_tol, aniso_val_dict)));
          },
          R"pbdoc(
          Construct a Prim from a Python dict.

          The
          `Prim reference <https://prisms-center.github.io/CASMcode_docs/formats/casm/crystallography/BasicStructure/>`_
          documents the expected format.
          )pbdoc",
          py::arg("data"), py::arg("xtal_tol") = TOL)
      .def(
          "to_dict",
          [](std::shared_ptr<config::Prim const> const &prim, bool frac,
             bool include_va) {
            jsonParser json;
            COORD_TYPE mode = frac ? FRAC : CART;
            write_prim(*prim->basicstructure, json, mode, include_va);
            return static_cast<nlohmann::json>(json);
          },
          py::arg("frac") = true, py::arg("include_va") = false,
          R"pbdoc(
          Represent the Prim as a Python dict

          Parameters
          ----------
          frac : boolean, default=True
              By default, basis site positions are written in fractional
              coordinates relative to the lattice vectors. If False, write basis site
              positions in Cartesian coordinates.
          include_va : boolean, default=False
              If a basis site only allows vacancies, it is not printed by default.
              If this is True, basis sites with only vacancies will be included.

          Returns
          -------
          data : json
              The `Prim reference <https://prisms-center.github.io/CASMcode_docs/formats/casm/crystallography/BasicStructure/>`_ documents the expected format.

          )pbdoc")
      .def_static("from_json", &prim_from_json,
                  R"pbdoc(
          Construct a Prim from a JSON-formatted string.

          .. deprecated:: 2.0a2
                Use :func:`libcasm.from_dict()` instead.

          The
          `Prim reference <https://prisms-center.github.io/CASMcode_docs/formats/casm/crystallography/BasicStructure/>`_
          documents the expected format.
          )pbdoc",
                  py::arg("prim_json_str"), py::arg("xtal_tol") = TOL)
      .def("to_json", &prim_to_json, R"pbdoc(
          Represent the Prim as a JSON-formatted string.

          .. deprecated:: 2.0a2
                Use ``prim.to_dict()`` instead.

          The
          `Prim reference <https://prisms-center.github.io/CASMcode_docs/formats/casm/crystallography/BasicStructure/>`_
          documents the expected format.
          )pbdoc");

  // SupercellSet -- declare class
  py::class_<config::SupercellSet, std::shared_ptr<config::SupercellSet>>
      pySupercellSet(m, "SupercellSet",
                     R"pbdoc(
      Data structure for holding / reading / writing supercells.

      )pbdoc");

  // SupercellRecord -- declare class
  py::class_<config::SupercellRecord> pySupercellRecord(m, "SupercellRecord",
                                                        R"pbdoc(
     Entry in a :class:`~libcasm.configuration.SupercellSet`

   )pbdoc");

  // ConfigurationSet -- declare class
  py::class_<config::ConfigurationSet,
             std::shared_ptr<config::ConfigurationSet>>
      pyConfigurationSet(m, "ConfigurationSet",
                         R"pbdoc(
        Data structure for holding unique configurations in canonical supercells.

        Notes
        -----

        - Only :class:`~libcasm.configuration.Configuration` with degrees of \
          freedom (DoF) values that compare as unique will be kept in \
          :class:`~libcasm.configuration.ConfigurationSet`.
        - The configuration added to \
          :class:`~libcasm.configuration.ConfigurationSet` **must** already be \
          in the canonical supercell to ensure proper configuration naming, \
          serialization, and deserialization.
        - Non-canonical and non-primitive configurations may be stored in \
          :class:`~libcasm.configuration.ConfigurationSet`.
        - If a user only wants canonical or primitive \
          :class:`~libcasm.configuration.Configuration` to be stored in the \
          :class:`~libcasm.configuration.ConfigurationSet`, those checks must \
          be done by the user.
        - If the configuration to be stored are not in the canonical supercell, a
          different container type, such as `List[Configuration]`, should be used.
        - The convenience methods \
          :func:`~libcasm.configuration.io.configuration_list_to_data` and \
          :func:`~libcasm.configuration.io.configuration_list_from_data` can be
          used when writing and reading `List[Configuration]`.

        .. warning::

            Users must ensure that :class:`~libcasm.configuration.Configuration` added to :class:`~libcasm.configuration.ConfigurationSet` are in the canonical supercell. This is **not** checked by :class:`~libcasm.configuration.ConfigurationSet` but required to ensure proper configuration naming, serialization, and deserialization.

        .. warning::

            Users are responsible for placing any other constraints (canonical
            configurations only, primitive configurations only, etc.) on which
            :class:`~libcasm.configuration.Configuration` are added to
            :class:`~libcasm.configuration.ConfigurationSet`.


        Examples
        --------

        .. rubric:: Constructing ConfigurationSet and adding Configuration

        A :class:`~libcasm.configuration.ConfigurationSet` can be constructed
        and :class:`~libcasm.configuration.Configuration` added to the set as
        follows:

        .. code-block:: Python

            from libcasm.configuration import (
                Configuration,
                ConfigurationSet,
            )

            # construct ConfigurationSet
            configurationset = ConfigurationSet()

            # add Configuration
            configruationset.add(Configuration(...))
            configruationset.add(Configuration(...))


        Only :class:`~libcasm.configuration.Configuration` with degrees of
        freedom (DoF) values that compare as unique will be kept in the set.

        Only :class:`~libcasm.configuration.Configuration` with degrees of
        freedom (DoF) values that compare as unique will be kept in the
        :class:`~libcasm.configuration.ConfigurationSet`. The configuration
        must be in the canonical supercell, though this is not checked. If
        the configuration is not in the canonical supercell, use a different
        container type. A configuration_id is given automatically, using the
        next available index.


        .. rubric:: Using ConfigurationSet

        The contents of :class:`~libcasm.configuration.ConfigurationSet` are of
        type :class:`~libcasm.configuration.ConfigurationRecord`, which can be
        iterated over using a standard for loop:

        .. code-block:: Python

            # iterate over ConfigurationSet contents
            for record in configurationset:
                configuration_name = record.name
                configuration = record.configuration
                # do something ...

        The convention ``x in set`` can be used to check the contents of
        :class:`~libcasm.configuration.ConfigurationSet`, using `x` of the
        following types:

        - `str`: to check by configuration name
        - :class:`~libcasm.configuration.Configuration`: to check by configuration
          degrees of freedom (DoF) values

        .. code-block:: Python

            # check if a Configuration is in ConfigurationSet
            configuration = Configuration(...)
            if configuration in configurationset:
                # do something ...

            # check by name if a Configuration is in ConfigurationSet
            configuration_name = "SCEL2_1_2_1_1_0_0/0"
            if configuration_name in configurationset:
                # do something ...

        The value ``None`` is returned by `get` methods if the requested
        configuration is not present:

        .. code-block:: Python

            # get a configuration by name and use it
            configuration_name = "SCEL2_1_2_1_1_0_0/0"
            record = configurationset.get(configuration_name)
            if record is not None:
                configuration = record.configuration
                # do something ...
            else:
                # do something else ...

            # check if configuration is already known and get name
            configuration = Configuration(...)
            record = configurationset.get(configuration)
            if record is not None:
                configuration_name = record.configuration_name
                # do something ...

      )pbdoc");

  // ConfigurationRecord -- declare class
  py::class_<config::ConfigurationRecord> pyConfigurationRecord(
      m, "ConfigurationRecord", R"pbdoc(
     Entry in a :class:`~libcasm.configuration.ConfigurationSet`

   )pbdoc");

  py::class_<config::Supercell, std::shared_ptr<config::Supercell>>(
      m, "Supercell", R"pbdoc(
      A data structure that stores the supercell transformation matrix and
      the symmetry representations needed for applying symmetry to
      `libcasm.configuration.Configuration` associated with a particular
      supercell.

      )pbdoc")
      .def(py::init(&make_supercell), py::arg("prim"),
           py::arg("transformation_matrix_to_super").noconvert(),
           py::arg("max_n_translation_permutations") = 100,
           R"pbdoc(Constructor

      Parameters
      ----------
      prim : libcasm.configuration.Prim
          A :class:`~libcasm.configuration.Prim`
      transformation_matrix_to_super : array_like, shape=(3,3), dtype=int
          The transformation matrix, T, relating the superstructure lattice
          vectors, S, to the unit structure lattice vectors, L, according to
          ``S = L @ T``, where S and L are shape=(3,3)  matrices with lattice
          vectors as columns.
      max_n_translation_permutations : int = 100
          The complete set of translation permutations is not generated for
          large supercells with `n_unitcells` > `max_n_translation_permutations`.
      )pbdoc")
      .def(
          "prim",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            return supercell->prim;
          },
          "Returns the internal shared :class:`~libcasm.configuration.Prim`")
      .def(
          "xtal_prim",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            return supercell->prim->basicstructure;
          },
          "Returns the internal shared :class:`~libcasm.xtal.Prim`")
      .def(
          "transformation_matrix_to_super",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            return supercell->superlattice.transformation_matrix_to_super();
          },
          "Returns the supercell transformation matrix.")
      .def(
          "superlattice",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            return supercell->superlattice.superlattice();
          },
          "Returns the supercell lattice.")
      .def(
          "prim_lattice",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            return supercell->superlattice.prim_lattice();
          },
          "Returns the prim lattice.")
      .def(
          "site_index_converter",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            return supercell->unitcellcoord_index_converter;
          },
          py::return_value_policy::reference_internal,
          "A const reference to the"
          ":class:`~libcasm.xtal.SiteIndexConverter` for the supercell.")
      .def(
          "unitcell_index_converter",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            return supercell->unitcell_index_converter;
          },
          py::return_value_policy::reference_internal,
          "A const reference to the "
          ":class:`~libcasm.xtal.UnitCellIndexConverter` for the supercell.")
      .def(
          "factor_group",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            return supercell->sym_info.factor_group;
          },
          "Returns the supercell factor group, which is the subgroup of the "
          "prim factor group that leaves the supercell lattice vectors "
          "invariant.")
      .def(
          "factor_group_permutations",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            return supercell->sym_info.factor_group_permutations;
          },
          "Returns the factor group permutations, where "
          "`factor_group_permutations()[i]` describes how "
          "`factor_group().element(i)` permutes supercell site DoF values. "
          "When permuting site occupants, the following convention is used, "
          "`after[l] = before[permutation[l]]`. When applying symmetry to "
          "anisotropic DoF values, the convention used by CASM, (for example, "
          "by `apply_supercell_sym_op`), is that the DoF values are "
          "transformed first, then permuted.")
      .def(
          "translation_permutations",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            return supercell->sym_info.translation_permutations;
          },
          "Returns the translation permutations, where "
          "`translations_permutations()[i]` describes how the translation "
          "vector corresponding to translating the origin unit cell to the "
          "unitcell specified by linear index `l`, permutes supercell site DoF "
          "values. When permuting site occupants, the following convention is "
          "used, `after[l] = before[permutation[l]]`. Returns None for large "
          "supercells (n_unitcells > max_n_translation_permutations).")
      .def(
          "n_sites",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            return supercell->unitcellcoord_index_converter.total_sites();
          },
          "Returns the number of sites in the supercell.")
      .def(
          "n_unitcells",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            return supercell->unitcell_index_converter.total_sites();
          },
          "Returns the unit cells in the supercell.")
      .def(
          "n_occupants",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            std::vector<Index> n_occupants;
            auto const &converter = supercell->unitcellcoord_index_converter;
            auto const &xtal_prim = supercell->prim->basicstructure;
            auto const &unique_names = xtal_prim->unique_names();
            Index n_sites = converter.total_sites();
            for (Index l = 0; l < n_sites; ++l) {
              Index b = converter(l).sublattice();
              n_occupants.push_back(unique_names[b].size());
            }
            return n_occupants;
          },
          "Returns a `List[int]`, such that `n_occupants[l]` is the number of "
          "occupants allowed on site `l`.")
      .def(
          "occ_dof",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            std::vector<std::vector<std::string>> occ_dof;
            auto const &converter = supercell->unitcellcoord_index_converter;
            auto const &xtal_prim = supercell->prim->basicstructure;
            auto const &unique_names = xtal_prim->unique_names();
            Index n_sites = converter.total_sites();
            for (Index l = 0; l < n_sites; ++l) {
              Index b = converter(l).sublattice();
              occ_dof.push_back(unique_names[b]);
            }
            return occ_dof;
          },
          "Returns a `List[List[str]]`, such that `occ_dof[l][s]` is the name "
          "('orientation name') of the occupant corresponding to occupation "
          "value `s` on site `l`.")
      .def(
          "coordinate_cart",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            auto const &converter = supercell->unitcellcoord_index_converter;
            auto const &xtal_prim = supercell->prim->basicstructure;
            Index n_sites = converter.total_sites();
            Eigen::MatrixXd R(3, n_sites);
            for (Index l = 0; l < n_sites; ++l) {
              xtal::UnitCellCoord bijk = converter(l);
              R.col(l) = bijk.coordinate(*xtal_prim).const_cart();
            }
            return R;
          },
          "Returns the basis site positions, as columns of a matrix, in "
          "Cartesian coordinates")
      .def(
          "coordinate_frac",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            auto const &converter = supercell->unitcellcoord_index_converter;
            auto const &xtal_prim = supercell->prim->basicstructure;
            Index n_sites = converter.total_sites();
            Eigen::MatrixXd R(3, n_sites);
            for (Index l = 0; l < n_sites; ++l) {
              xtal::UnitCellCoord bijk = converter(l);
              R.col(l) = bijk.coordinate(*xtal_prim).const_frac();
            }
            return R;
          },
          "Returns the basis site positions, as columns of a matrix, in "
          "fractional coordinates of the prim lattice vectors.")
      .def(
          "sublattice_indices",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            std::vector<Index> sublattice_indices;
            auto const &converter = supercell->unitcellcoord_index_converter;
            Index n_sites = converter.total_sites();
            for (Index l = 0; l < n_sites; ++l) {
              sublattice_indices.push_back(converter(l).sublattice());
            }
            return sublattice_indices;
          },
          "Returns the sublattice indices, as a List[int], of each site "
          "in the supercell.")
      .def(
          "unitcell_indices",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            auto const &converter = supercell->unitcellcoord_index_converter;
            Index n_sites = converter.total_sites();
            Eigen::MatrixXl R(3, n_sites);
            for (Index l = 0; l < n_sites; ++l) {
              xtal::UnitCellCoord bijk = converter(l);
              R.col(l) = bijk.unitcell();
            }
            return R;
          },
          "Returns the integer unit cell indices, as columns of a matrix, of "
          "each site in the supercell.")
      .def(
          "linear_unitcell_indices",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            std::vector<Index> unitcell_indices;
            auto const &xtal_prim = supercell->prim->basicstructure;
            Index N_sublat = xtal_prim->basis().size();
            Index N_unitcells =
                supercell->unitcell_index_converter.total_sites();
            for (Index b = 0; b < N_sublat; ++b) {
              for (Index i = 0; i < N_unitcells; ++i) {
                unitcell_indices.push_back(i);
              }
            }
            return unitcell_indices;
          },
          "Returns the linear unitcell index for each site in the supercell.")
      .def(
          "linear_unitcell_index",
          [](std::shared_ptr<config::Supercell const> const &supercell,
             Eigen::Vector3l const &unitcell) {
            return supercell->unitcell_index_converter(unitcell);
          },
          py::arg("unitcell"),
          "Returns the linear unitcell index for the given unit cell "
          "coordinates.")
      .def(
          "linear_site_index",
          [](std::shared_ptr<config::Supercell const> const &supercell,
             xtal::UnitCellCoord const &integral_site_coordinate) {
            auto const &converter = supercell->unitcellcoord_index_converter;
            return converter(integral_site_coordinate);
          },
          py::arg("integral_site_coordinate"),
          "Converts integral_site_coordinate to the linear site index of the "
          "periodic equivalent site within the supercell.")
      .def(
          "within",
          [](std::shared_ptr<config::Supercell const> const &supercell,
             xtal::UnitCellCoord const &integral_site_coordinate) {
            auto const &converter = supercell->unitcellcoord_index_converter;
            return converter.bring_within(integral_site_coordinate);
          },
          py::arg("integral_site_coordinate"),
          "Returns the periodic equivalent integral_site_coordinate within the "
          "supercell.")
      .def(
          "integral_site_coordinate",
          [](std::shared_ptr<config::Supercell const> const &supercell,
             Index l) {
            auto const &converter = supercell->unitcellcoord_index_converter;
            return converter(l);
          },
          "Returns the integral_site_coordinate of a site in the supercell.")
      .def(py::self < py::self,
           "Sorts supercells by size then how canonical the lattice vectors "
           "are. Only supercells with the same prim can be compared.")
      .def(py::self <= py::self,
           "Sorts supercells by size then how canonical the lattice vectors "
           "are. Only supercells with the same prim can be compared.")
      .def(py::self > py::self,
           "Sorts supercells by size then how canonical the lattice vectors "
           "are. Only supercells with the same prim can be compared.")
      .def(py::self >= py::self,
           "Sorts supercells by size then how canonical the lattice vectors "
           "are. Only supercells with the same prim can be compared.")
      .def(py::self == py::self,
           "True if supercells are equal. Only supercells with the same prim "
           "can be compared.")
      .def(py::self != py::self,
           ""
           "True if supercells are not equal. Only supercells with the same "
           "prim can be compared.")
      .def_static(
          "from_dict",
          [](const nlohmann::json &data,
             std::shared_ptr<config::SupercellSet> supercells) {
            jsonParser json{data};
            std::shared_ptr<config::Supercell const> supercell;
            from_json(supercell, json, *supercells);
            return supercell;
          },
          R"pbdoc(
        Construct a Supercell from a Python dict

        The `Configuration reference <https://prisms-center.github.io/CASMcode_docs/formats/casm/clex/Configuration/>`_ documents the expected format for Configurations and Supercells."

        Parameters
        ----------
        data : dict
            A :class:`~libcasm.configuration.Supercell` as a dict.
        supercells : libcasm.configuration.SupercellSet
            A :class:`~libcasm.configuration.SupercellSet`, which holds shared
            supercells in order to avoid duplicates.

        Returns
        -------
        supercell : libcasm.configuration.Supercell
            The :class:`~libcasm.configuration.Supercell` constructed from the dict.
        )pbdoc",
          py::arg("data"), py::arg("supercells"))
      .def(
          "to_dict",
          [](std::shared_ptr<config::Supercell const> const &supercell) {
            jsonParser json;
            to_json(supercell, json);
            return static_cast<nlohmann::json>(json);
          },
          "Represent the Supercell as a Python dict. The `Configuration "
          "reference "
          "<https://prisms-center.github.io/CASMcode_docs/formats/casm/clex/"
          "Configuration/>`_ documents the expected format for Configurations "
          "and Supercells.");

  m.def(
      "is_canonical_supercell",
      [](std::shared_ptr<config::Supercell const> const &supercell) {
        return is_canonical(*supercell);
      },
      py::arg("init_supercell"),
      "Return true if supercell lattice is in canonical form");

  m.def(
      "make_canonical_supercell",
      [](std::shared_ptr<config::Supercell const> const &supercell) {
        return make_canonical_form(*supercell);
      },
      py::arg("init_supercell"),
      "Return a supercell that compares greater to all equivalent supercells "
      "generated using the prim crystal point group");

  m.def(
      "to_canonical_supercell",
      [](std::shared_ptr<config::Supercell const> const &supercell) {
        return to_canonical(*supercell);
      },
      py::arg("supercell"),
      "Return the :class:`~libcasm.xtal.SymOp` that makes a supercell lattice "
      "canonical");

  m.def(
      "from_canonical_supercell",
      [](std::shared_ptr<config::Supercell const> const &supercell) {
        return from_canonical(*supercell);
      },
      py::arg("supercell"),
      "Return the :class:`~libcasm.xtal.SymOp` that makes a supercell lattice "
      "from the canonical supercell lattice");

  m.def(
      "make_equivalent_supercells",
      [](std::shared_ptr<config::Supercell const> const &supercell) {
        return make_equivalents(*supercell);
      },
      py::arg("supercell"),
      "Return a list of supercells with distinct, but symmetrically equivalent "
      "lattice vectors, using the prim crystal point group.");

  // SupercellRecord -- define functions
  pySupercellRecord
      .def(py::init<std::shared_ptr<config::Supercell const> const &>(),
           py::arg("supercell"), "Construct a SupercellRecord.")
      .def_readonly("supercell", &config::SupercellRecord::supercell,
                    "The shared :class:`~libcasm.configuration.Supercell`")
      .def_readonly("supercell_name", &config::SupercellRecord::supercell_name,
                    "The supercell name.")
      .def_readonly("canonical_supercell_name",
                    &config::SupercellRecord::canonical_supercell_name,
                    "The canonical equivalent supercell name.")
      .def_readonly("is_canonical", &config::SupercellRecord::is_canonical,
                    "True if the supercell is canonical, False otherwise.")
      .def(py::self < py::self, "Sorts SupercellRecord.")
      .def(py::self <= py::self, "Sorts SupercellRecord.")
      .def(py::self > py::self, "Sorts SupercellRecord.")
      .def(py::self >= py::self, "Sorts SupercellRecord.")
      .def(py::self == py::self, "Compare SupercellRecord.")
      .def(py::self != py::self, "Compare SupercellRecord.")
      .def("__copy__",
           [](config::SupercellRecord const &self) {
             return config::SupercellRecord(self);
           })
      .def("__deepcopy__", [](config::SupercellRecord const &self, py::dict) {
        return config::SupercellRecord(self);
      });

  // ConfigurationRecord -- define functions
  pyConfigurationRecord
      .def(py::init<config::Configuration const &, std::string, std::string>(),
           py::arg("configuration"), py::arg("supercell_name"),
           py::arg("configuration_id"), "Construct a ConfigurationRecord.")
      .def_readonly("configuration",
                    &config::ConfigurationRecord::configuration,
                    "The :class:`~libcasm.configuration.Configuration`")
      .def_readonly("supercell_name",
                    &config::ConfigurationRecord::supercell_name,
                    "The supercell name.")
      .def_readonly("configuration_id",
                    &config::ConfigurationRecord::configuration_id,
                    "The configuration id.")
      .def_readonly("configuration_name",
                    &config::ConfigurationRecord::configuration_name,
                    "The configuration name.")
      .def(py::self < py::self, "Sorts ConfigurationRecord.")
      .def(py::self <= py::self, "Sorts ConfigurationRecord.")
      .def(py::self > py::self, "Sorts ConfigurationRecord.")
      .def(py::self >= py::self, "Sorts ConfigurationRecord.")
      .def(py::self == py::self, "Compare ConfigurationRecord.")
      .def(py::self != py::self, "Compare ConfigurationRecord.")
      .def("__copy__",
           [](config::ConfigurationRecord const &self) {
             return config::ConfigurationRecord(self);
           })
      .def("__deepcopy__",
           [](config::ConfigurationRecord const &self, py::dict) {
             return config::ConfigurationRecord(self);
           });

  // SupercellSet -- define functions
  pySupercellSet
      .def(py::init<std::shared_ptr<config::Prim const> const &>(),
           py::arg("prim"),
           R"pbdoc(
          Construct an empty SupercellSet

          Parameters
          ----------
          prim : libcasm.configuration.Prim
              A :class:`~libcasm.configuration.Prim`
          )pbdoc")
      .def("prim", &config::SupercellSet::prim,
           "Returns the internal shared :class:`~libcasm.configuration.Prim`")
      .def("empty", &config::SupercellSet::empty,
           "Returns True if the SupercellSet is empty")
      // len(set)
      .def("__len__", &config::SupercellSet::size)
      // clear
      .def("clear", &config::SupercellSet::clear, "Clear SupercellSet")
      // add
      .def(
          "add_supercell",
          [](config::SupercellSet &m,
             std::shared_ptr<config::Supercell const> supercell)
              -> config::SupercellRecord const & {
            return *(m.insert(supercell).first);
          },
          py::return_value_policy::reference,
          R"pbdoc(
          Add a supercell to the set

          Parameters
          ----------
          supercell : libcasm.configuration.Supercell
              A supercell to add to the set.

          Returns
          -------
          record : libcasm.configuration.SupercellRecord
              A :class:`~libcasm.configuration.SupercellRecord`, as a const reference.
          )pbdoc",
          py::arg("supercell"))
      .def(
          "add",
          [](config::SupercellSet &m,
             std::shared_ptr<config::Supercell const> supercell)
              -> config::SupercellRecord const & {
            return *(m.insert(supercell).first);
          },
          py::return_value_policy::reference,
          R"pbdoc(
          Add a supercell to the set (equivalent to \
          :func:`~libcasm.configuration.SupercellSet.add_supercell`).
          )pbdoc",
          py::arg("supercell"))
      .def(
          "add_by_transformation_matrix_to_super",
          [](config::SupercellSet &m,
             Eigen::Matrix3l const &transformation_matrix_to_super)
              -> config::SupercellRecord const & {
            return *(m.insert(transformation_matrix_to_super).first);
          },
          py::return_value_policy::reference,
          R"pbdoc(
          Add a supercell to the set, by constructing from the transformation matrix.

          Parameters
          ----------
          transformation_matrix_to_super : array_like, shape=(3,3), dtype=int
              The transformation matrix, T, relating the superstructure lattice
              vectors, S, to the unit structure lattice vectors, L, according to
              ``S = L @ T``, where S and L are shape=(3,3)  matrices with lattice
              vectors as columns.

          Returns
          -------
          record : libcasm.configuration.SupercellRecord
              A :class:`~libcasm.configuration.SupercellRecord`, as a const reference.
          )pbdoc",
          py::arg("transformation_matrix_to_super").noconvert())
      .def(
          "add",
          [](config::SupercellSet &m,
             Eigen::Matrix3l const &transformation_matrix_to_super)
              -> config::SupercellRecord const & {
            return *(m.insert(transformation_matrix_to_super).first);
          },
          py::return_value_policy::reference,
          R"pbdoc(
          Add a supercell to the set, by constructing from the transformation \
          matrix (equivalent to :func:`~libcasm.configuration.SupercellSet.add_by_transformation_matrix_to_super`).
          )pbdoc",
          py::arg("transformation_matrix_to_super").noconvert())
      .def(
          "add_record",
          [](config::SupercellSet &m, config::SupercellRecord const &record)
              -> config::SupercellRecord const & {
            return *(m.insert(record).first);
          },
          py::return_value_policy::reference,
          R"pbdoc(
          Add a supercell record to the set.

          Parameters
          ----------
          record : libcasm.configuration.SupercellRecord
              A supercell record to add.

          Returns
          -------
          record : libcasm.configuration.SupercellRecord
              A :class:`~libcasm.configuration.SupercellRecord`, as a const reference.
          )pbdoc",
          py::arg("record"))
      .def(
          "add",
          [](config::SupercellSet &m, config::SupercellRecord const &record)
              -> config::SupercellRecord const & {
            return *(m.insert(record).first);
          },
          py::return_value_policy::reference,
          R"pbdoc(
          Add a supercell record to the set (equivalent to \
          :func:`~libcasm.configuration.SupercellSet.add_record`).
          )pbdoc",
          py::arg("record"))
      .def(
          "add_by_canonical_name",
          [](config::SupercellSet &m,
             std::string supercell_name) -> config::SupercellRecord const & {
            return *(m.insert_canonical(supercell_name).first);
          },
          py::return_value_policy::reference,
          R"pbdoc(
          Construct the canonical supercell from a supercell name and add to the set.

          Parameters
          ----------
          supercell_name : str
              The name of a canonical supercell. Raises if `supercell_name` is not
              the name of the canonical equivalent supercell.

          Returns
          -------
          record : libcasm.configuration.SupercellRecord
              A :class:`~libcasm.configuration.SupercellRecord`, as a const reference.
          )pbdoc",
          py::arg("supercell_name"))
      .def(
          "add",
          [](config::SupercellSet &m,
             std::string supercell_name) -> config::SupercellRecord const & {
            return *(m.insert_canonical(supercell_name).first);
          },
          py::return_value_policy::reference,
          R"pbdoc(
          Construct the canonical supercell from a supercell name and add to \
          the set (equivalent to \
          :func:`~libcasm.configuration.SupercellSet.add_by_canonical_name`).
          )pbdoc",
          py::arg("supercell_name"))
      // remove
      .def(
          "remove_supercell",
          [](config::SupercellSet &m,
             std::shared_ptr<config::Supercell const> supercell) {
            auto it = m.find(supercell);
            if (it == m.end()) {
              throw pybind11::key_error("Not in set");
            }
            m.erase(it);
          },
          R"pbdoc(
          Remove a supercell from the set. Raises if not in the set.
          )pbdoc",
          py::arg("supercell"))
      .def(
          "remove",
          [](config::SupercellSet &m,
             std::shared_ptr<config::Supercell const> supercell) {
            auto it = m.find(supercell);
            if (it == m.end()) {
              throw pybind11::key_error("Not in set");
            }
            m.erase(it);
          },
          R"pbdoc(
          Remove a supercell from the set. Raises if not in the set. Equivalent to \
          :func:`~libcasm.configuration.SupercellSet.remove_supercell`.
          )pbdoc",
          py::arg("supercell"))
      .def(
          "remove_by_transformation_matrix_to_super",
          [](config::SupercellSet &m,
             Eigen::Matrix3l const &transformation_matrix_to_super) {
            auto it = m.find(transformation_matrix_to_super);
            if (it == m.end()) {
              throw pybind11::key_error("Not in set");
            }
            m.erase(it);
          },
          R"pbdoc(
          Remove a supercell from the set. Raises if not in the set.
          )pbdoc",
          py::arg("transformation_matrix_to_super").noconvert())
      .def(
          "remove",
          [](config::SupercellSet &m,
             Eigen::Matrix3l const &transformation_matrix_to_super) {
            auto it = m.find(transformation_matrix_to_super);
            if (it == m.end()) {
              throw pybind11::key_error("Not in set");
            }
            m.erase(it);
          },
          R"pbdoc(
          Remove a supercell from the set. Raises if not in the set. Equivalent to \
          :func:`~libcasm.configuration.SupercellSet.remove_by_transformation_matrix_to_super`.
          )pbdoc",
          py::arg("transformation_matrix_to_super").noconvert())
      .def(
          "remove_record",
          [](config::SupercellSet &m, config::SupercellRecord const &record) {
            auto it = m.find(record);
            if (it == m.end()) {
              throw pybind11::key_error("Not in set");
            }
            m.erase(it);
          },
          R"pbdoc(
          Remove a supercell record from the set. Raises if not in the set.
          )pbdoc",
          py::arg("record"))
      .def(
          "remove",
          [](config::SupercellSet &m, config::SupercellRecord const &record) {
            auto it = m.find(record);
            if (it == m.end()) {
              throw pybind11::key_error("Not in set");
            }
            m.erase(it);
          },
          R"pbdoc(
          Remove a supercell record from the set. Raises if not in the set. \
          Equivalent to :func:`~libcasm.configuration.SupercellSet.remove_record`.
          )pbdoc",
          py::arg("record"))
      .def(
          "remove_by_canonical_name",
          [](config::SupercellSet &m, std::string supercell_name) {
            auto it = m.find_canonical_by_name(supercell_name);
            if (it == m.end()) {
              throw pybind11::key_error("Not in set");
            }
            m.erase(it);
          },
          R"pbdoc(
          Remove the canonical supercell, determined by supercell name, from \
          the set. Raises if not in the set.
          )pbdoc",
          py::arg("supercell_name"))
      //
      .def(
          "remove",
          [](config::SupercellSet &m, std::string supercell_name) {
            auto it = m.find_canonical_by_name(supercell_name);
            if (it == m.end()) {
              throw pybind11::key_error("Not in set");
            }
            m.erase(it);
          },
          R"pbdoc(
          Remove the canonical supercell, determined by supercell name, from \
          the set. Raises if not in the set. Equivalent to \
          :func:`~libcasm.configuration.SupercellSet.remove_by_canonical_name`.
          )pbdoc",
          py::arg("supercell_name"))
      // discard
      .def(
          "discard_supercell",
          [](config::SupercellSet &m,
             std::shared_ptr<config::Supercell const> supercell) {
            m.erase(supercell);
          },
          R"pbdoc(
          Remove a supercell from the set if present
          )pbdoc",
          py::arg("supercell"))
      .def(
          "discard",
          [](config::SupercellSet &m,
             std::shared_ptr<config::Supercell const> supercell) {
            m.erase(supercell);
          },
          R"pbdoc(
          Remove a supercell from the set if present. Equivalent to \
          :func:`~libcasm.configuration.SupercellSet.discard_supercell`.
          )pbdoc",
          py::arg("supercell"))
      .def(
          "discard_by_transformation_matrix_to_super",
          [](config::SupercellSet &m,
             Eigen::Matrix3l const &transformation_matrix_to_super) {
            m.erase(transformation_matrix_to_super);
          },
          R"pbdoc(
          Remove a supercell from the set if present, by checking for the \
          transformation matrix.
          )pbdoc",
          py::arg("transformation_matrix_to_super").noconvert())
      .def(
          "discard",
          [](config::SupercellSet &m,
             Eigen::Matrix3l const &transformation_matrix_to_super) {
            m.erase(transformation_matrix_to_super);
          },
          R"pbdoc(
          Remove a supercell from the set if present, by checking for the \
          transformation matrix. Equivalent to \
          :func:`~libcasm.configuration.SupercellSet.discard_by_transformation_matrix_to_super`.
          )pbdoc",
          py::arg("transformation_matrix_to_super").noconvert())
      .def(
          "discard_record",
          [](config::SupercellSet &m, config::SupercellRecord const &record) {
            m.erase(record);
          },
          R"pbdoc(
          Remove a supercell from the set if present.
          )pbdoc",
          py::arg("record"))
      .def(
          "discard",
          [](config::SupercellSet &m, config::SupercellRecord const &record) {
            m.erase(record);
          },
          R"pbdoc(
          Remove a supercell from the set if present. Equivalent to \
          :func:`~libcasm.configuration.SupercellSet.discard_record`.
          )pbdoc",
          py::arg("record"))
      .def(
          "discard_by_canonical_name",
          [](config::SupercellSet &m, std::string supercell_name) {
            m.erase_canonical_by_name(supercell_name);
          },
          R"pbdoc(
          Remove a canonical supercell, determined by supercell name, from the \
          set if present.
          )pbdoc",
          py::arg("supercell_name"))
      .def(
          "discard",
          [](config::SupercellSet &m, std::string supercell_name) {
            m.erase_canonical_by_name(supercell_name);
          },
          R"pbdoc(
          Remove a canonical supercell, determined by supercell name, from the \
          set if present. Equivalent to \
          :func:`~libcasm.configuration.SupercellSet.discard_by_canonical_name`.
          )pbdoc",
          py::arg("supercell_name"))
      // x in set
      .def(
          "__contains__",
          [](config::SupercellSet &m,
             std::shared_ptr<config::Supercell const> supercell) {
            return m.find(supercell) != m.end();
          },
          R"pbdoc(
          Check if a supercell is contained in the set.
          )pbdoc",
          py::arg("supercell"))
      .def(
          "__contains__",
          [](config::SupercellSet &m,
             Eigen::Matrix3l const &transformation_matrix_to_super) {
            return m.find(transformation_matrix_to_super) != m.end();
          },
          R"pbdoc(
          Check if a supercell is contained in the set, by transformation matrix.
          )pbdoc",
          py::arg("transformation_matrix_to_super").noconvert())
      .def(
          "__contains__",
          [](config::SupercellSet &m, config::SupercellRecord const &record) {
            return m.find(record) != m.end();
          },
          R"pbdoc(
          Check if a supercell record is contained in the set.
          )pbdoc",
          py::arg("record"))
      .def(
          "__contains__",
          [](config::SupercellSet &m, std::string supercell_name) {
            return m.find_canonical_by_name(supercell_name) != m.end();
          },
          R"pbdoc(
          Check if a canonical supercell, determined by supercell name, is \
          contained in the set.
          )pbdoc",
          py::arg("record"))
      // for x in set
      .def(
          "__iter__",
          [](config::SupercellSet const &m) {
            return py::make_iterator(m.begin(), m.end());
          },
          py::keep_alive<
              0, 1>() /* Essential: keep object alive while iterator exists */)
      .def_static(
          "from_dict",
          [](const nlohmann::json &data,
             std::shared_ptr<config::Prim const> const &prim)
              -> std::shared_ptr<config::SupercellSet> {
            auto supercells = std::make_shared<config::SupercellSet>(prim);
            jsonParser json{data};
            from_json(*supercells, json, prim);
            return supercells;
          },
          R"pbdoc(
          Construct SupercellSet from a Python dict

          Parameters
          ----------
          data : dict
              The serialized SupercellSet. Expected format:

                  version: string
                      A string indicating format version

                  supercells: Dict[str,array_like]
                      A dict of canonical supercells, with supercell name as key
                      and the integer transformation matrix, T, as value. T relates
                      the superstructure lattice vectors, S, defining the DoF space
                      to the unit structure lattice vectors, L, according to
                      ``S = L @ T``, where S and L are shape=(3,3) matrices with
                      lattice vectors as columns.

                  non_canonical_supercells: List[Dict]
                      A list of non-canonical supercells. The format is:

                          "supercell_name": <supercell_name>,
                          "canonical_supercell_name": <canonical_supercell_name>,
                          "transformation_matrix_to_supercell": <transformation_matrix_to_super>

          prim : libcasm.configuration.Prim
              A :class:`~libcasm.configuration.Prim`

          Returns
          -------
          supercells : libcasm.configuration.SupercellSet
              The :class:`~libcasm.configuration.SupercellSet`.
          )pbdoc",
          py::arg("data"), py::arg("prim"))
      .def(
          "to_dict",
          [](std::shared_ptr<config::SupercellSet> supercells,
             std::string version) -> nlohmann::json {
            jsonParser json;
            if (version == "2.0") {
              to_json(*supercells, json);
            } else if (version == "1.0") {
              to_json_v1(*supercells, json);
            } else {
              throw std::runtime_error(
                  "Error in SupercellSet.to_dict: invalid version");
            }
            return static_cast<nlohmann::json>(json);
          },
          R"pbdoc(
          Represent the SupercellSet as a Python dict.

          Parameters
          ----------
          version : str = "2.0"
              Specify the format version to output. Options are:

              - "2.0": Includes "supercells" and "non_canonical_supercells"
              - "1.0": Only includes "supercells"

          Returns
          -------
          data :
              The :class:`~libcasm.configuration.SupercellSet`.
          )pbdoc",
          py::arg("version") = std::string("2.0"));

  pyConfigurationSet
      .def(py::init<>(),
           R"pbdoc(
          Construct an empty ConfigurationSet
          )pbdoc")
      .def("empty", &config::ConfigurationSet::empty,
           "Returns True if the ConfigurationSet is empty")
      // len(set)
      .def("__len__", &config::ConfigurationSet::size)
      // clear
      .def("clear", &config::ConfigurationSet::clear, "Clear ConfigurationSet")
      // add
      .def(
          "add_configuration",
          [](config::ConfigurationSet &m,
             config::Configuration const &configuration,
             std::optional<std::string> supercell_name)
              -> config::ConfigurationRecord const & {
            if (supercell_name.has_value()) {
              return *(m.insert(*supercell_name, configuration).first);
            } else {
              return *(m.insert(configuration).first);
            }
          },
          py::return_value_policy::reference,
          R"pbdoc(
          Add a configuration to the set

          Parameters
          ----------
          configuration : libcasm.configuration.Configuration
              The configuration to add if it is unique. The configuration must
              be in the canonical supercell, though this is not checked. If the
              configuration is not in the canonical supercell, use a different
              container type. A configuration_id is given automatically, using
              the next available index.
          supercell_name : Optional[str] = None
              If the supercell name is known, insertion may be faster.

          Returns
          -------
          record : libcasm.configuration.ConfigurationRecord
              A :class:`~libcasm.configuration.ConfigurationRecord`, as a
              const reference.

          )pbdoc",
          py::arg("configuration"), py::arg("supercell_name") = std::nullopt)
      .def(  // make "add_configuration" available via "add"
          "add",
          [](config::ConfigurationSet &m,
             config::Configuration const &configuration,
             std::optional<std::string> supercell_name)
              -> config::ConfigurationRecord const & {
            if (supercell_name.has_value()) {
              return *(m.insert(*supercell_name, configuration).first);
            } else {
              return *(m.insert(configuration).first);
            }
          },
          py::return_value_policy::reference,
          R"pbdoc(
          Add a configuration to the set (equivalent to \
          :func:`~libcasm.configuration.ConfigurationSet.add_configuration`)
          )pbdoc",
          py::arg("configuration"), py::arg("supercell_name") = std::nullopt)
      .def(
          "add_record",
          [](config::ConfigurationSet &m,
             config::ConfigurationRecord const &record)
              -> config::ConfigurationRecord const & {
            return *m.insert(record).first;
          },
          py::return_value_policy::reference,
          R"pbdoc(
          Add a configuration record to the set, allowing custom configuration_id

          Parameters
          ----------
          record : libcasm.configuration.ConfigurationRecord
              A :class:`~libcasm.configuration.ConfigurationRecord` to insert in
              the set.

          Returns
          -------
          record : libcasm.configuration.ConfigurationRecord
              A :class:`~libcasm.configuration.ConfigurationRecord` held by the
              set, as a const reference.
          )pbdoc",
          py::arg("record"))
      .def(  // make "add_record" available via "add"
          "add",
          [](config::ConfigurationSet &m,
             config::ConfigurationRecord const &record)
              -> config::ConfigurationRecord const & {
            return *m.insert(record).first;
          },
          py::return_value_policy::reference,
          R"pbdoc(
          Add a configuration to the set (equivalent to \
          :func:`~libcasm.configuration.ConfigurationSet.add_record`)
          )pbdoc",
          py::arg("record"))
      // get
      .def(
          "get_configuration",
          [](config::ConfigurationSet &m,
             config::Configuration const &configuration) -> py::object {
            auto it = m.find(configuration);
            if (it == m.end()) {
              return py::none();
            }
            return py::object(
                py::cast<config::ConfigurationRecord const &>(*it));
          },
          py::return_value_policy::reference,
          R"pbdoc(
          Find a ConfigurationRecord by configuration degrees of freedom (DoF) \
          and return a const reference, else return None.
          )pbdoc",
          py::arg("configuration"))
      .def(
          "get",
          [](config::ConfigurationSet &m,
             config::Configuration const &configuration) -> py::object {
            auto it = m.find(configuration);
            if (it == m.end()) {
              return py::none();
            }
            return py::object(
                py::cast<config::ConfigurationRecord const &>(*it));
          },
          py::return_value_policy::reference,
          R"pbdoc(
          Find a ConfigurationRecord by configuration degrees of freedom (DoF) \
          and return a const reference, else return None (equivalent to \
          :func:`~libcasm.configuration.ConfigurationSet.get_configuration`).
          )pbdoc",
          py::arg("configuration"))
      .def(
          "get_by_name",
          [](config::ConfigurationSet &m,
             std::string configuration_name) -> py::object {
            auto it = m.find_by_name(configuration_name);
            if (it == m.end()) {
              return py::none();
            }
            return py::object(
                py::cast<config::ConfigurationRecord const &>(*it));
          },
          py::return_value_policy::reference,
          R"pbdoc(
          Find a ConfigurationRecord by configuration name and return a const \
          reference, else return None.
          )pbdoc",
          py::arg("configuration_name"))
      .def(
          "get",
          [](config::ConfigurationSet &m,
             std::string configuration_name) -> py::object {
            auto it = m.find_by_name(configuration_name);
            if (it == m.end()) {
              return py::none();
            }
            return py::object(
                py::cast<config::ConfigurationRecord const &>(*it));
          },
          py::return_value_policy::reference,
          R"pbdoc(
          Find a ConfigurationRecord by configuration name and return a const \
          reference, else return None (equivalent to \
          :func:`~libcasm.configuration.ConfigurationSet.get_by_name`).
          )pbdoc",
          py::arg("configuration_name"))
      // remove
      .def(
          "remove_configuration",
          [](config::ConfigurationSet &m,
             config::Configuration const &configuration) {
            auto it = m.find(configuration);
            if (it == m.end()) {
              throw pybind11::key_error("Not in set");
            }
            m.erase(it);
          },
          R"pbdoc(
          Find a ConfigurationRecord by configuration degrees of freedom (DoF) \
          and remove from the set. Raise KeyError if not in the set.
          )pbdoc",
          py::arg("configuration"))
      .def(
          "remove",
          [](config::ConfigurationSet &m,
             config::Configuration const &configuration) {
            auto it = m.find(configuration);
            if (it == m.end()) {
              throw pybind11::key_error("Not in set");
            }
            m.erase(it);
          },
          R"pbdoc(
          Find a ConfigurationRecord by configuration degrees of freedom (DoF) \
          and remove from the set. Raise KeyError if not in the set (equivalent \
          to :func:`~libcasm.configuration.ConfigurationSet.remove_configuration`).
          )pbdoc",
          py::arg("configuration"))
      .def(
          "remove_by_name",
          [](config::ConfigurationSet &m, std::string configuration_name) {
            auto it = m.find_by_name(configuration_name);
            if (it == m.end()) {
              throw pybind11::key_error("Not in set");
            }
            m.erase(it);
          },
          R"pbdoc(
          Find a ConfigurationRecord by configuration name and remove from the \
          set. Raise KeyError if not in the set.
          )pbdoc",
          py::arg("configuration_name"))
      .def(
          "remove",
          [](config::ConfigurationSet &m, std::string configuration_name) {
            auto it = m.find_by_name(configuration_name);
            if (it == m.end()) {
              throw pybind11::key_error("Not in set");
            }
            m.erase(it);
          },
          R"pbdoc(
          Find a ConfigurationRecord by configuration name and remove from the \
          set. Raise KeyError if not in the set (equivalent to \
          :func:`~libcasm.configuration.ConfigurationSet.remove_by_name`).
          )pbdoc",
          py::arg("configuration_name"))
      // discard
      .def(
          "discard_configuration",
          [](config::ConfigurationSet &m,
             config::Configuration const &configuration) {
            auto it = m.find(configuration);
            if (it != m.end()) {
              m.erase(it);
            }
          },
          R"pbdoc(
          Find a ConfigurationRecord by configuration degrees of freedom (DoF) \
          and remove from the set if present.
          )pbdoc",
          py::arg("configuration"))
      .def(
          "discard",
          [](config::ConfigurationSet &m,
             config::Configuration const &configuration) {
            auto it = m.find(configuration);
            if (it != m.end()) {
              m.erase(it);
            }
          },
          R"pbdoc(
          Find a ConfigurationRecord by configuration degrees of freedom (DoF) \
          and remove from the set if present (equivalent to \
          :func:`~libcasm.configuration.ConfigurationSet.discard_configuration`).
          )pbdoc",
          py::arg("configuration"))
      .def(
          "discard_by_name",
          [](config::ConfigurationSet &m, std::string configuration_name) {
            auto it = m.find_by_name(configuration_name);
            if (it != m.end()) {
              m.erase(it);
            }
          },
          R"pbdoc(
          Find a ConfigurationRecord by configuration name and remove from \
          the set if present.
          )pbdoc",
          py::arg("configuration_name"))
      .def(
          "discard",
          [](config::ConfigurationSet &m, std::string configuration_name) {
            auto it = m.find_by_name(configuration_name);
            if (it != m.end()) {
              m.erase(it);
            }
          },
          R"pbdoc(
          Find a ConfigurationRecord by configuration name and remove from the \
          set if present (equivalent to \
          :func:`~libcasm.configuration.ConfigurationSet.discard_by_name`).
          )pbdoc",
          py::arg("configuration_name"))
      // x in set
      .def(
          "__contains__",
          [](config::ConfigurationSet &m,
             config::Configuration const &configuration) {
            return m.find(configuration) != m.end();
          },
          R"pbdoc(
          Check by configuration degrees of freedom if configuration is in set.
          )pbdoc",
          py::arg("record"))
      // x in set
      .def(
          "__contains__",
          [](config::ConfigurationSet &m, std::string configuration_name) {
            return m.find_by_name(configuration_name) != m.end();
          },
          R"pbdoc(
          Check by configuration_name if configuration is in set.
          )pbdoc",
          py::arg("record"))
      // for x in set
      .def(
          "__iter__",
          [](config::ConfigurationSet const &m) {
            return py::make_iterator(m.begin(), m.end());
          },
          py::keep_alive<
              0, 1>() /* Essential: keep object alive while iterator exists */)
      .def_static(
          "from_dict",
          [](const nlohmann::json &data,
             std::shared_ptr<config::SupercellSet> supercells) {
            jsonParser json{data};
            std::shared_ptr<config::ConfigurationSet> configurations =
                std::make_shared<config::ConfigurationSet>();
            from_json(*supercells, *configurations, json, supercells->prim());
            return configurations;
          },
          R"pbdoc(
          Construct a ConfigurationSet from a Python dict

          The `Configuration reference <https://prisms-center.github.io/CASMcode_docs/formats/casm/clex/Configuration/>`_ documents the expected format for Configurations and Supercells."

          Parameters
          ----------
          data : dict
              The serialized ConfigurationSet. Expected format:

              .. code-block::

                  {
                    "version": "1.0",
                    "supercells": {
                      "<supercell_name>": {
                        "<configuration_id>": <Configuration JSON>,
                          ...
                        },
                        ...
                    }
                  }


          supercells : libcasm.configuration.SupercellSet
              A :class:`~libcasm.configuration.SupercellSet`, which holds shared
              supercells used by the constructed
              :class:`~libcasm.configuration.Configuration` in order to avoid
              duplicates.

          Returns
          -------
          configurations : libcasm.configuration.ConfigurationSet
              The :class:`~libcasm.configuration.ConfigurationSet` constructed from
              the dict.
          )pbdoc",
          py::arg("data"), py::arg("supercells"))
      .def(
          "to_dict",
          [](config::ConfigurationSet const &configurations) {
            jsonParser json;
            to_json(configurations, json);
            return static_cast<nlohmann::json>(json);
          },
          "Represent the ConfigurationSet as a Python dict. The `Configuration "
          "reference "
          "<https://prisms-center.github.io/CASMcode_docs/formats/casm/clex/"
          "Configuration/>`_ documents the expected format for Configurations "
          "and Supercells.");

  // SupercellSymOp -- declare class
  py::class_<config::SupercellSymOp> pySupercellSymOp(m, "SupercellSymOp",
                                                      R"pbdoc(
      Represents and allows iteration over symmetry operations consistent
      with a given Supercell, combining pure factor group and pure
      translation operations.

    )pbdoc");

  // Configuration -- declare class
  py::class_<config::Configuration> pyConfiguration(m, "Configuration", R"pbdoc(
      A data structure encapsulating configuration DoF values and all
      information necessary to apply supercell factor group operations.

      Notes
      -----

      - Configuration may be copied with `copy.copy` or `copy.deepcopy`.

    )pbdoc");

  // ConfigurationWithProperties -- declare class
  py::class_<config::ConfigurationWithProperties> pyConfigurationWithProperties(
      m, "ConfigurationWithProperties", R"pbdoc(
      A data structure encapsulating a Configuration along with associated
      local and global continuous properties.

      Notes
      -----

      - The format for local and global properties follows the format for local and
        global continuous degrees of freedom (DoF) in the standard basis, as documented
        for `ConfigDoFValues <https://prisms-center.github.io/CASMcode_pydocs/libcasm/clexulator/2.0/usage/config_dof_values.html>`_
      - Scalar global properties, such as energy, are stored in a vector like other
        global properties, and can also be accessed using
        :func:`~libcasm.configuration.ConfigurationWithProperties.scalar_property`.
      - ConfigurationWithProperties may be copied with `copy.copy` or `copy.deepcopy`.

    )pbdoc");

  // SupercellSymOp -- define functions
  pySupercellSymOp
      .def(py::init(&make_supercell_symop), py::arg("supercell"),
           py::arg("supercell_factor_group_index"),
           py::arg("translation_index"), py::arg("translation_frac"),
           py::arg("translation_cart"),
           R"pbdoc(
      Construct a representation that allows applying symmetry to
      configurations in a particular supercell.

      Notes
      -----
      Only one of `translation_index`, `translation_frac`, or
      `translation_cart` should be provided.

      Parameters
      ----------
      supercell : libcasm.configuration.Supercell
          The supercell defining the periodicity of the configuration to
          be transformed.
      supercell_factor_group_index : int
          Index into the supercell factor group.
      translation_index : Optional[int] = None
          Linear index of translation to apply. Equivalent to linear
          unitcell_index.
      translation_frac : Optional[numpy.ndarray[numpy.int64[3,]]] = None
          Translation, as multiples of prim lattice vectors.
      translation_cart : Optional[numpy.ndarray[numpy.float64[3,]]] = None
          Translation, in Cartesian coordinates.
      )pbdoc")
      .def("supercell", &config::SupercellSymOp::supercell,
           "Return the supercell.")
      .def(
          "next", [](config::SupercellSymOp &op) { ++op; },
          "Transform this to represent the next operation in the supercell "
          "factor group.")
      .def_static("begin", &config::SupercellSymOp::begin,
                  "Construct a representation for the first operation in the "
                  "supercell factor group.")
      .def_static("end", &config::SupercellSymOp::end,
                  "Construct a representation for the past-the-last operation "
                  "in the supercell factor group.")
      .def_static("translation_begin",
                  &config::SupercellSymOp::translation_begin,
                  "Construct a representation for the first operation in the "
                  "set of supercell translations.")
      .def_static("translation_end", &config::SupercellSymOp::translation_end,
                  "Construct a representation for the past-the-last operation "
                  "in the set of supercell translations.")
      .def("supercell_factor_group_index",
           &config::SupercellSymOp::supercell_factor_group_index,
           "Index into the supercell factor group of the element applied by "
           "this supercell factor group operation.")
      .def("prim_factor_group_index",
           &config::SupercellSymOp::prim_factor_group_index,
           "Index into the prim factor group of the element applied by this "
           "supercell factor group operation.")
      .def("translation_index", &config::SupercellSymOp::translation_index,
           "Index of the translation applied by this supercell factor group "
           "operation.")
      .def("translation_frac", &config::SupercellSymOp::translation_frac,
           "The translation applied by this supercell factor group operation, "
           "in fractional coordinates relative to the prim lattice vectors.")
      .def("permute_index", &config::SupercellSymOp::permute_index,
           py::arg("i"),
           "Returns the index of the site containing the site DoF values that "
           "will be permuted onto site i")
      .def("to_symop", &config::SupercellSymOp::to_symop,
           "Return the SymOp for the current operation")
      .def("combined_permute", &config::SupercellSymOp::combined_permute,
           "Returns the combination of factor group operation permutation and "
           "translation permutation")
      .def("inverse", &config::SupercellSymOp::inverse,
           "Returns the inverse supercell operation")
      .def(
          "__mul__",
          [](config::SupercellSymOp const &self,
             config::SupercellSymOp const &rhs) { return self * rhs; },
          py::arg("rhs"),
          "Return the supercell operation equivalent to applying first rhs and "
          "then this.")
      .def(py::self < py::self,
           "Sorts SupercellSymOp. Only SupercellSymOp with the same supercell "
           "can be compared.")
      .def(py::self <= py::self,
           "Sorts SupercellSymOp. Only SupercellSymOp with the same supercell "
           "can be compared.")
      .def(py::self > py::self,
           "Sorts SupercellSymOp. Only SupercellSymOp with the same supercell "
           "can be compared.")
      .def(py::self >= py::self,
           "Sorts SupercellSymOp. Only SupercellSymOp with the same supercell "
           "can be compared.")
      .def(py::self == py::self,
           "True if SupercellSymOp are equal. Only SupercellSymOp with the "
           "same supercell can be compared.")
      .def(py::self != py::self,
           "True if SupercellSymOp are not equal. Only SupercellSymOp with the "
           "same supercell can be compared.")
      .def(
          "__mul__",
          [](config::SupercellSymOp const &self,
             config::Configuration const &configuration) {
            return copy_apply(self, configuration);
          },
          py::arg("configuration"),
          "Creates a copy of the configuration and applies the symmetry "
          "operation represented by this SupercellSymOp to its degree of "
          "freedom "
          "(DoF) values.")
      .def(
          "__mul__",
          [](config::SupercellSymOp const &self,
             config::ConfigurationWithProperties const &configuration) {
            return copy_apply(self, configuration);
          },
          py::arg("configuration"),
          "Creates a copy of the configuration and applies the symmetry "
          "operation represented by this SupercellSymOp to its degree of "
          "freedom (DoF) values and properties.")
      .def(
          "__mul__",
          [](config::SupercellSymOp const &self,
             xtal::UnitCellCoord const &integral_site_coordinate) {
            return copy_apply(self, integral_site_coordinate);
          },
          py::arg("integral_site_coordinate"),
          "Creates a copy of `integral_site_coordinate` and applies the "
          "symmetry operation represented by this SupercellSymOp.");

  // Configuration -- define functions
  pyConfiguration
      .def(py::init<std::shared_ptr<config::Supercell const> const &>(),
           py::arg("supercell"),
           R"pbdoc(
      Construct a default-valued Configuration

      Parameters
      ----------
      supercell : libcasm.configuration.Supercell
          The supercell defining the periodicity of the configuration.
      )pbdoc")
      .def(
          "supercell",
          [](config::Configuration const &configuration) {
            return configuration.supercell;
          },
          "Returns the internal shared "
          ":class:`~libcasm.configuration.Supercell`")
      .def(
          "set_dof_values",
          [](config::Configuration &self,
             clexulator::ConfigDoFValues const &other) {
            self.dof_values = other;
          },
          "Assign all values from other, using copy", py::arg("other"))
      .def(
          "dof_values",
          [](config::Configuration const &self) { return self.dof_values; },
          "Return a copy of ConfigDoFValues")
      .def(
          "dof_values_ptr",
          [](config::Configuration &self) { return &self.dof_values; },
          "Return a pointer to the ConfigDoFValues")
      .def(
          "occupation",
          [](config::Configuration const &configuration)
              -> Eigen::VectorXi const & {
            return configuration.dof_values.occupation;
          },
          py::return_value_policy::reference_internal,
          "Returns the site occupation values, as indices into the allowed "
          "occupants on the corresponding basis site, as a const reference.")
      .def(
          "set_occupation",
          [](config::Configuration &configuration,
             Eigen::Ref<Eigen::VectorXi const> occupation) {
            if (occupation.size() !=
                configuration.dof_values.occupation.size()) {
              throw std::runtime_error(
                  "Error in Configuration.set_occupation: occupation vector "
                  "size may not be changed");
            }
            return configuration.dof_values.occupation = occupation;
          },
          "Sets the site occupation values. Changing the size of the "
          "occupation vector results in an exception.")
      .def(
          "occ",
          [](config::Configuration const &configuration, Index l) -> int {
            return configuration.dof_values.occupation(l);
          },
          py::arg("l"),
          "Returns the site occupation value on the specified site, using a "
          "copy.")
      .def(
          "set_occ",
          [](config::Configuration &configuration, Index l, int s) {
            configuration.dof_values.occupation(l) = s;
          },
          py::arg("l"), py::arg("s"),
          "Set the site occupation value on site `l` to value `s`. Values are "
          "not checked for validity, but `l` is expected to be in range `[0, "
          "supercell.n_sites())`, `s` is expected to be in range `[0, "
          "supercell.n_occupants()[l])`.")
      .def(
          "global_dof_values",
          [](config::Configuration const &configuration,
             std::string key) -> Eigen::VectorXd const & {
            return configuration.dof_values.global_dof_values.at(key);
          },
          py::return_value_policy::reference_internal, py::arg("key"),
          "Returns global DoF values of type `key`, in the prim basis, as a "
          "const reference.")
      .def(
          "global_standard_dof_values",
          [](config::Configuration const &configuration,
             std::string key) -> Eigen::VectorXd {
            auto const &prim = configuration.supercell->prim;
            return clexulator::global_to_standard_values(
                configuration.dof_values.global_dof_values.at(key),
                prim->global_dof_info.at(key));
          },
          py::arg("key"),
          "Returns global DoF values of type `key`, in the standard basis, as "
          "a copy.")
      .def(
          "set_global_dof_values",
          [](config::Configuration &configuration, std::string key,
             Eigen::Ref<Eigen::VectorXd const> dof_values) {
            Eigen::VectorXd &curr_dof_values =
                configuration.dof_values.global_dof_values.at(key);
            if (curr_dof_values.size() != dof_values.size()) {
              throw std::runtime_error(
                  "Error in set_global_dof_values: size may not be changed");
            }
            return curr_dof_values = dof_values;
          },
          py::arg("key"), py::arg("dof_values"),
          "Set global DoF values of type `key`, in the prim basis, using a "
          "copy.")
      .def(
          "set_global_standard_dof_values",
          [](config::Configuration &configuration, std::string key,
             Eigen::Ref<Eigen::VectorXd const> standard_dof_values) {
            auto const &prim = configuration.supercell->prim;
            Eigen::VectorXd &curr_dof_values =
                configuration.dof_values.global_dof_values.at(key);
            curr_dof_values = clexulator::global_from_standard_values(
                standard_dof_values, prim->global_dof_info.at(key));
          },
          py::arg("key"), py::arg("standard_dof_values"),
          "Set global DoF values of type `key`, in the standard basis, using a "
          "copy.")
      .def(
          "local_dof_values",
          [](config::Configuration const &configuration,
             std::string key) -> Eigen::MatrixXd const & {
            return configuration.dof_values.local_dof_values.at(key);
          },
          py::return_value_policy::reference_internal, py::arg("key"),
          "Returns local DoF values of type `key`, in the prim basis, as a "
          "const reference.")
      .def(
          "local_standard_dof_values",
          [](config::Configuration const &configuration,
             std::string key) -> Eigen::MatrixXd {
            auto const &supercell = configuration.supercell;
            auto const &prim = supercell->prim;
            auto const &xtal_prim = prim->basicstructure;
            Index N_sublat = xtal_prim->basis().size();
            Index N_unitcells =
                supercell->unitcell_index_converter.total_sites();
            return clexulator::local_to_standard_values(
                configuration.dof_values.local_dof_values.at(key), N_sublat,
                N_unitcells, prim->local_dof_info.at(key));
          },
          py::arg("key"),
          "Returns local DoF values of type `key`, in the standard basis, as a "
          "copy.")
      .def(
          "set_local_dof_values",
          [](config::Configuration &configuration, std::string key,
             Eigen::Ref<Eigen::MatrixXd const> dof_values) {
            Eigen::MatrixXd &curr_dof_values =
                configuration.dof_values.local_dof_values.at(key);
            if (curr_dof_values.rows() != dof_values.rows()) {
              throw std::runtime_error(
                  "Error in set_local_dof_values: number of rows may not be "
                  "changed");
            }
            if (curr_dof_values.cols() != dof_values.cols()) {
              throw std::runtime_error(
                  "Error in set_local_dof_values: number of cols may not be "
                  "changed");
            }
            return curr_dof_values = dof_values;
          },
          py::arg("key"), py::arg("dof_values"),
          "Set local DoF values of type `key`, in the prim basis, using a "
          "copy.")
      .def(
          "set_local_standard_dof_values",
          [](config::Configuration &configuration, std::string key,
             Eigen::Ref<Eigen::MatrixXd const> standard_dof_values) {
            auto const &supercell = configuration.supercell;
            auto const &prim = supercell->prim;
            auto const &xtal_prim = prim->basicstructure;
            Index N_sublat = xtal_prim->basis().size();
            Index N_unitcells =
                supercell->unitcell_index_converter.total_sites();
            Eigen::MatrixXd &curr_dof_values =
                configuration.dof_values.local_dof_values.at(key);
            curr_dof_values = clexulator::local_from_standard_values(
                standard_dof_values, N_sublat, N_unitcells,
                prim->local_dof_info.at(key));
          },
          py::arg("key"), py::arg("standard_dof_values"),
          "Set local DoF values of type `key`, in the standard basis, using a "
          "copy.")
      .def(
          "local_dof_site_value",
          [](config::Configuration const &configuration, std::string key,
             Index l) {
            return configuration.dof_values.local_dof_values.at(key).col(l);
          },
          py::arg("key"), py::arg("l"),
          "Returns local DoF values of type `key`, in the prim basis, on site "
          "`l`, using a copy.")
      .def(
          "set_local_dof_site_value",
          [](config::Configuration &configuration, std::string key, Index l,
             Eigen::Ref<Eigen::VectorXd const> site_dof_value) {
            configuration.dof_values.local_dof_values.at(key).col(l) =
                site_dof_value;
          },
          py::arg("key"), py::arg("l"), py::arg("site_dof_value"),
          "Set the local DoF values of type `key`, in the prim basis, on site "
          "`l`, using a copy.")
      .def(
          "local_standard_dof_site_value",
          [](config::Configuration const &configuration, std::string key,
             Index l) {
            auto const &prim = configuration.supercell->prim;
            auto const &converter =
                configuration.supercell->unitcellcoord_index_converter;
            Index b = converter(l).sublattice();
            auto const &dof_info = prim->local_dof_info.at(key);
            auto const &M = configuration.dof_values.local_dof_values.at(key);
            return dof_info[b].basis() * M.col(l).head(dof_info[b].dim());
          },
          py::arg("key"), py::arg("l"),
          "Returns local DoF values of type `key`, in the standard basis, on "
          "site `l`, using a copy.")
      .def(
          "set_local_standard_dof_site_value",
          [](config::Configuration &configuration, std::string key, Index l,
             Eigen::Ref<Eigen::VectorXd const> standard_site_dof_value) {
            auto const &prim = configuration.supercell->prim;
            auto const &converter =
                configuration.supercell->unitcellcoord_index_converter;
            Index b = converter(l).sublattice();
            auto const &dof_info = prim->local_dof_info.at(key);
            auto &M = configuration.dof_values.local_dof_values.at(key);
            M.col(l).head(dof_info[b].dim()) =
                dof_info[b].inv_basis() * standard_site_dof_value;
          },
          py::arg("key"), py::arg("l"), py::arg("standard_site_dof_value"),
          "Set the local DoF values of type `key`, in the standard basis, on "
          "site `l`, using a copy.")
      .def(py::self < py::self,
           "Sorts configurations, first by supercell, then global DoF, then "
           "occupation DoF, then local continuous DoF. Only configurations "
           "with the same prim can be compared.")
      .def(py::self <= py::self,
           "Sorts configurations, first by supercell, then global DoF, then "
           "occupation DoF, then local continuous DoF. Only configurations "
           "with the same prim can be compared.")
      .def(py::self > py::self,
           "Sorts configurations, first by supercell, then global DoF, then "
           "occupation DoF, then local continuous DoF. Only configurations "
           "with the same prim can be compared.")
      .def(py::self >= py::self,
           "Sorts configurations, first by supercell, then global DoF, then "
           "occupation DoF, then local continuous DoF. Only configurations "
           "with the same prim can be compared.")
      .def(py::self == py::self,
           "True if configurations are equal, or approximately equal up the "
           "lattice tolerance if there continuous DoF. Only configurations "
           "with the same prim can be compared.")
      .def(py::self != py::self,
           "True if configurations are equal, or approximately equal up the "
           "lattice tolerance if there continuous DoF. Only configurations "
           "with the same prim can be compared.")
      .def("__copy__",
           [](config::Configuration const &self) {
             return config::Configuration(self);
           })
      .def("__deepcopy__", [](config::Configuration const &self,
                              py::dict) { return config::Configuration(self); })
      .def_static(
          "from_dict",
          [](const nlohmann::json &data,
             std::shared_ptr<config::SupercellSet> supercells) {
            jsonParser json{data};
            InputParser<config::Configuration> parser(json, *supercells);
            std::runtime_error error_if_invalid{
                "Error in libcasm.configuration.Configuration.from_dict"};
            report_and_throw_if_invalid(parser, CASM::log(), error_if_invalid);
            return std::move(*parser.value);
          },
          R"pbdoc(
        Construct a Configuration from a Python dict

        The `Configuration reference <https://prisms-center.github.io/CASMcode_docs/formats/casm/clex/Configuration/>`_ documents the expected format for Configurations and Supercells."

        Parameters
        ----------
        data : dict
            A :class:`~libcasm.configuration.Supercell` as a dict.
        supercells : libcasm.configuration.SupercellSet
            A :class:`~libcasm.configuration.SupercellSet`, which holds shared
            supercells in order to avoid duplicates.

        Returns
        -------
        configuration : libcasm.configuration.Configuration
            The :class:`~libcasm.configuration.Configuration` constructed from the dict.
        )pbdoc",
          py::arg("data"), py::arg("supercells"))
      .def(
          "to_dict",
          [](config::Configuration const &self) {
            jsonParser json;
            to_json(self, json);
            return static_cast<nlohmann::json>(json);
          },
          "Represent the Configuration as a Python dict. The `Configuration "
          "reference "
          "<https://prisms-center.github.io/CASMcode_docs/formats/casm/clex/"
          "Configuration/>`_ documents the expected format for Configurations "
          "and Supercells.")
      .def_static(
          "from_structure",
          [](std::shared_ptr<config::Prim const> prim,
             xtal::SimpleStructure const &structure, std::string converter,
             std::optional<std::shared_ptr<config::SupercellSet>>
                 opt_supercells) {
            std::shared_ptr<config::SupercellSet> supercells;
            if (opt_supercells.has_value() &&
                opt_supercells.value() != nullptr) {
              supercells = opt_supercells.value();
            }

            if (converter == "isotropic_atomic") {
              config::FromIsotropicAtomicStructure f(prim, supercells);
              return f(structure).configuration;
            } else {
              std::stringstream ss;
              ss << "Error in Configuration.from_structure: Unknown converter: "
                 << "\" " << converter << "\".";
              throw std::runtime_error(ss.str());
            }
          },
          R"pbdoc(
          Construct a Configuration from a Structure

          This method is equivalent to
          :func:`ConfigurationWithProperties.from_structure`, but only the
          :class:`Configuration` is kept.
          )pbdoc",
          py::arg("prim"), py::arg("structure"),
          py::arg("converter") = std::string("isotropic_atomic"),
          py::arg("supercells") = std::nullopt)
      .def(
          "to_structure",
          [](config::Configuration const &self, std::string converter) {
            config::ConfigurationWithProperties configuration(self);
            if (converter == "atomic") {
              config::ToAtomicStructure f;
              return f(configuration);
            } else {
              std::stringstream ss;
              ss << "Error in Configuration.to_structure: Unknown converter: "
                 << "\" " << converter << "\".";
              throw std::runtime_error(ss.str());
            }
          },
          R"pbdoc(
          Construct a Structure from a Configuration

          This method is equivalent to \
          :func:`ConfigurationWithProperties.to_structure`,
          but no additional properties are included in the resulting
          :class:`~libcasm.xtal.Structure`.
          )pbdoc",
          py::arg("converter") = std::string("atomic"));

  // ConfigurationWithProperties -- define functions
  pyConfigurationWithProperties
      .def(py::init<config::Configuration const &,
                    std::map<std::string, Eigen::MatrixXd> const &,
                    std::map<std::string, Eigen::VectorXd> const &>(),
           py::arg("configuration"),
           py::arg("local_properties") =
               std::map<std::string, Eigen::MatrixXd>(),
           py::arg("global_properties") =
               std::map<std::string, Eigen::VectorXd>(),
           R"pbdoc(
      Construct a ConfigurationWithProperties

      Parameters
      ----------
      configuration : libcasm.configuration.Configuration
          The configuration.
      local_properties : dict[str,numpy.ndarray[numpy.float64[matrix_dim, n_sites]]] = {}
          Local continuous property values, as two-dimensional floating-point arrays
          (value), by property type (key), with one column of values
          for each in the supercell. To be transformed by symmetry operations,
          the keys must be CASM-supported property types and values are expected
          to be in the standard basis.
      global_properties : dict[str,numpy.ndarray[numpy.float64[vector_dim, 1]]] = {}
          Global continuous property values, as one-dimensional floating-point arrays
          (value), accessed by property type (key). To be transformed by symmetry
          operations, the keys must be CASM-supported property types and values are
          expected to be in the standard basis.
      )pbdoc")
      .def_readonly("configuration",
                    &config::ConfigurationWithProperties::configuration,
                    py::return_value_policy::reference_internal,
                    R"pbdoc(
          Access the configuration.
          )pbdoc")
      .def_readonly("local_properties",
                    &config::ConfigurationWithProperties::local_properties,
                    py::return_value_policy::reference_internal,
                    R"pbdoc(
          dict[str,numpy.ndarray[numpy.float64[matrix_dim, n_sites]]]: \
          Access the local properties.
          )pbdoc")
      .def(
          "local_property_values",
          [](config::ConfigurationWithProperties const &configuration,
             std::string key) -> Eigen::MatrixXd const & {
            return configuration.local_properties.at(key);
          },
          py::return_value_policy::reference_internal, R"pbdoc(
          numpy.ndarray[numpy.float64[matrix_dim, n_sites]]: Local property values of type `key`, as a const reference.
          )pbdoc",
          py::arg("key"))
      .def_readonly("global_properties",
                    &config::ConfigurationWithProperties::global_properties,
                    py::return_value_policy::reference_internal,
                    R"pbdoc(
          dict[str,numpy.ndarray[numpy.float64[vector_dim, 1]]]: \
          Access the global properties.
          )pbdoc")
      .def(
          "global_property_values",
          [](config::ConfigurationWithProperties const &configuration,
             std::string key) -> Eigen::VectorXd const & {
            return configuration.global_properties.at(key);
          },
          R"pbdoc(
          numpy.ndarray[numpy.float64[vector_dim, 1]]: Global property values of type `key`, as a const reference.
          )pbdoc",
          py::return_value_policy::reference_internal, py::arg("key"))
      .def(
          "scalar_global_property_value",
          [](config::ConfigurationWithProperties const &configuration,
             std::string key) -> double {
            Eigen::VectorXd const &v = configuration.global_properties.at(key);
            if (v.size() != 1) {
              std::stringstream ss;
              ss << "Error in "
                    "ConfigurationWithProperties.scalar_global_property: "
                 << "key=" << key << " is not a scalar property";
              throw std::runtime_error(ss.str());
            }
            return v(0);
          },
          R"pbdoc(
          float: Scalar global property value.
          )pbdoc",
          py::arg("key"))
      .def("__copy__",
           [](config::ConfigurationWithProperties const &self) {
             return config::ConfigurationWithProperties(self);
           })
      .def("__deepcopy__",
           [](config::ConfigurationWithProperties const &self, py::dict) {
             return config::ConfigurationWithProperties(self);
           })
      .def_static(
          "from_dict",
          [](const nlohmann::json &data,
             std::shared_ptr<config::SupercellSet> supercells) {
            jsonParser json{data};
            InputParser<config::ConfigurationWithProperties> parser(
                json, *supercells);
            std::runtime_error error_if_invalid{
                "Error in "
                "libcasm.configuration.ConfigurationWithProperties.from_dict"};
            report_and_throw_if_invalid(parser, CASM::log(), error_if_invalid);
            return std::move(*parser.value);
          },
          "Construct a ConfigurationWithProperties from a Python dict.",
          R"pbdoc(
        Construct a ConfigurationWithProperties from a Python dict

        Parameters
        ----------
        data : dict
            A :class:`~libcasm.configuration.Supercell` as a dict.
        supercells : libcasm.configuration.SupercellSet
            A :class:`~libcasm.configuration.SupercellSet`, which holds shared
            supercells in order to avoid duplicates.

        Returns
        -------
        configuration_with_properties : libcasm.configuration.ConfigurationWithProperties
            The :class:`~libcasm.configuration.ConfigurationWithProperties` constructed from the dict.
        )pbdoc",
          py::arg("data"), py::arg("supercells"))
      .def(
          "to_dict",
          [](config::ConfigurationWithProperties const &self) {
            jsonParser json;
            to_json(self, json);
            return static_cast<nlohmann::json>(json);
          },
          "Represent the ConfigurationWithProperties as a Python dict.")
      .def_static(
          "from_structure",
          [](std::shared_ptr<config::Prim const> prim,
             xtal::SimpleStructure const &structure, std::string converter,
             std::optional<std::shared_ptr<config::SupercellSet>>
                 opt_supercells) {
            std::shared_ptr<config::SupercellSet> supercells;
            if (opt_supercells.has_value() &&
                opt_supercells.value() != nullptr) {
              supercells = opt_supercells.value();
            }

            if (converter == "isotropic_atomic") {
              config::FromIsotropicAtomicStructure f(prim, supercells);
              return f(structure);
            } else {
              std::stringstream ss;
              ss << "Error in Configuration.from_structure: Unknown converter: "
                 << "\" " << converter << "\".";
              throw std::runtime_error(ss.str());
            }
          },
          R"pbdoc(
          Construct a ConfigurationWithProperties from a Structure

          This method is designed to be used with a mapped structure
          generated from :func:`~libcasm.mapping.methods.map_structures`
          and :func:`~libcasm.mapping.methods.make_mapped_structure` or
          the equivalent, meaning that atoms and atom properties are in
          the same order as the supercell sites they are mapped to and
          all properties (including the coordinates, displacements,
          and lattice vectors) are rotated so that they can be directly
          copied to configuration DoF or properties.

          If `structure` has a global strain property (i.e. "Ustrain",
          "Hstrain", "GLstrain", etc.) it must be of a type recognized by
          CASM and it is interpreted as the strain applied to the ideal
          lattice vectors to result in the structure's lattice vectors.
          The strain property is read and converted to :math:`U`, the
          right stretch tensor (see :class:`~libcasm.xtal.StrainConverter`).

          Then, the ideal supercell lattice vectors, as column vector
          matrix :math:`S`, are solved for from the lattice vectors
          of `structure`, column vector matrix :math:`L^{mapped}`,
          using :math:`L^{mapped} = U S`. For this method, it is
          required that `S = P T`, where :math:`P` is the prim
          lattice vectors as a column vector matrix and :math:`T` is
          an integer transformation matrix. If :math:`T` is not found
          to be integer, an exception will be thrown.

          When interpreting strain and displacement properties of `structure`,
          the convention in CASM is that displacements are applied to ideal
          coordinates before strain deformation is applied to the displaced
          coordinates. See the CASM `Degrees of Freedom (DoF) and Properties`_
          documentation for the full list of supported properties and their
          definitions.

          .. _`Degrees of Freedom (DoF) and Properties`: https://prisms-center.github.io/CASMcode_docs/formats/dof_and_properties/


          Parameters
          ----------
          prim : :class:`~libcasm.configuration.Prim`
              The Prim.
          structure : :class:`~libcasm.xtal.Structure`
              A :class:`~libcasm.xtal.Structure` which has been mapped to a
              supercell of `prim`.
          converter : str = "isotropic_atomic"
              The converter to use for generating the configuration. Options are
              currently limited to one:

              - "isotropic_atomic": Conversion is performed using
                a method which is limited to prim with isotropic atomic occupants.

          supercells : Optional[:class:`~libcasm.configuration.SupercellSet`] = None
              An optional :class:`~libcasm.configuration.SupercellSet`, in which
              to hold the shared supercell of the generated configuration in order
              to avoid duplicates.

          Returns
          -------
          configuration_with_properties : :class:`ConfigurationWithProperties`
              The :class:`ConfigurationWithProperties` constructed from the structure.
          )pbdoc",
          py::arg("prim"), py::arg("structure"),
          py::arg("converter") = std::string("isotropic_atomic"),
          py::arg("supercells") = std::nullopt)
      .def(
          "to_structure",
          [](config::ConfigurationWithProperties const &self,
             std::string converter) {
            if (converter == "atomic") {
              config::ToAtomicStructure f;
              return f(self);
            } else {
              std::stringstream ss;
              ss << "Error in Configuration.to_structure: Unknown converter: "
                 << "\" " << converter << "\".";
              throw std::runtime_error(ss.str());
            }
          },
          R"pbdoc(
          Construct a Structure from a ConfigurationWithProperties

          Parameters
          ----------
          converter : str = "atomic"
              The converter to use for generating the structure. Options are
              currently limited to one:

              - "atomic": Conversion is supported for configurations with prim
                that only have atomic occupants and generates structure with only
                atom types and properties. Fixed species properties of occupants are
                ignored.

                If `"disp"` is a degree of freedom (DoF), it is included in the
                structure's atomic coordinates, but not included in the structure's
                atom properties. If strain is a DoF, it is included in the
                structure's atomic coordinates, and the structure's lattice vectors,
                and not included in the structure's global properties. Other DoF are
                copied to the structure's atom or global properties.

                The deformation gradient applied to ideal lattice
                vectors is obtained from one of the following, in order of preference:

                1) Strain DoF (this is not copied to the structure's global properties)
                2) "Ustrain" in global_properties (this is copied to the structure's \
                   global properties)
                3) The identify matrix, I


          Returns
          -------
          structure : :class:`~libcasm.xtal.Structure`
              The :class:`~libcasm.xtal.Structure` constructed from the
              :class:`~libcasm.configuration.ConfigurationWithProperties`.
          )pbdoc",
          py::arg("converter") = std::string("atomic"));

  m.def(
      "apply",
      [](config::SupercellSymOp const &op,
         config::Configuration &configuration) {
        return apply(op, configuration);
      },
      py::arg("supercell_symop"), py::arg("configuration"),
      "Applies the symmetry operation represented by the SupercellSymOp to "
      "transform the configuration's degree of freedom (DoF) values.");

  m.def(
      "copy_apply",
      [](config::SupercellSymOp const &op,
         config::Configuration const &configuration) {
        return copy_apply(op, configuration);
      },
      py::arg("supercell_symop"), py::arg("configuration"),
      "Creates a copy of the configuration and applies the symmetry "
      "operation represented by this SupercellSymOp to its degree of freedom "
      "(DoF) values.");

  m.def(
      "apply",
      [](config::SupercellSymOp const &op,
         config::ConfigurationWithProperties &configuration) {
        return apply(op, configuration);
      },
      py::arg("supercell_symop"), py::arg("configuration"),
      "Applies the symmetry operation represented by the SupercellSymOp to "
      "transform the configuration's degree of freedom (DoF) values"
      "and properties.");

  m.def(
      "copy_apply",
      [](config::SupercellSymOp const &op,
         config::ConfigurationWithProperties const &configuration) {
        return copy_apply(op, configuration);
      },
      py::arg("supercell_symop"), py::arg("configuration"),
      "Creates a copy of the configuration and applies the symmetry "
      "operation represented by this SupercellSymOp to its degree of freedom "
      "(DoF) values and properties.");

  m.def(
      "apply",
      [](config::SupercellSymOp const &op,
         xtal::UnitCellCoord &integral_site_coordinate) {
        return apply(op, integral_site_coordinate);
      },
      py::arg("supercell_symop"), py::arg("integral_site_coordinate"),
      "Applies the symmetry operation represented by the SupercellSymOp to "
      "transform `integral_site_coordinate`.");

  m.def(
      "copy_apply",
      [](config::SupercellSymOp const &op,
         xtal::UnitCellCoord const &integral_site_coordinate) {
        return copy_apply(op, integral_site_coordinate);
      },
      py::arg("supercell_symop"), py::arg("configuration"),
      "Creates a copy of `integral_site_coordinate` and applies the symmetry "
      "operation represented by this SupercellSymOp");

  m.def(
      "is_canonical_configuration",
      [](config::Configuration const &configuration,
         std::optional<config::SupercellSymOp> begin,
         std::optional<config::SupercellSymOp> end) {
        auto const &supercell = configuration.supercell;
        if (!begin.has_value()) {
          begin = config::SupercellSymOp::begin(supercell);
        }
        if (!end.has_value()) {
          end = config::SupercellSymOp::end(supercell);
        }
        return is_canonical(configuration, *begin, *end);
      },
      py::arg("configuration"), py::arg("begin") = std::nullopt,
      py::arg("end") = std::nullopt,
      "Return true if configuration is in canonical form, given the provided "
      "SupercellSymOp (default is the supercell factor group).");

  m.def(
      "make_canonical_configuration",
      [](config::Configuration const &configuration,
         bool in_canonical_supercell,
         std::optional<std::vector<config::SupercellSymOp>> subgroup) {
        if (in_canonical_supercell) {
          if (subgroup.has_value()) {
            throw std::runtime_error(
                "Error in make_canonical_configuration: "
                "`in_canonical_supercell` may not be used in combination with "
                "`subgroup`");
          }
          return make_in_canonical_supercell(configuration);
        } else if (subgroup.has_value()) {
          return make_canonical_form(configuration, subgroup->begin(),
                                     subgroup->end());
        } else {
          auto const &supercell = configuration.supercell;
          auto begin = config::SupercellSymOp::begin(supercell);
          auto end = config::SupercellSymOp::end(supercell);
          return make_canonical_form(configuration, begin, end);
        }
      },
      py::arg("configuration"), py::arg("in_canonical_supercell") = false,
      py::arg("subgroup") = std::nullopt,
      R"pbdoc(
      Return the canonical configuration

      The canonical configuration is the configuration which compares greater
      than all equivalent supercells given a symmetry group. By default, the
      supercell factor group is used. The parameter
      `in_canonical_supercell` can be used to specify that the supercell
      should also be made canonical. A subgroup of the supercell factor
      group may be used through the `subgroup` parameter, but not in combination
      with `in_canonical_supercell`.

      Parameters
      ----------
      configuration : libcasm.configuration.Configuration
          The initial configuration.
      in_canonical_supercell : bool, default=False
          If True, the canonical configuration is found in the
          canonical supercell. Otherwise the supercell is not changed.
      subgroup : Optional[List[libcasm.configuration.SupercellSymOp]] = None
          If provided, the canonical configuration will be found with
          respect to a subgroup of the supercell factor group instead of
          the complete supercell factor group. These operations are supercell
          specifici, so this parameter may not be used with
          `in_canonical_supercell == True`.
      )pbdoc");

  m.def(
      "to_canonical_configuration",
      [](config::Configuration const &configuration,
         std::optional<std::vector<config::SupercellSymOp>> subgroup) {
        if (subgroup.has_value()) {
          return to_canonical(configuration, subgroup->begin(),
                              subgroup->end());
        } else {
          auto const &supercell = configuration.supercell;
          auto begin = config::SupercellSymOp::begin(supercell);
          auto end = config::SupercellSymOp::end(supercell);
          return to_canonical(configuration, begin, end);
        }
      },
      py::arg("configuration"), py::arg("subgroup") = std::nullopt,
      "Return an operation that makes a configuration canonical with respect "
      "to the supercell factor group (default) or a subgroup of the supercell "
      "factor group.");

  m.def(
      "from_canonical_configuration",
      [](config::Configuration const &configuration,
         std::optional<std::vector<config::SupercellSymOp>> subgroup) {
        if (subgroup.has_value()) {
          return from_canonical(configuration, subgroup->begin(),
                                subgroup->end());
        } else {
          auto const &supercell = configuration.supercell;
          auto begin = config::SupercellSymOp::begin(supercell);
          auto end = config::SupercellSymOp::end(supercell);
          return from_canonical(configuration, begin, end);
        }
      },
      py::arg("configuration"), py::arg("subgroup") = std::nullopt,
      "Return an operation that makes a configuration from the canonical "
      "configuration with respect to the supercell factor group (default) or a "
      "subgroup of the supercell factor group.");

  m.def(
      "make_invariant_subgroup",
      [](config::Configuration const &configuration,
         std::optional<std::set<Index>> site_indices,
         std::optional<std::vector<config::SupercellSymOp>> group) {
        if (!site_indices.has_value()) {
          if (group.has_value()) {
            return make_invariant_subgroup(configuration, group->begin(),
                                           group->end());
          } else {
            auto const &supercell = configuration.supercell;
            auto begin = config::SupercellSymOp::begin(supercell);
            auto end = config::SupercellSymOp::end(supercell);
            return make_invariant_subgroup(configuration, begin, end);
          }
        } else {
          if (group.has_value()) {
            return make_invariant_subgroup(configuration, site_indices.value(),
                                           group->begin(), group->end());
          } else {
            auto const &supercell = configuration.supercell;
            auto begin = config::SupercellSymOp::begin(supercell);
            auto end = config::SupercellSymOp::end(supercell);
            return make_invariant_subgroup(configuration, site_indices.value(),
                                           begin, end);
          }
        }
      },
      py::arg("configuration"), py::arg("site_indices") = std::nullopt,
      py::arg("group") = std::nullopt,
      "Return the subgroup (as a List[libcasm.configuration.SupercellSymOp]) "
      "that leaves a configuration invariant. If `site_indices` are provided "
      "(a set of linear index of sites in the supercell), the subgroup is "
      "restricted such that it does not mix the given sites and other sites. "
      "By default, the subgroup is found with respect to the supercell factor "
      "group. Optionally, another `group` (itself a subgroup of the supercell "
      "factor group) may be provided.");

  m.def(
      "make_invariant_subgroup",
      [](std::set<Index> site_indices,
         std::optional<std::vector<config::SupercellSymOp>> group) {
        if (group.has_value()) {
          return make_invariant_subgroup(site_indices, group->begin(),
                                         group->end());
        } else {
          auto supercell = group->begin()->supercell();
          auto begin = config::SupercellSymOp::begin(supercell);
          auto end = config::SupercellSymOp::end(supercell);
          return make_invariant_subgroup(site_indices, begin, end);
        }
      },
      py::arg("site_indices"), py::arg("group") = std::nullopt,
      "Return the subgroup (as a List[libcasm.configuration.SupercellSymOp]) "
      "that does not mix the given sites (a set of linear index of sites in "
      "the supercell) and other sites. By default, the subgroup is found with "
      "respect to the supercell factor group. Optionally, another `group` "
      "(itself a subgroup of the supercell factor group) may be provided.");

  m.def(
      "make_equivalent_configurations",
      [](config::Configuration const &configuration,
         std::optional<std::vector<config::SupercellSymOp>> subgroup) {
        if (subgroup.has_value()) {
          return make_equivalents(configuration, subgroup->begin(),
                                  subgroup->end());
        } else {
          auto const &supercell = configuration.supercell;
          auto begin = config::SupercellSymOp::begin(supercell);
          auto end = config::SupercellSymOp::end(supercell);
          return make_equivalents(configuration, begin, end);
        }
      },
      py::arg("configuration"), py::arg("subgroup") = std::nullopt,
      "Return the distinct symmetrically equivalent configurations, with "
      "respect to the supercell factor group (default) or a subgroup of the "
      "supercell factor group.");

  m.def(
      "copy_configuration",
      [](config::Configuration const &motif,
         std::shared_ptr<config::Supercell const> const &supercell,
         Eigen::Vector3l origin) {
        return copy_configuration(motif, supercell, xtal::UnitCell(origin));
      },
      py::arg("motif"), py::arg("supercell"),
      py::arg("origin") = Eigen::Vector3l::Zero(),
      R"pbdoc(
      Copy motif configuration DoF values into a supercell

      Parameters
      ----------
      motif : libcasm.configuration.Configuration
          The initial configuration, with DoF values to be filled into the supercell.
      supercell : libcasm.configuration.Supercell
          The supercell to be filled by the motif configuration.
      origin : array_like of int, shape=(3,)
          The UnitCell indicating which unit cell in the initial configuration
          is the origin in new configuration
      )pbdoc");

  m.def(
      "copy_transformed_configuration",
      [](Index prim_factor_group_index, Eigen::Vector3l const &translation,
         config::Configuration const &motif,
         std::shared_ptr<config::Supercell const> const &supercell,
         Eigen::Vector3l origin) {
        return copy_configuration(prim_factor_group_index, translation, motif,
                                  supercell, xtal::UnitCell(origin));
      },
      py::arg("prim_factor_group_index"), py::arg("translation"),
      py::arg("motif"), py::arg("supercell"),
      py::arg("origin") = Eigen::Vector3l::Zero(),
      R"pbdoc(
      Copy transformed motif configuration DoF values into a supercell

      Copies DoF values as if `motif` is transformed by the prim factor group
      operation with index `factor_group_index`, then translated by
      `translation`, then copied starting from `origin`. In other words, sites
      map according to:

          new_config_unitcellcoord + origin = fg * motif_unitcellcoord + trans


      Parameters
      ----------
      prim_factor_group_index : int
          Index of prim factor group operation which transforms the initial
          configuration
      translation : array_like of int, shape=(3,)
          Lattice translation applied after the prim factor group operation.
      motif : libcasm.configuration.Configuration
          The initial configuration, with DoF values to be filled into the supercell.
      supercell : libcasm.configuration.Supercell
          The supercell to be filled by the motif configuration.
      origin : array_like of int, shape=(3,)
          The UnitCell indicating which unit cell in the initial configuration
          is the origin in new configuration
      )pbdoc");

  m.def(
      "make_all_super_configurations",
      [](config::Configuration const &motif,
         std::shared_ptr<config::Supercell const> const &supercell) {
        return config::make_all_super_configurations(motif, supercell);
      },
      py::arg("motif"), py::arg("supercell"),
      R"pbdoc(
      Make all equivalent configurations with respect to the prim factor group
      that fill a supercell

      Parameters
      ----------
      motif : libcasm.configuration.Configuration
          The initial configuration, with DoF values to be filled into the supercell.
      supercell : libcasm.configuration.Supercell
          The supercell to be filled by the motif configuration.

      Returns
      -------
      super_configurations : List[libcasm.configuration.Configuration]
          All configurations equivalent with respect to the prim factor
          group which fit in the given supercell.
      )pbdoc");

  m.def("is_primitive_configuration", &config::is_primitive,
        py::arg("configuration"),
        "Return true if no translations within the supercell result in the "
        "same configuration");

  m.def(
      "make_primitive_configuration",
      [](config::Configuration const &configuration) {
        return config::make_primitive(configuration);
      },
      py::arg("configuration"),
      "Return the primitive configuration. Does not apply any symmetry "
      "operations. Use `make_canonical_configuration` with "
      "`in_canonical_supercell=True` aftwards to obtain the "
      "primitive canonical configuration in the canonical supercell.");

  m.def(
      "make_global_dof_matrix_rep",
      [](std::vector<config::SupercellSymOp> const &group, config::DoFKey key) {
        std::shared_ptr<config::SymGroup const> symgroup;
        return config::make_global_dof_matrix_rep(group, key, symgroup);
      },
      py::arg("group"), py::arg("key"),
      "Make the matrix representation of `group` that describes the "
      "transformation of a particular global DoF, specified by `key`");

  m.def(
      "make_local_dof_matrix_rep",
      [](std::vector<config::SupercellSymOp> const &group, config::DoFKey key,
         std::set<Index> const &site_indices) {
        std::shared_ptr<config::SymGroup const> symgroup;
        return config::make_local_dof_matrix_rep(group, key, site_indices,
                                                 symgroup);
      },
      py::arg("group"), py::arg("key"), py::arg("site_indices"),
      "Make the matrix representation of `group` that describes the "
      "transformation of a particular local DoF, specified by `key` "
      "(may be \"occ\") amongst a subset of supercell sites, "
      "specified by `site_indices` (a set of linear index of sites in "
      "the supercell).");

  m.def("make_dof_space_rep", &config::make_dof_space_rep, R"pbdoc(
      Make the matrix representation of a group for transforming values in the DoF
      space basis

      Parameters
      ----------
      group: list[:class:`~libcasm.configuration.SupercellSymOp`]
          The symmetry group, as a SupercellSymOp representation
      dof_space: :class:`~libcasm.clexulator.DoFSpace`
          A DoFSpace, with basis defining vectors in a subspace of the prim degree of
          freedom (DoF) basis, `x_subspace` according to
          ``x_prim = dof_space.basis @ x_subspace``, where `x_prim` is a vector in the
          prim DoF basis.

      Returns
      -------
      dof_space_rep: list[numpy.ndarray[numpy.float64[subspace_dim, subspace_dim]]]
          Elements, `M`, of `dof_space_rep` transform subspace vectors according to
          ``x_subspace_after = M @ x_subspace_before``.

      )pbdoc",
        py::arg("group"), py::arg("dof_space"));

  //
  py::class_<config::ConfigSpaceAnalysisResults>(m,
                                                 "ConfigSpaceAnalysisResults",
                                                 R"pbdoc(
      Holds results from :func:`~libcasm.configuration.config_space_analysis`.

    )pbdoc")
      .def(py::init(&make_ConfigSpaceAnalysisResults),
           "Construct ConfigSpaceAnalysisResults.",
           py::arg("standard_dof_space"), py::arg("equivalent_dof_values"),
           py::arg("equivalent_configurations"), py::arg("projector"),
           py::arg("eigenvalues"), py::arg("symmetry_adapted_dof_space"))
      .def_readonly("standard_dof_space",
                    &config::ConfigSpaceAnalysisResults::standard_dof_space,
                    ":class:`~libcasm.clexulator.DoFSpace`: The shared "
                    ":class:`~libcasm.clexulator.DoFSpace`")
      .def_readonly("equivalent_dof_values",
                    &config::ConfigSpaceAnalysisResults::equivalent_dof_values,
                    R"pbdoc(
          Dict[str,np.ndarray]: DoF values of all equivalent \
          configurations in the fully commensurate supercell, \
          expressed in the basis of the standard DoF space, \
          with key == input configuration identifier
          )pbdoc")
      .def_readonly(
          "equivalent_configurations",
          &config::ConfigSpaceAnalysisResults::equivalent_configurations,
          R"pbdoc(
          Dict[str,List[:class:`~libcasm.configuration.Configuration`]]: All \
          equivalent configurations in the fully commensurate supercell, with \
          key == input configuration identifier
          )pbdoc")
      .def_readonly("projector", &config::ConfigSpaceAnalysisResults::projector,
                    "np.ndarray: Projection matrix")
      .def_readonly("eigenvalues",
                    &config::ConfigSpaceAnalysisResults::eigenvalues,
                    "np.ndarray: Non-zero eigenvalues of projector")
      .def_readonly(
          "symmetry_adapted_dof_space",
          &config::ConfigSpaceAnalysisResults::symmetry_adapted_dof_space,
          ":class:`~libcasm.clexulator.DoFSpace`: Symmetry-adapted config "
          "space, with basis formed by eigenvectors of P.");

  m.def("config_space_analysis", &config::config_space_analysis,
        R"pbdoc(
      Construct symmetry adapted bases in the DoF space spanned by the set of
      configurations symmetrically equivalent to the input configurations

      This method:

      - Constructs a projector onto the DoF space spanned by all configurations
        symmetrically equivalent to a set of input configurations, and
      - Finds the eigenvectors spanning that space. The eigenvectors are axes that
        can be used as a basis for symmetry adapted order parameters.

      This method is faster than the function `dof_space_analysis`, and
      often the resulting axes do lie along high-symmetry directions, but
      they may not lie within a single irreducible subspace, and they are
      not explicitly rotated to the highest symmetry directions.

      Parameters
      ----------
      configurations : Dict[str,:class:`~libcasm.configuration.Configuration`]
          Map of identifier string (key) to
          :class:`~libcasm.configuration.Configuration`, providing the
          configurations defining the DoF vector space to be spanned by the
          symmetry adapated bases that are constructed.
      dofs : Optional[list[str]] = None
          Names of degree of freedoms for which the analysis is run. The default
          includes all DoF types in the prim.
      exclude_homogeneous_modes : Optional[bool] = None
          Exclude homogeneous modes if this is true, or include if this is false.
          If this is None (default), exclude homogeneous modes for dof==\"disp\" only.
      include_default_occ_modes : bool = False
          Include the dof component for the default occupation value on each site
          with occupation DoF. The default is to exclude these modes because they
          are not independent. This parameter is only checked dof==\"occ\". If
          false, the default occupation is determined using
          `site_index_to_default_occ` if that is provided, else using
          `sublattice_index_to_default_occ` if that is provided, else using
          occupation index 0.
      sublattice_index_to_default_occ: Optional[dict[int,int]]
          Optional values of default occupation index (the value), specified by
          sublattice index (the key).
      site_index_to_default_occ: Optional[dict[int,int]]
          Optional values of default occupation index (the value), specified by
          supercell site index (the key).
      tol : float = libcasm.TOL
          Tolerance used for identifying zero-valued eigenvalues.

      Returns
      -------
      results : Dict[str,:class:`~libcasm.configuration.ConfigSpaceAnalysisResults`]
          Results including equivalent DoF values and configurations, projection
          matrix, eigenvalues, and symmetry adapted configuration space, for each
          requested DoF type.
      )pbdoc",
        py::arg("configurations"), py::arg("dofs") = std::nullopt,
        py::arg("exclude_homogeneous_modes") = std::nullopt,
        py::arg("include_default_occ_modes") = false,
        py::arg("sublattice_index_to_default_occ") = std::nullopt,
        py::arg("site_index_to_default_occ") = std::nullopt,
        py::arg("tol") = CASM::TOL);

  //
  py::class_<config::DoFSpaceAnalysisResults>(m, "DoFSpaceAnalysisResults",
                                              R"pbdoc(
      Holds results from :func:`~libcasm.configuration.dof_space_analysis`.

      )pbdoc")
      .def(py::init<clexulator::DoFSpace, irreps::VectorSpaceSymReport>(),
           "Construct DoFSpaceAnalysisResults.",
           py::arg("symmetry_adapted_dof_space"), py::arg("symmetry_report"))
      .def_readonly(
          "symmetry_adapted_dof_space",
          &config::DoFSpaceAnalysisResults::symmetry_adapted_dof_space,
          ":class:`~libcasm.clexulator.DoFSpace`: The symmetry adapated "
          ":class:`~libcasm.clexulator.DoFSpace`")
      .def_readonly("symmetry_report",
                    &config::DoFSpaceAnalysisResults::symmetry_report,
                    ":class:`~libcasm.irreps.VectorSpaceSymReport`: Holds the "
                    "irreducible space decomposition");

  m.def(
      "dof_space_analysis",
      [](clexulator::DoFSpace const &dof_space,
         std::shared_ptr<config::Prim const> prim,
         std::optional<config::Configuration> configuration,
         std::optional<bool> exclude_homogeneous_modes,
         bool include_default_occ_modes,
         std::optional<std::map<int, int>> sublattice_index_to_default_occ,
         std::optional<std::map<Index, int>> site_index_to_default_occ,
         bool calc_wedges) -> config::DoFSpaceAnalysisResults {
        std::optional<Log> log = std::nullopt;
        // std::optional<Log> log = Log(std::cout, Log::debug, true);
        return config::dof_space_analysis(
            dof_space, prim, configuration, exclude_homogeneous_modes,
            include_default_occ_modes, sublattice_index_to_default_occ,
            site_index_to_default_occ, calc_wedges, log);
      },
      R"pbdoc(
      Construct symmetry adapted bases in a DoFSpace

      This method:

      - Constructs symmetry representation matrices describing the affect of applying
        symmetry operations on DoF values in the specified DoFSpace.
      - Performs an irreducible space decomposition to find invariant subspaces
      - Finds high symmetry directions in each subspace
      - Constructs a symmetry adapated basis, preferring to use basis vectors
        aligned along the high symmetry directions.

      This method is slower than the function `config_space_analysis`, but
      the resulting axes do lie along high-symmetry directions, and within a
      single irreducible subspace.

      Parameters
      ----------
      dof_space : :class:`~libcasm.clexulator.DoFSpace`
          The :class:`~libcasm.clexulator.DoFSpace` for which a symmetry
          adapted basis is constructed.
      prim : :class:`~libcasm.configuration.Prim`
          A :class:`~libcasm.configuration.Prim`, for symmetry representation
          information.
      configuration : Optional[:class:`~libcasm.configuration.Configuration`] = None
          If None, use the full symmetry of the DoFSpace. If has value, use the
          factor group of the provided configuration. For DoFSpace of occupant
          or local continuous DoF, this should have the same supercell as
          `dof_space`.
      exclude_homogeneous_modes : Optional[bool] = None
          Exclude homogeneous modes if this is true, or include if this is false.
          If this is None (default), exclude homogeneous modes for dof==\"disp\" only.
      include_default_occ_modes : bool = False
          Include the dof component for the default occupation value on each site
          with occupation DoF. The default is to exclude these modes because they
          are not independent. This parameter is only checked dof==\"occ\". If
          false, the default occupation is determined using
          `site_index_to_default_occ` if that is provided, else using
          `sublattice_index_to_default_occ` if that is provided, else using
          occupation index 0.
      sublattice_index_to_default_occ: Optional[dict[int,int]]
          Optional values of default occupation index (the value), specified by
          sublattice index (the key).
      site_index_to_default_occ: Optional[dict[int,int]]
          Optional values of default occupation index (the value), specified by
          supercell site index (the key).
      calc_wedges : bool = False
          If True, calculate the irreducible wedges for the vector space.
          This may take a long time, but provides the symmetrically unique
          portions of the vector space, which is useful for enumeration.


      Returns
      -------
      results : :class:`~libcasm.configuration.DoFSpaceAnalysisResults`
          Results include a :class:`~libcasm.clexulator.DoFSpace` with symmetry
          adapted basis, and a :class:`~libcasm.irreps.VectorSpaceSymReport`
          holding the irreducible space decomposition used to construct the
          symmetry adapted basis.
      )pbdoc",
      py::arg("dof_space"), py::arg("prim"),
      py::arg("configuration") = std::nullopt,
      py::arg("exclude_homogeneous_modes") = std::nullopt,
      py::arg("include_default_occ_modes") = false,
      py::arg("sublattice_index_to_default_occ") = std::nullopt,
      py::arg("site_index_to_default_occ") = std::nullopt,
      py::arg("calc_wedges") = false);

#ifdef VERSION_INFO
  m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
  m.attr("__version__") = "dev";
#endif
}
