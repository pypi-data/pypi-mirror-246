# sdwis-drink-water: Safe Drinking Water Information System (SDWIS) API Wrapper

Python wrappers for the  [Envirofacts Data Service API](https://www.epa.gov/enviro/envirofacts-data-service-api) provided by the U.S. Environmental Protection Agency (EPA), with a focus on the Safe Drinking Water Information System (SDWIS).


[![PyPI Version](https://img.shields.io/pypi/v/sdwis_drink_water?label=PyPI)](https://pypi.org/project/sdwis_drink_water/)
[![Documentation Status](https://readthedocs.org/projects/sdwis-drink-water/badge/?version=latest)](https://sdwis-drink-water.readthedocs.io/en/latest)

Installation
------------

The easiest way to install the latest version from PyPI is by using
[pip](https://pip.pypa.io/):

    pip install sdwis_drink_water

You can also use Git to clone the repository from GitHub to install the latest
development version:

    git clone https://github.com/norahtao/sdwis_drink_water
    cd sdwis-drink-water
    pip install .

Alternatively, install directly from the GitHub repository:

    pip install git+https://github.com/norahtao/sdwis_drink_water


## Basic Usage
You do not require any API key to access data from the Envirofacts Data Service API. However, it is essential to familiarize yourself with the SDWIS (Safe Drinking Water Information System) database structure. Understanding this structure will enable you to effectively utilize the various methods provided by the library.

- **Safe Drinking Water Information System (SDWIS) Database**
  - ENFORCEMENT ACTION
  - GEOGRAPHIC AREA
  - LCR_SAMPLE_RESULT
  - LCR_SAMPLE
  - SERVICE AREA
  - TREATMENT
  - WATER SYSTEM
  - WATER SYSTEM FACILITY
  - VIOLATION
  - VIOLATION_ENF_ASSOC

### SdwisTable Class
#### Get Table Information & Data

I provide server methods for fetch table information directly
```python
from sdwis_drink_water import SdwisTable

# "print_url=True" here will cause subsequent queries to display the requested URL
table_api = SdwisTable(print_url=False)
# "print_to_console=True" here causes all subsequent queries to be printed
# fetch all table names
table_names = table_api.get_all_table_names(print_to_console=True)
# fetch all table names with description (Crawl the latest information from the website)
table_api.get_all_table_names_and_descriptions(print_to_console=True)
"""
┌───────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ table_name            │ description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      │
├───────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ ENFORCEMENT_ACTION    │ Documents actions taken against a Public Water System (PWS), laboratory, or operator. Includes requirements that must be met in order to rectify a failure to perform under the Public Water Supply Supervision (PWSS) Program. Enforcement actions are informal and formal. They may be issued by the Primacy State (or its representative) or the EPA. Examples: administrative and civil/criminal legal actions, warning notices, citations, orders to follow water treatment procedures, orders to follow sampling requirements, orders to resolve violations, moratoriums on connections, temporary injunctions, restraining orders, penalties, and orders to comply with reporting requirements. Example descriptors: type of enforcement action, directed actions, and milestone date(s). │
├───────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ GEOGRAPHIC_AREA       │ Information on political units established by geographic boundaries, such as state, town, or county served by a Water System.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    │
├───────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ LCR_SAMPLE_RESULT     │ 90th percentile sample summary results data for lead or copper.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  │
├───────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ LCR_SAMPLE            │ 90th percentile sample summaries data for lead or copper.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        │
├───────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ SERVICE_AREA          │ A service area defines the sensitive populations that receive water from the water system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       │
├───────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ TREATMENT             │ Treatment objectives and process for treating water from a water system facility.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                │
├───────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ WATER_SYSTEM          │ Inventory information on public water systems.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   │
├───────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ WATER_SYSTEM_FACILITY │ Inventory information on public water system facilities.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         │
├───────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ VIOLATION             │ Documents a breach of a requirement. Violations are detected by assessment of sample results or reviews (including on site visits). Violations may lead to legal actions or compliance orders. Violations are publicized, when required, by public notification. Violations may be remedied by compliance/enforcement remedies, such as improved filtration techniques or changes in procedures. Examples: Maximum Contaminant Level (MCL) violations, failure to replace lead service lines, monitoring and reporting violations, treatment technique violations, and procedural violations. Example descriptors: type, date, description, severity, and recommended corrective action(s) to include milestones.                                                                                │
├───────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ VIOLATION_ENF_ASSOC   │ Association between a violation and an enforcement action.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       │
└───────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
"""
for table_name in table_names:
    # fetch structure for specific table name
    table_api.get_table_column_name_by_table_name(table_name=table_name, print_to_console=True)

for table_name in table_names:
    # fetch first data for specific table name
    table_api.get_table_first_data_by_table_name(table_name=table_name, print_to_console=True)

for table_name in table_names:
    # fetch first n for specific table name
    table_api.get_table_first_n_data_by_table_name(table_name=table_name, n=1, print_to_console=True)

```

#### Handle Table Data 

I provide server methods for handling results
```python
from sdwis_drink_water import SdwisTable

# "print_url=True" here will cause subsequent queries to display the requested URL
table_api = SdwisTable(print_url=True)
# fetch first 1000 data from LCR_SAMPLE_RESULT table
result = table_api.get_table_first_n_data_by_table_name(table_name="LCR_SAMPLE_RESULT", n=1000, print_to_console=False)
# get all keys of result data
print(result.get_all_keys())

# get first n data in results
first_one = result.get_first_n_records(1)
first_one.show()

print("find max sample_measure in results")
max_one = result.find_max("sample_measure")
max_one.show()

print("find max sample_measure in results with condition (contaminant_code==PB90)")
max_one_limited_to_pb = result.find_max_with_condition("sample_measure", condition="contaminant_code==PB90")
max_one_limited_to_pb.show()

# export data to a specific file
result.export_data("output.xlsx", format_type="xlsx")
# result.export_data("output.parquet", format_type="parquet")
# result.export_data("output.csv", format_type="csv")
# result.export_data("output.txt", format_type="txt")
```


### Specific Table Handle
You may notice that the most methods of  **`SdwisTable`** require  **`"table_name"`** parameter.
If you only want to focus on specific TABLE, you can directly use its Class.

```python
from sdwis_drink_water import LcrSample, LcrSampleResult, Violation, WaterSystem, WaterSystemFacility, GeographicArea
```
#### WaterSystem
```python
from sdwis_drink_water import WaterSystem
water_system_api = WaterSystem(print_url=True)
# fetch first data from Water_System table
water_system_api.get_table_first_data()

# fetch first n data from Water_System table
water_system_api.get_table_first_n_data(n=2, print_to_console=True)

# get summarize data number according to epa_region
water_system_api.summarize_water_system_data_by_epa_region(multi_threads=True, print_to_console=True)
"""
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  EPA_REGION_ID    WATER_SYSTEM_TOTAL_NUMBER
---------------  ---------------------------
   EPA_REGION_1                        33898
   EPA_REGION_2                        43325
   EPA_REGION_3                        25563
   EPA_REGION_4                        67410
   EPA_REGION_5                        30931
   EPA_REGION_6                        24074
   EPA_REGION_7                        17077
   EPA_REGION_8                        45508
   EPA_REGION_9                       125223
  EPA_REGION_10                        15799
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""

water_system_epa_1 = water_system_api.get_water_system_by_epa_region(epa_region=1, print_to_console=False)
# export data to xlsx
water_system_epa_1.export_data("./output_files/water_system_epa_1.xlsx", format_type="xlsx")
# print all keys to determine how to use this data
print(water_system_epa_1.get_all_keys())

# find by condition "is_grant_eligible_ind==Y"
is_grant_eligible_ind = water_system_epa_1.find_by_condition("is_grant_eligible_ind=Y")
print(is_grant_eligible_ind.count())

# find by condition "is_wholesaler_ind==Y"
is_wholesaler_ind = water_system_epa_1.find_by_condition("is_wholesaler_ind=Y")
print(is_wholesaler_ind.count())

# find by condition "is_grant_eligible_ind==Y" and "is_wholesaler_ind==Y"
is_grant_eligible_ind_and_is_wholesaler_ind = is_grant_eligible_ind.find_by_condition("is_wholesaler_ind=Y")
print(is_grant_eligible_ind_and_is_wholesaler_ind.count())
is_grant_eligible_ind_and_is_wholesaler_ind.show()

# export data to csv
is_grant_eligible_ind_and_is_wholesaler_ind.export_data("./output_files/water_system_epa_1_filtered_result.csv", format_type="csv")
```


### How many drinking water test samples have lead levels that meet the old regulations but not the new ones?
```python
# BACKGROUND: EPA is proposing to lower the lead action level from 15 µg/L (0.015mg/L) to 10 µg/L (0.01mg/L)
# We want to look at the database and see those samples that match the original rule, but not the new one.
from sdwis_drink_water import LcrSampleResult

lcr_sample_result_api = LcrSampleResult(print_url=True)

# fetch first data from LcrSampleResult table
lcr_sample_result_api.get_table_first_data()
# Setting "multi_threads=True" will use multithreading to speed up the fetching of data
lcr_sample_result_api.get_table_columns_description(multi_threads=True)

# Samples exceeding the original rule
pb90_exceed_original_rule = lcr_sample_result_api.get_lcr_sample_result_data_by_conditions("contaminant_code=PB90",
                                                                                           "result_sign_code==",
                                                                                           "sample_measure>0.015")
# Samples exceeding the new rule
pb90_exceed_new_rule = lcr_sample_result_api.get_lcr_sample_result_data_by_conditions("contaminant_code=PB90",
                                                                                      "result_sign_code==",
                                                                                      "sample_measure>0.01")
# fetch their intersection, union, difference
# here intersection is the number of pb90_exceed_original_rule
print(pb90_exceed_original_rule.intersect_with(pb90_exceed_new_rule).count())
# here union is the number of pb90_exceed_new_rule
print(pb90_exceed_original_rule.merge_with(pb90_exceed_new_rule).count())
# get difference. These samples comply with the original rule, but not the new rule. Additional attention is required
print(pb90_exceed_new_rule.difference_with(pb90_exceed_original_rule).count())

result_we_need = pb90_exceed_new_rule.difference_with(pb90_exceed_original_rule)
result_we_need.export_data("./output_files/Sample sets for additional attention in the new regulation of Lead.xlsx",
                           format_type="xlsx")
```

### Quickly access to full database, then export to a xlsx file
This package can serves as an efficient crawler tool, designed to swiftly scrape the entire contents of a data table and export them to an XLSX file. It adeptly navigates the API's restriction of returning a maximum of 10,000 items per query by intelligently segmenting the query into multiple smaller queries. Additionally, the tool boasts a multi-threaded mode, activated by setting the parameter "multi_threads=True". This mode leverages the power of parallel processing to significantly accelerate the rate at which query results are retrieved, ensuring a more efficient and time-effective data collection process.

```python
from sdwis_drink_water import LcrSampleResult
lcr_sample_result_api = LcrSampleResult(print_url=True)
all_lcr_sample = lcr_sample_result_api.get_table_first_n_data(n=99999999, multi_threads=True, print_to_console=False)
all_lcr_sample.export_data("./output_files/all_lcr_samples.xlsx", format_type="xlsx")
"""
The data number in the database provided by the API is 247567. Your request number exceeds this limit, please note.
Fetching Data by multi_threads_mode:   100%|██████████| 25/25 [00:12<00:00,  2.02it/s]
Data is successfully exported to all_lcr_samples.xlsx!
"""
```

## Examples

We have provided various examples to help you understand and use our package effectively:

- **Folder Examples**: 
  - Visit the [`examples` folder](./examples/) for standalone scripts and usage demonstrations.
  
- **Jupyter Notebook Examples**: 
  - For interactive and detailed usage examples, check out the Jupyter notebooks in the [`notebooks` folder](./notebooks/).

These examples cover a range of scenarios and use cases, demonstrating the functionality and features of our package in practical settings.

## Documentation
The code documentation can be found at https://.readthedocs.io/en/latest/

## Contributing
Contributing is always welcome. Just contact us on how best you can contribute, add an issue, or make a PR. 

## License
`sdwis_drink_water` was created by norahtao. It is licensed under the terms of the MIT license.

## TODOs
* Add more features as required

## Contact
You can reach/follow me on any of the following platforms:
* Author: norahtao
* Email: rt29112@columbia.edu

## Credits
`sdwis_drink_water` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
