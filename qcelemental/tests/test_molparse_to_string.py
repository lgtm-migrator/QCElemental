import pytest

import qcelemental as qcel
from qcelemental.testing import compare

from .addons import drop_qcsk

# CODATA2014 = 1.05835442134
# CODATA2018 = 1.058354421806
au2 = 2.0 * qcel.constants.bohr2angstroms

_results = {
    "subject1": """
3 au

Co 0 0 0
H  2 0 0
h_OTher -2 0 0
""",
    "ans1_xyz_au": """3 au
0 2 CoH2
Co                    0.000000000000     0.000000000000     0.000000000000
H                     2.000000000000     0.000000000000     0.000000000000
H                    -2.000000000000     0.000000000000     0.000000000000
""",
    "ans1_xyz_ang": f"""3
0 2 CoH2
Co                    0.000000000000     0.000000000000     0.000000000000
H                     {au2:.12f}     0.000000000000     0.000000000000
H                    -{au2:.12f}     0.000000000000     0.000000000000
""",
    "ans1c_xyz_ang": """3
0 2 CoH2
59Co                      0.00000000         0.00000000         0.00000000
1H                        1.05835442         0.00000000         0.00000000
1H_other                 -1.05835442         0.00000000         0.00000000
""",
    "ans1c_xyz_nm": """3 nm
0 2 CoH2
59Co                      0.00000000         0.00000000         0.00000000
1H                        0.10583544         0.00000000         0.00000000
1H_other                 -0.10583544         0.00000000         0.00000000
""",
    "ans1_psi4_ang": f"""0 2
Co                    0.000000000000     0.000000000000     0.000000000000
H                     {au2:.12f}     0.000000000000     0.000000000000
H_other              -{au2:.12f}     0.000000000000     0.000000000000
units angstrom
""",
    "ans1_qchem_ang": f"""$molecule
0 2
Co                    0.000000000000     0.000000000000     0.000000000000
H                     {au2:.12f}     0.000000000000     0.000000000000
H                    -{au2:.12f}     0.000000000000     0.000000000000
$end
""",
    "ans1_orca_ang": f"""!

*xyz 0 2
Co                    0.000000000000     0.000000000000     0.000000000000
H                     {au2:.12f}     0.000000000000     0.000000000000
H                    -{au2:.12f}     0.000000000000     0.000000000000
*
""",
    "subject2": f"""
Co 0 0 0
no_reorient
--
@H  {au2} 0 0
h_OTher -{au2} 0 0
""",
    "ans2_au": """3 au
0 3 CoH2
Co                    0.000000000000     0.000000000000     0.000000000000
@H                    2.000000000000     0.000000000000     0.000000000000
H                    -2.000000000000     0.000000000000     0.000000000000
""",
    "ans2_ang": f"""3
0 3 CoH2
Co                    0.000000000000     0.000000000000     0.000000000000
Gh(1)                 {au2:.12f}     0.000000000000     0.000000000000
H                    -{au2:.12f}     0.000000000000     0.000000000000
""",
    "ans2c_ang": f"""2
0 3 CoH2
Co                    0.000000000000     0.000000000000     0.000000000000
H                    -{au2:.12f}     0.000000000000     0.000000000000
""",
    "ans2_cfour_ang": f"""auto-generated by QCElemental from molecule CoH2
Co                    0.000000000000     0.000000000000     0.000000000000
GH                    {au2:.12f}     0.000000000000     0.000000000000
H                    -{au2:.12f}     0.000000000000     0.000000000000
""",
    "ans2_nwchem_ang": f"""geometry units angstroms
Co                    0.000000000000     0.000000000000     0.000000000000
bqH                   {au2:.12f}     0.000000000000     0.000000000000
H_other              -{au2:.12f}     0.000000000000     0.000000000000

end
""",
    "ans2_madness_au": f"""geometry
units au
Co                    0.000000000000     0.000000000000     0.000000000000
GH                    2.000000000000     0.000000000000     0.000000000000
H                    -2.000000000000     0.000000000000     0.000000000000
end
""",
    "ans2_madness_ang": f"""geometry
units angstrom
Co                    0.000000000000     0.000000000000     0.000000000000
GH                    {au2:.12f}     0.000000000000     0.000000000000
H                    -{au2:.12f}     0.000000000000     0.000000000000
end
""",
    "ans2_mrchem_au": """Molecule {
charge = 0
multiplicity = 3
translate = False
$coords
Co                    0.000000000000     0.000000000000     0.000000000000
H                     2.000000000000     0.000000000000     0.000000000000
H                    -2.000000000000     0.000000000000     0.000000000000
$end
}
""",
    "ans2_mrchem_ang": f"""Molecule {{
charge = 0
multiplicity = 3
translate = False
$coords
Co                    0.000000000000     0.000000000000     0.000000000000
H                     {au2:.12f}     0.000000000000     0.000000000000
H                    -{au2:.12f}     0.000000000000     0.000000000000
$end
}}
""",
    "ans2_terachem_au": """3 au
CoH2
Co                    0.000000000000     0.000000000000     0.000000000000
XH                    2.000000000000     0.000000000000     0.000000000000
H                    -2.000000000000     0.000000000000     0.000000000000
""",
    "ans2_terachem_ang": f"""3
CoH2
Co                    0.000000000000     0.000000000000     0.000000000000
XH                    {au2:.12f}     0.000000000000     0.000000000000
H                    -{au2:.12f}     0.000000000000     0.000000000000
""",
    "ans2_psi4_au": """0 3
--
0 2
Co                    0.000000000000     0.000000000000     0.000000000000
--
0 2
Gh(H)                 2.000000000000     0.000000000000     0.000000000000
H_other              -2.000000000000     0.000000000000     0.000000000000
units bohr
no_reorient
""",
    "ans2_qchem_au": """$molecule
0 3
--
0 2
Co                    0.000000000000     0.000000000000     0.000000000000
--
0 2
@H                    2.000000000000     0.000000000000     0.000000000000
H                    -2.000000000000     0.000000000000     0.000000000000
$end
""",
    "ans2_molpro_au": """{orient,noorient}
{symmetry,auto}

{bohr}
geometry={
Co                    0.000000000000     0.000000000000     0.000000000000
H                     2.000000000000     0.000000000000     0.000000000000
H                    -2.000000000000     0.000000000000     0.000000000000
}
dummy,2
set,charge=0.0
set,spin=2
""",
    "ans2_molpro_ang": f"""{{orient,noorient}}
{{symmetry,auto}}

{{angstrom}}
geometry={{
Co                    0.000000000000     0.000000000000     0.000000000000
H                     {au2:.12f}     0.000000000000     0.000000000000
H                    -{au2:.12f}     0.000000000000     0.000000000000
}}
dummy,2
set,charge=0.0
set,spin=2
""",
    "ans2_orca_au": """! Bohrs

*xyz 0 3
Co                    0.000000000000     0.000000000000     0.000000000000
H:                    2.000000000000     0.000000000000     0.000000000000
H                    -2.000000000000     0.000000000000     0.000000000000
*
""",
    "ans2_orca_ang": """!

*xyz 0 3
Co                    0.000000000000     0.000000000000     0.000000000000
H:                    1.058354421340     0.000000000000     0.000000000000
H                    -1.058354421340     0.000000000000     0.000000000000
*
""",
    "ans2_turbomole_au": """$coord
   0.000000000000     0.000000000000     0.000000000000  co
   2.000000000000     0.000000000000     0.000000000000  h
  -2.000000000000     0.000000000000     0.000000000000  h
$end
""",
    "ans2_ngslviewsdf": """
QCElemental

  3  2  0  0  0  0  0  0  0  0  0
    0.0000    0.0000    0.0000 Co  0  0     0  0  0  0  0  0
    1.0584    0.0000    0.0000 Gh  0  0     0  0  0  0  0  0
   -1.0584    0.0000    0.0000  H  0  0     0  0  0  0  0  0
  1  2  1  0  0  0  0
  1  3  1  0  0  0  0
""",
    "ans2_gamess_ang": """ $data
 auto-generated by QCElemental from molecule CoH2
 C1
 Co 27                0.000000000000     0.000000000000     0.000000000000
 H -1                 1.058354421340     0.000000000000     0.000000000000
 H_other 1           -1.058354421340     0.000000000000     0.000000000000
 $end
""",
}


@pytest.mark.parametrize(
    "inp,expected",
    [
        (("subject1", {"dtype": "xyz", "units": "Bohr"}), "ans1_xyz_au"),
        (("subject1", {"dtype": "xyz", "units": "Angstrom"}), "ans1_xyz_ang"),
        (("subject1", {"dtype": "xyz", "prec": 8, "atom_format": "{elea}{elem}{elbl}"}), "ans1c_xyz_ang"),
        (("subject1", {"dtype": "xyz", "units": "nm", "prec": 8, "atom_format": "{elea}{elem}{elbl}"}), "ans1c_xyz_nm"),
        (("subject1", {"dtype": "psi4", "units": "angstrom"}), "ans1_psi4_ang"),
        (("subject1", {"dtype": "qchem", "units": "angstrom"}), "ans1_qchem_ang"),
        (("subject1", {"dtype": "orca", "units": "angstrom"}), "ans1_orca_ang"),
        (("subject2", {"dtype": "xyz", "units": "Bohr"}), "ans2_au"),
        (("subject2", {"dtype": "xyz", "units": "Angstrom", "ghost_format": "Gh({elez})"}), "ans2_ang"),
        (("subject2", {"dtype": "xyz", "units": "angstrom", "ghost_format": ""}), "ans2c_ang"),
        (("subject2", {"dtype": "cfour", "units": "angstrom"}), "ans2_cfour_ang"),
        (("subject2", {"dtype": "nwchem", "units": "angstrom"}), "ans2_nwchem_ang"),
        (("subject2", {"dtype": "madness", "units": "bohr"}), "ans2_madness_au"),
        (("subject2", {"dtype": "madness", "units": "angstrom"}), "ans2_madness_ang"),
        (("subject2", {"dtype": "mrchem", "units": "bohr"}), "ans2_mrchem_au"),
        (("subject2", {"dtype": "mrchem", "units": "angstrom"}), "ans2_mrchem_ang"),
        (("subject2", {"dtype": "terachem", "units": "angstrom"}), "ans2_terachem_ang"),
        (("subject2", {"dtype": "terachem"}), "ans2_terachem_au"),
        (("subject2", {"dtype": "psi4", "units": "bohr"}), "ans2_psi4_au"),
        (("subject2", {"dtype": "molpro", "units": "bohr"}), "ans2_molpro_au"),
        (("subject2", {"dtype": "molpro", "units": "angstrom"}), "ans2_molpro_ang"),
        (("subject2", {"dtype": "orca", "units": "bohr"}), "ans2_orca_au"),
        (("subject2", {"dtype": "orca", "units": "angstrom"}), "ans2_orca_ang"),
        (("subject2", {"dtype": "turbomole", "units": "bohr"}), "ans2_turbomole_au"),
        (("subject2", {"dtype": "nglview-sdf"}), "ans2_ngslviewsdf"),
        (("subject2", {"dtype": "qchem", "units": "bohr"}), "ans2_qchem_au"),
        (("subject2", {"dtype": "gamess", "units": "angstrom"}), "ans2_gamess_ang"),
    ],
)
def test_to_string_xyz(inp, expected):
    molrec = qcel.molparse.from_string(_results[inp[0]])
    smol = qcel.molparse.to_string(molrec["qm"], **inp[1])
    print(smol)

    assert compare(_results[expected], smol)


_molecule_inputs = {
    "subject1": qcel.models.Molecule(
        **{
            "geometry": [0, 0, 0, 0, 0, 1.9, 0, -1.9, 0],
            "symbols": ["O", "H", "H"],
            "connectivity": [[0, 1, 1], [0, 2, 1]],
        }
    ),
    "subject1_nocon": qcel.models.Molecule(
        **{"geometry": [0, 0, 0, 0, 0, 1.9, 0, -1.9, 0], "symbols": ["O", "H", "H"]}
    ),
    "subject2": qcel.models.Molecule(
        **{
            "geometry": [0, 0, 0, 0, 0, 1.9, 0, -1.9, 0],
            "symbols": ["O", "H", "H"],
            "connectivity": [[0, 1, 1], [0, 2, 1]],
            "real": [False, False, True],
        }
    ),
}

_molecule_outputs = {
    "ans1_ngslviewsdf": """
QCElemental

  3  2  0  0  0  0  0  0  0  0  0
    0.0000    0.0000    0.0000  O  0  0     0  0  0  0  0  0
    0.0000    0.0000    1.0054  H  0  0     0  0  0  0  0  0
    0.0000   -1.0054    0.0000  H  0  0     0  0  0  0  0  0
  1  2  1  0  0  0  0
  1  3  1  0  0  0  0
""",
    "ans2_ngslviewsdf": """
QCElemental

  3  2  0  0  0  0  0  0  0  0  0
    0.0000    0.0000    0.0000 Gh  0  0     0  0  0  0  0  0
    0.0000    0.0000    1.0054 Gh  0  0     0  0  0  0  0  0
    0.0000   -1.0054    0.0000  H  0  0     0  0  0  0  0  0
  1  2  1  0  0  0  0
  1  3  1  0  0  0  0
""",
}


@pytest.mark.parametrize(
    "inp,kwargs,expected",
    [
        ("subject1", {"dtype": "nglview-sdf"}, "ans1_ngslviewsdf"),
        ("subject1_nocon", {"dtype": "nglview-sdf"}, "ans1_ngslviewsdf"),
        ("subject2", {"dtype": "nglview-sdf"}, "ans2_ngslviewsdf"),
    ],
)
def test_molecule_to_string(inp, kwargs, expected, request):

    smol = _molecule_inputs[inp].to_string(**kwargs)
    drop_qcsk(_molecule_inputs[inp], request.node.name)
    assert compare(_molecule_outputs[expected], smol)


@pytest.mark.parametrize(
    "inp", [("subject1", {"dtype": "xyz", "units": "kg", "prec": 8, "atom_format": "{elea}{elem}{elbl}"})]
)
def test_to_string_pint_error(inp):
    import pint

    molrec = qcel.molparse.from_string(_results[inp[0]])

    with pytest.raises(pint.errors.DimensionalityError):
        qcel.molparse.to_string(molrec["qm"], **inp[1])


@pytest.mark.parametrize("inp", [("subject1", {"dtype": "nglview-sdf", "units": "bohr"})])
def test_to_string_value_error(inp):
    molrec = qcel.molparse.from_string(_results[inp[0]])

    with pytest.raises(ValueError):
        qcel.molparse.to_string(molrec["qm"], **inp[1])
