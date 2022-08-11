
from glaciationBCs import glacierclass_AREHS as glc	# glacier
from glaciationBCs import crustclass_AREHS as crc 	# earth crust
from glaciationBCs import repoclass_AREHS as dgr	# repository
from glaciationBCs import airclass_AREHS as air		# atmosphere
from glaciationBCs.constants_AREHS import *			# constants




# Nomenclature: BC Process_LocationQuantity_Component
# 					(THM)			(XYZ)

# Process	Dirichlet BC	Neumann BC (normal to boundary)
# T			temperature		heat flux
# H			pressure		hydraulic flux
# M			displacement	momentum flux (stress vector)

#TODO linear distribution for T gradient and p gradient at left boundary

# ---------------------------------------------------------
# Thermal BCs
# ---------------------------------------------------------
def create_BCT_InitialTemperature(base):

	class BCT_InitialTemperature(base):

		def __init__(self):
			super(BCT_InitialTemperature, self).__init__()
			# instantiate member objects of the external geosphere
			self.air = air.air(T_ini, T_min, t_)

		def getDirichletBCValue(self, t, coords, node_id, primary_vars):
			x, y, z = coords

			value = self.air.T_ini

			return (True, value)

	return BCT_InitialTemperature

def create_BCT_SurfaceTemperature(base):
	class BCT_SurfaceTemperature(base):

		def __init__(self):
			super(BCT_SurfaceTemperature, self).__init__()
			# instantiate member objects of the external geosphere
			self.air = air.air(T_ini, T_min, t_)
			self.glacier = glc.glacier(L_dom, L_max, H_max, x_0, t_)
			if plotinput:
				self.air.plot_evolution()

		def getDirichletBCValue(self, t, coords, node_id, primary_vars):
			x, y, z = coords

			if t != self.air.t_prev:
				print(self.air.tcr.stage_control(t))
				self.air.t_prev = t

			under_glacier = x-self.glacier.x_0 <= self.glacier.length(t) > 0
			if under_glacier:
				# prescribe fixed temperature underneath the glacier body
				value = self.glacier.temperature(x,t)
			else:
				#linear profile from north to south
				value = self.air.temperature(t)

			return (True, value)

	return BCT_SurfaceTemperature

def create_BCT_SourceFromRepository(base_SourceTerm):
	class BCT_SourceFromRepository(base_SourceTerm):

		def __init__(self):
			super(BCT_SourceFromRepository, self).__init__()
			# instantiate member objects of the external geosphere
			self.repo = dgr.repo(BE_Q, BE_z, BE_f, HA_Q, HA_z, HA_f, BE_vol, HA_vol,
								 100*lrepo, t_inter_BE, t_inter_HA, t_filled)
			if plotinput:
				self.repo.print_max_load()
				self.repo.plot_evolution()

		def getFlux(self, t, coords, primary_vars):
			x, y, z = coords

			value = 0
			inside_repo = (xrmin <= x <= xrmax) and (yrmin <= y <= yrmax)
			if inside_repo:
				# prescribe heat flux from radioactive repository
				value = self.repo.radioactive_heatflux(t)
				"""
				if t != self.repo.t_prev:
					#print("y = ",y)
					print("t/a = ",t/s_a)
					print("H = ", self.repo.radioactive_heatflow(t))
					self.repo.t_prev = t
				"""

			derivative = [0.0] * len(primary_vars)
			return (value, derivative)

	return BCT_SourceFromRepository


def create_BCT_BottomHeatFlux(base):
	class BCT_BottomHeatFlux(base):

		def __init__(self):
			super(BCT_BottomHeatFlux, self).__init__()
			# instantiate member objects of the external geosphere
			self.crust = crc.crust(q_geo)

		def getFlux(self, t, coords, primary_vars): #here Neumann BC: flux of heat
			x, y, z = coords

			# get heat flux component
			value = self.crust.geothermal_heatflux()[1]

			derivative = [0.0] * len(primary_vars)
			return (True, value, derivative)

	return BCT_BottomHeatFlux


def create_BCT_VerticalGradient(base):
	class BCT_VerticalGradient(base):

		def __init__(self):
			super(BCT_VerticalGradient, self).__init__()
			# instantiate member objects of the external geosphere
			self.air = air.air(T_ini, T_min, t_)
			self.crust = crc.crust(q_geo)

		def getDirichletBCValue(self, t, coords, node_id, primary_vars):
			x, y, z = coords

			# evolving surface temperature
			T_top = self.air.temperature(t)
			# vertical geothermal gradient
			value = self.crust.geothermal_temperature(x,y,z,t,T_top)

			return (True, value)

	return BCT_VerticalGradient

# ------------------------------------------------------
# Hydraulic BCs
# ------------------------------------------------------
def create_BCH_InitialPressure(base):
	class BCH_InitialPressure(base):

		def __init__(self):
			super(BCH_InitialPressure, self).__init__()
			# instantiate member objects of the external geosphere
			self.air = air.air(T_ini, T_min, t_)

		def getDirichletBCValue(self, t, coords, node_id, primary_vars):
			x, y, z = coords

			value = self.air.pressure

			return (True, value)

	return BCH_InitialPressure

def create_BCH_SurfacePressure(base):
	class BCH_SurfacePressure(base):

		def __init__(self):
			super(BCH_SurfacePressure, self).__init__()
			# instantiate member objects of the external geosphere
			self.air = air.air(T_ini, T_min, t_)
			self.glacier = glc.glacier(L_dom, L_max, H_max, x_0, t_)

		def getDirichletBCValue(self, t, coords, node_id, primary_vars):
			x, y, z = coords

			if t != self.glacier.t_prev:
				print(self.glacier.tcr_h.stage_control(t))
				self.glacier.t_prev = t

			under_glacier = x-self.glacier.x_0 <= self.glacier.length(t) > 0
			if under_glacier:
				# height dependent pressure from glacier
				value = self.glacier.pressure(x,t)
			else:
				# fixed pressure from ambient air
				value = self.air.pressure

			return (True, value)

	return BCH_SurfacePressure

def create_BCH_SurfaceInflux(base):
	class BCH_SurfaceInflux(base):

		def __init__(self):
			super(BCH_SurfaceInflux, self).__init__()
			# instantiate member objects of the external geosphere
			self.glacier = glc.glacier(L_dom, L_max, H_max, x_0, t_)

		def getFlux(self, t, coords, primary_vars): #here Neumann BC: hydraulic flux
			x, y, z = coords

			derivative = [0.0] * len(primary_vars)

			under_glacier = x-self.glacier.x_0 <= self.glacier.length(t) > 0
			if under_glacier:
				# get hydraulic flux under glacier
				value = self.glacier.local_meltwater(x,t)
				return (True, value, derivative)
			# no BC => free boundary then (no flux)
			return (False, 0.0, derivative)

	return BCH_SurfaceInflux

def create_BCH_VerticalGradient(base):
	class BCH_VerticalGradient(base):

		def __init__(self):
			super(BCH_VerticalGradient, self).__init__()
			# instantiate member objects of the external geosphere
			self.air = air.air(T_ini, T_min, t_)
			self.crust = crc.crust(q_geo)

		def getDirichletBCValue(self, t, coords, node_id, primary_vars):
			x, y, z = coords

			# height dependent pressure from the crust
			p_pore = self.crust.hydrostatic_pressure(x,y,z,t)
			# fixed pressure from ambient air
			p_atmo = self.air.pressure

			value = p_pore + p_atmo

			return (True, value)

	return BCH_VerticalGradient


# --------------------------------------------------------
# Mechanics BCs
# --------------------------------------------------------
def create_BCM_SurfaceTraction_X(base):
	class BCM_SurfaceTraction_X(base):

		def __init__(self):
			super(BCM_SurfaceTraction_X, self).__init__()
			# instantiate member objects of the external geosphere
			self.glacier = glc.glacier(L_dom, L_max, H_max, x_0, t_)
			if plotinput:
				self.glacier.print_max_load()
				self.glacier.plot_evolution()
				self.glacier.plot_evolving_shape()

		def getFlux(self, t, coords, primary_vars): #here Neumann BC: flux of linear momentum
			x, y, z = coords

			derivative = [0.0] * len(primary_vars)

			under_glacier = x-self.glacier.x_0 <= self.glacier.length(t) > 0
			if under_glacier:
				value = self.glacier.tangentialstress(x,t)
				return (True, value, derivative)
			# no BC => free boundary then (no flux)
			return (False, 0.0, derivative)

	return BCM_SurfaceTraction_X

def create_BCM_SurfaceTraction_Y(base):
	class BCM_SurfaceTraction_Y(base):

		def __init__(self):
			super(BCM_SurfaceTraction_Y, self).__init__()
			# instantiate member objects of the external geosphere
			self.glacier = glc.glacier(L_dom, L_max, H_max, x_0, t_)

		def getFlux(self, t, coords, primary_vars): #here Neumann BC: flux of linear momentum
			x, y, z = coords

			derivative = [0.0] * len(primary_vars)

			under_glacier = x-self.glacier.x_0 <= self.glacier.length(t) > 0
			if under_glacier:
				value = self.glacier.normalstress(x,t)
				return (True, value, derivative)
			# no BC => free boundary then (no flux)
			return (False, 0.0, derivative)

	return BCM_SurfaceTraction_Y

def create_BCM_BottomDisplacement_X(base):
	class BCM_BottomDisplacement_X(base):

		def __init__(self):
			super(BCM_BottomDisplacement_X, self).__init__()
			# instantiate member objects of the external geosphere
			self.crust = crc.crust(q_geo)

		def getDirichletBCValue(self, t, coords, node_id, primary_vars):
			x, y, z = coords

			# prescribe displacement u_x
			value = self.crust.displacement_below(x,y,z,t)[0]

			return (True, value)

	return BCM_BottomDisplacement_X

def create_BCM_BottomDisplacement_Y(base):
	class BCM_BottomDisplacement_Y(base):

		def __init__(self):
			super(BCM_BottomDisplacement_Y, self).__init__()
			# instantiate member objects of the external geosphere
			self.crust = crc.crust(q_geo)

		def getDirichletBCValue(self, t, coords, node_id, primary_vars):
			x, y, z = coords

			# prescribe displacement u_y
			value = self.crust.displacement_below(x,y,z,t)[1]

			return (True, value)

	return BCM_BottomDisplacement_Y


def create_BCM_LateralDisplacement_X(base):
	class BCM_LateralDisplacement_X(base):

		def __init__(self):
			super(BCM_LateralDisplacement_X, self).__init__()
			# instantiate member objects of the external geosphere
			self.crust = crc.crust(q_geo)

		def getDirichletBCValue(self, t, coords, node_id, primary_vars):
			x, y, z = coords

			# prescribe displacement u_x
			value = self.crust.displacement_aside(x,y,z,t)[0]

			return (True, value)

	return BCM_LateralDisplacement_X


def create_BCM_LateralDisplacement_Y(base):

	class BCM_LateralDisplacement_Y(base):

		def __init__(self):
			base.__init__(self)
			# instantiate member objects of the external geosphere
			self.crust = crc.crust(q_geo)

		def getDirichletBCValue(self, t, coords, node_id, primary_vars):
			x, y, z = coords

			# prescribe displacement u_y
			value = self.crust.displacement_aside(x,y,z,t)[0]

			return (True, value)

	return BCM_LateralDisplacement_Y