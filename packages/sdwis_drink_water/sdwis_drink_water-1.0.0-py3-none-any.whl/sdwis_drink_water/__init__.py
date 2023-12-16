"""
sdwis-drink-water: Safe Drinking Water Information System (SDWIS) API Wrapper
"""
from importlib.metadata import version

__version__ = '1.1.0'
__author__ = ''
__license__ = 'MIT'

from sdwis_drink_water.api import SdwisAPI
from sdwis_drink_water.api_for_table import SdwisTable
from sdwis_drink_water.data_praser import ResultDataParser
from sdwis_drink_water.models import EnforcementAction, GeographicArea, LcrSample, LcrSampleResult, \
    ServiceArea, Treatment, Violation, ViolationEnfAssoc, WaterSystem, WaterSystemFacility

# Global API
api = SdwisAPI()
lcr_sample = LcrSample()
lcr_sample_result = LcrSampleResult()
violation = Violation()
water_system = WaterSystem()
water_system_facility = WaterSystemFacility()
geographic_area = GeographicArea()
enforcement_action = EnforcementAction()
service_area = ServiceArea()
treatment = Treatment()
violation_enf_assoc = ViolationEnfAssoc()
