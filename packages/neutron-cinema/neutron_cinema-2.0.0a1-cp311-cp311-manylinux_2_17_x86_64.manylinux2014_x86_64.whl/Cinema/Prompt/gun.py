################################################################################
##                                                                            ##
##  This file is part of Prompt (see https://gitlab.com/xxcai1/Prompt)        ##
##                                                                            ##
##  Copyright 2021-2022 Prompt developers                                     ##
##                                                                            ##
##  Licensed under the Apache License, Version 2.0 (the "License");           ##
##  you may not use this file except in compliance with the License.          ##
##  You may obtain a copy of the License at                                   ##
##                                                                            ##
##      http://www.apache.org/licenses/LICENSE-2.0                            ##
##                                                                            ##
##  Unless required by applicable law or agreed to in writing, software       ##
##  distributed under the License is distributed on an "AS IS" BASIS,         ##
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  ##
##  See the License for the specific language governing permissions and       ##
##  limitations under the License.                                            ##
##                                                                            ##
################################################################################

from ..Interface import *

_pt_PythonGun_new = importFunc('pt_PythonGun_new', type_voidp, [type_pyobject])
_pt_PythonGun_delete = importFunc('pt_PythonGun_delete', None, [type_voidp])
_pt_PythonGun_pushToStack = importFunc('pt_PythonGun_pushToStack', None, [type_voidp, type_npdbl1d])


class PythonGun():
    def __init__(self):
        self.cobj = _pt_PythonGun_new(self)
        
    def __del__(self):
        _pt_PythonGun_delete(self.cobj)

    def generate(self):
        pdata = np.zeros(9)
        pdata[0] = self.sampleEnergy()
        pdata[1] = self.sampleWeight()
        pdata[2] = self.sampleTime()
        pdata[3:6] = self.samplePosition()
        pdata[6:]  = self.sampleDirection()        
        _pt_PythonGun_pushToStack(self.cobj, pdata)      
    
    def sampleEnergy(self):
        return 0.0253

    def sampleWeight(self):
        return 1. 
    
    def sampleTime(self):
        return 0.
    
    def samplePosition(self):
        return np.array([0.,0.,0.])
    
    def sampleDirection(self):
        return np.array([0.,0.,1.])



    
from .configstr import ConfigString
from .Histogram import wl2ekin

class Gun(ConfigString):
    pass

# gunCfg = f'gun=SimpleThermalGun;position=0,0,-12000;direction=0,0,1;energy={0}'

class IsotropicGun(ConfigString):
    def __init__(self) -> None:
        super().__init__()
        self.cfg_gun='IsotropicGun'
        self.cfg_position = '0,0,0.'
        self.cfg_energy = 0

    def setPosition(self, pos):
        self.cfg_position = f'{pos[0]}, {pos[1]}, {pos[2]}'

    def setEnergy(self, ekin):
        self.cfg_energy = ekin

    def setWavelength(self, wl):
        self.cfg_energy = wl2ekin(wl)

class SimpleThermalGun(IsotropicGun):
    def __init__(self) -> None:
        super().__init__()
        self.cfg_gun='SimpleThermalGun'
        self.cfg_direction = '0,0,1.'

    def setDirection(self, dir):
        self.cfg_position = f'{dir[0]}, {dir[1]}, {dir[2]}'


class SurfaceSurce(ConfigString):
    def __init__(self, src_whz=None, slit_whz=None) -> None:
        super().__init__()
        if src_whz:
            self.setSource(src_whz)
        if slit_whz:
            self.setSlit(slit_whz)

    def setSource(self, whz):
        self.cfg_src_w = whz[0]
        self.cfg_src_h = whz[1]
        self.cfg_src_z = whz[2]

    def setSlit(self, whz):
        self.cfg_slit_w = whz[0]
        self.cfg_slit_h = whz[1]
        self.cfg_slit_z = whz[2]

class MaxwellianGun(SurfaceSurce):
    def __init__(self, src_whz=None, slit_whz=None, temperature=293.15) -> None:
        super().__init__(src_whz, slit_whz)
        self.setTemperature(temperature)
        self.cfg_gun='MaxwellianGun'
        

    def setTemperature(self, temp):
        self.cfg_temperature = temp

class UniModeratorGun(SurfaceSurce):
    def __init__(self, src_whz=None, slit_whz=None, wl_mean=1, wl_range=0.0001) -> None:
        super().__init__(src_whz, slit_whz)
        self.setWlMean(wl_mean)
        self.setWlRange(wl_range)
        self.cfg_gun='UniModeratorGun'
    
    def setWlMean(self, wl):
        self.cfg_mean_wl = wl

    def setWlRange(self, wl_range):
        self.cfg_range_wl = wl_range

class MCPLGun(ConfigString):
    def __init__(self, mcplfile = None) -> None:
        super().__init__()
        if mcplfile:
            self.setMCPLFile(mcplfile)
        self.cfg_gun='MCPLGun'

    def setMCPLFile(self, mcplfile):
        self.cfg_mcplfile = mcplfile