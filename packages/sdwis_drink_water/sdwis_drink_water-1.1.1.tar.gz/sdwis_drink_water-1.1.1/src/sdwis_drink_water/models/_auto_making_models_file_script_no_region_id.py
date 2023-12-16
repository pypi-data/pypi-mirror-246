import os

directory = "."

file_class_map = {
    "enforcement_action.py": "Enforcement_Action",
    "service_area.py": "Service_Area",
    "treatment.py": "Treatment",
    "violation_enf_assoc.py": "Violation_Enf_Assoc"
}

class_template = '''
from sdwis_drink_water.api_for_table import SdwisTable

class {class_name}:
    def __init__(self, print_url=False):
        self.sdwis_table = SdwisTable(print_url=print_url)
        self.TABLE_NAME = "{table_name}"
    
    def get_table_column_name(self, print_to_console=True):
        return self.sdwis_table.get_table_column_name_by_table_name(table_name=self.TABLE_NAME,
                                                                    print_to_console=print_to_console)
    
    def get_table_columns_description(self, multi_threads=False, print_to_console=True):
        return self.sdwis_table.get_columns_description_by_table_name(table_name=self.TABLE_NAME,
                                                                    print_to_console=print_to_console, 
                                                                    multi_threads=multi_threads)                                                       
    def get_table_data_number(self):
        return self.sdwis_table.get_table_data_number(table_name=self.TABLE_NAME)
        
    def get_table_first_data(self, print_to_console=True):
        return self.sdwis_table.get_table_first_data_by_table_name(table_name=self.TABLE_NAME,
                                                                   print_to_console=print_to_console)

    def get_table_first_n_data(self, n=0, multi_threads=False, print_to_console=True):
        return self.sdwis_table.get_table_first_n_data_by_table_name(table_name=self.TABLE_NAME, n=n,
                                                                     multi_threads=multi_threads, print_to_console=print_to_console)                                                              

    def get_{table_name_lower}_data_by_conditions(self, condition1="", condition2="", condition3="", print_to_console=True,
                                          only_count=False):
        return self.sdwis_table.get_data_by_conditions(table_name=self.TABLE_NAME, condition1=condition1,
                                                condition2=condition2, condition3=condition3,
                                                print_to_console=print_to_console, only_count=only_count)
'''

for file_name, class_name in file_class_map.items():
    table_name = class_name.upper()
    content = class_template.format(
        class_name=class_name.replace("_", ""),
        table_name=table_name,
        table_name_lower=table_name.lower()
    )

    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w') as fp:
        fp.write(content)
