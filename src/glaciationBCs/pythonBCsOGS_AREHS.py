# Collection of python boundary condition (BC) classes for OpenGeoSys
# BCs reflect the external geosphere: cryo-, litho- and atmosphere
# Physical units: depending on parameter set, see below!

import sys
print(sys.version)
print(sys.path)


# e.g export PYTHONPATH=<your path to>/glaciationBCs/src or
# or install pip install https://github.com/cbsilver/glaciationBCs/archive/refs/heads/master.zip
# Make Sure glaciationBCs is installed at the same python executable that is used by OGS


from glaciationBCs import BCs_AREHS as arehs
import OpenGeoSys

OGS_BC = OpenGeoSys.BoundaryCondition
OGS_ST = OpenGeoSys.SourceTerm

# Atmosphere BCs
bc_T_atmosph_above_Dirichlet = arehs.create_BCT_InitialTemperature(OGS_BC)()

bc_H_atmosph_above_Dirichlet = arehs.create_BCH_InitialPressure(OGS_BC)()

# Cryosphere BCs
bc_T_glacier_above_Dirichlet = arehs.create_BCT_SurfaceTemperature(OGS_BC)()
bc_H_glacier_above_Dirichlet = arehs.create_BCH_SurfacePressure(OGS_BC)()
bc_H_glacier_above_Neumann   = arehs.create_BCH_SurfaceInflux(OGS_BC)()
bc_M_glacier_above_Neumann_x = arehs.create_BCM_SurfaceTraction_X(OGS_BC)()
bc_M_glacier_above_Neumann_y = arehs.create_BCM_SurfaceTraction_Y(OGS_BC)()

# Internal source
bc_T_dgrepo_inside_VolSource = arehs.create_BCT_SourceFromRepository(OGS_ST)()

# Lithosphere BCs
bc_T_crustal_below_Neumann_y = arehs.create_BCT_BottomHeatFlux(OGS_BC)()
bc_T_crustal_aside_Dirichlet = arehs.create_BCT_VerticalGradient(OGS_BC)()
bc_H_crustal_aside_Dirichlet = arehs.create_BCH_VerticalGradient(OGS_BC)()
bc_M_crustal_aside_Dirichlet_x = arehs.create_BCM_LateralDisplacement_X(OGS_BC)()


bc_M_crustal_aside_Dirichlet_y = arehs.create_BCM_LateralDisplacement_Y(OGS_BC)()
bc_M_crustal_below_Dirichlet_x = arehs.create_BCM_BottomDisplacement_X(OGS_BC)()
bc_M_crustal_below_Dirichlet_y = arehs.create_BCM_BottomDisplacement_Y(OGS_BC)()
#bc_M_crustal_north
#bc_M_crustal_aside
