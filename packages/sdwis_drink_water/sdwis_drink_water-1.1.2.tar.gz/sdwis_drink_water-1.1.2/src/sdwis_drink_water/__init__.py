"""
sdwis-drink-water: Safe Drinking Water Information System (SDWIS) API Wrapper
"""
from importlib.metadata import version

__version__ = '1.1.0'
__author__ = ''
__license__ = 'MIT'

from .api import SdwisAPI
from .api_for_table import SdwisTable
from .data_praser import ResultDataParser
from .models import EnforcementAction, GeographicArea, LcrSample, LcrSampleResult, \
    ServiceArea, Treatment, Violation, ViolationEnfAssoc, WaterSystem, WaterSystemFacility

from .utils_for_jupyter_print import tabulate_for_jupyter, print_column_description, print_result_data, print_columns

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
