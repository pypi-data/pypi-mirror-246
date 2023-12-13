"""
  MechViz -- Python-based toolkit for the analysis and visualization of mechanical properties of materials

  Copyright (C) 2019-2024 by Chinedu Ekuma

  This program is free software; you can redistribute it and/or modify it under the
  terms of the GNU General Public License as published by the Free Software Foundation
  version 3 of the License.

  This program is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
  PARTICULAR PURPOSE.  See the GNU General Public License for more details.

  E-mail: cekuma1@gmail.com

"""

import os
from ase.io import vasp, cif,read, write
from ase.io import vasp
from math import pi, sqrt
from numpy import cross, linalg
import numpy as np

def readstruct():
    # Get the current working directory
    cwd = os.getcwd()

    # Search for .vasp and .cif files in the current directory
    for file in os.listdir(cwd):
        if file.endswith('.vasp'):
            pos = vasp.read_vasp(file)
            return pos
        elif file.endswith('.cif'):
            # Read the CIF file
            atoms = read(file)

            # Convert to POSCAR format
            poscar_file = os.path.join(cwd, 'POSCAR')
            write(poscar_file, atoms, format='vasp')
            pos = vasp.read_vasp(poscar_file)
            return pos

    raise ValueError("No supported structure file found in the current directory!")


def read_elastic_tensor(file_name):
    # Reading the elastic tensor from the file
    elastic_tensor = np.loadtxt(file_name)
    return elastic_tensor
    
def read_rho_dim(file_name):
    with open(file_name, 'r') as file:
        # Skip the header line
        next(file)
        # Read the data line
        data_line = next(file).strip()

    # Split the line into components and check if it contains exactly two values
    parts = data_line.split()
    if len(parts) != 2:
        raise ValueError(f"Expected 2 values in the line, but got {len(parts)} values.")

    rho_str, dimensional = parts

    # Convert the numeric data back to a float
    rho = float(rho_str)

    return rho, dimensional


def readstructold(structure_file, pos):
    # Get the current working directory
    cwd = os.getcwd()

    if structure_file.endswith('.vasp'):
        pos = vasp.read_vasp(structure_file)
    elif structure_file.endswith('.cif'):
        # Read the CIF file
        atoms = read(structure_file)

        # Convert to POSCAR format
        poscar_file = os.path.join(cwd, 'POSCAR')
        write(poscar_file, atoms, format='vasp')
        pos = vasp.read_vasp(poscar_file)
    else:
        raise ValueError("Unsupported structure file format!")

    return pos
