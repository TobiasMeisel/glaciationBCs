from lib2to3.pgen2.token import OP
from glaciationBCs import BCs_AREHs
import OpenGeoSys

BC=OpenGeoSys.BoundaryCondition
ST = OpenGeoSys.SourceTerm

# ---------------------------------------------
# instantiate the BC objects used by OpenGeoSys
# ---------------------------------------------
# Naming convention:
# bc_Process_(external)origin_boundary_type(_coefficient)

# Atmosphere BCs
bc_T_atmosph_above_Dirichlet = BCT_InitialTemperature()
bc_H_atmosph_above_Dirichlet = BCH_InitialPressure()

# Cryosphere BCs
bc_T_glacier_above_Dirichlet = BCT_SurfaceTemperature()
bc_H_glacier_above_Dirichlet = BCH_SurfacePressure()
bc_H_glacier_above_Neumann   = BCH_SurfaceInflux()
bc_M_glacier_above_Neumann_x = BCM_SurfaceTraction_X()
bc_M_glacier_above_Neumann_y = BCM_SurfaceTraction_Y()

# Internal source
bc_T_dgrepo_inside_VolSource = BCT_SourceFromRepository()

# Lithosphere BCs
bc_T_crustal_below_Neumann_y = BCT_BottomHeatFlux()
bc_T_crustal_aside_Neumann_x = BCT_LateralHeatFlux()
bc_T_crustal_aside_Dirichlet = BCT_VerticalGradient()
bc_H_crustal_aside_Dirichlet = BCH_VerticalGradient()
bc_M_crustal_aside_Dirichlet_x = BCM_LateralDisplacement_X()
bc_M_crustal_aside_Dirichlet_y = BCM_LateralDisplacement_Y()
bc_M_crustal_aside_Neumann_x = BCM_LateralTraction_X()
bc_M_crustal_below_Dirichlet_x = BCM_BottomDisplacement_X()
bc_M_crustal_below_Dirichlet_y = BCM_BottomDisplacement_Y()
#bc_M_crustal_north
#bc_M_crustal_aside