import json
import pandas as pd
import re

import tabulate

from sdwis_drink_water.errors import SdwisHTTPException, SdwisResultDataParserException


class Parser:
    def parse(self, payload, *args, **kwargs):
        """
        Parse the response payload and return the result.
        """
        raise NotImplementedError


class SDWISJSONParser(Parser):
    """
    [
    {
        "pwsid": "010502003",
        "sample_id": "01050200317607",
        "primacy_agency_code": "01",
        "epa_region": "01",
        "sar_id": 18509157,
        "contaminant_code": "PB90",
        "result_sign_code": "=",
        "sample_measure": 0.029,
        "unit_of_measure": "mg/L"
    },
    {
        "pwsid": "041210001",
        "sample_id": "041461",
        "primacy_agency_code": "04",
        "epa_region": "04",
        "sar_id": 17717185,
        "contaminant_code": "PB90",
        "result_sign_code": null,
        "sample_measure": 0.031,
        "unit_of_measure": "mg/L"
    }
    ]
    """

    def parse(self, payload, *args, **kwargs):
        if not payload:
            return
        try:
            json_result = json.loads(payload)
        except Exception as e:
            raise SdwisHTTPException(f'Failed to load payload as JSON Format {e}')
        return json_result

    def parse_count_result(self, count_result):
        return count_result[0]["TOTALQUERYRESULTS"]


class ResultDataParser:
    def __init__(self, data):
        """
        Initialize with data, which is a list of dictionaries.
        """
        self.data = data

    def get_first_n_records(self, n):
        """
        Return the first n records from the data.
        """
        return ResultDataParser(self.data[:n])

    def count(self):
        """
        Return the first n records from the data.
        """
        return len(self.data)

    def show(self):
        """
        Return the first n records from the data.
        """
        query_result = self.data
        headers = query_result[0].keys()
        values = [list(record.values()) for record in query_result]
        tabulate_result = tabulate.tabulate(values, headers=headers, tablefmt="simple_grid")
        # print_tabulate_result_with_divider(tabulate_result)
        print(tabulate_result)

    def _get_column_values(self, key):
        """
        Extract all values for a given key from the data.
        """
        return [record[key] for record in self.data if key in record]

    def _get_column_values_with_records(self, key):
        """
        Extract all values for a given key from the data along with their corresponding records.
        """
        return [(record[key], record) for record in self.data if key in record]

    def find_max(self, key):
        """
        Find the maximum value(s) and corresponding records for a given key.
        """
        values_with_records = self._get_column_values_with_records(key)
        if values_with_records:
            max_val = max(value for value, _ in values_with_records)
            return ResultDataParser([record for value, record in values_with_records if value == max_val])
        return ResultDataParser([])

    def find_min(self, key):
        """
        Find the minimum value(s) and corresponding records for a given key.
        """
        values_with_records = self._get_column_values_with_records(key)
        if values_with_records:
            min_val = min(value for value, _ in values_with_records)
            return ResultDataParser([record for value, record in values_with_records if value == min_val])
        return ResultDataParser([])

    def _parse_condition(self, condition):
        match = re.match(r"(.*?)(>=|<=|!=|==|=|>|<)(.*)", condition)
        if not match:
            raise ValueError("Condition string is not in the expected format.")
        key, operator, value = match.groups()
        key, operator, value = key.strip(), operator.strip(), value.strip()
        if operator == "=":
            operator = "=="
        return key, operator, value

    def _filter_by_condition(self, condition):
        key, operator, value = self._parse_condition(condition)
        filtered_records = []
        for record in self.data:
            if key in record:
                record_value = record[key]
                if eval(f"'{record_value}' {operator} '{value}'"):
                    filtered_records.append(record)
        return filtered_records

    def find_min_with_condition(self, key, condition):
        filtered_data = self._filter_by_condition(condition)
        if not filtered_data:
            return ResultDataParser([])
        min_value = min(record[key] for record in filtered_data if key in record)
        return ResultDataParser([record for record in filtered_data if record[key] == min_value])

    def find_max_with_condition(self, key, condition):
        filtered_data = self._filter_by_condition(condition)
        if not filtered_data:
            return ResultDataParser([])
        max_value = max(record[key] for record in filtered_data if key in record)
        return ResultDataParser([record for record in filtered_data if record[key] == max_value])

    def find_by_condition(self, condition):
        """
        Find records that match a condition like 'KEY>value'.
        """
        filtered_data = self._filter_by_condition(condition)
        if not filtered_data:
            return ResultDataParser([])
        return ResultDataParser(filtered_data)

    def get_all_keys(self):
        """
        Return a set of all keys in the data.
        """
        all_keys = self.data[0].keys()
        return all_keys

    def export_data(self, filename, format_type="csv"):
        """
        Export data to a file in the specified format.
        """
        if len(self.data) == 0:
            raise SdwisResultDataParserException("empty result can't be exported")
        df = pd.DataFrame(self.data)
        if format_type == "parquet":
            df.to_parquet(filename)
        elif format_type == "xlsx":
            df.to_excel(filename, index=False)
        elif format_type == "csv":
            df.to_csv(filename, index=False)
        elif format_type == "txt":
            df.to_csv(filename, index=False, sep='\t')
        else:
            raise SdwisResultDataParserException("Unsupported file format.")
        print(f"Data is successfully exported to {filename}!")

    def intersect_with(self, other_data):
        """
        Find the intersection of the current data with the specified data.
        Args:
            other_data (ResultDataParser): The specified data to intersect with.
        Returns:
            ResultDataParser: New instance containing the intersecting records.
        """
        if not isinstance(other_data, ResultDataParser):
            raise ValueError("other_data must be a \"ResultDataParser\" class")

        other_data = other_data.data

        # Convert other_data to a set of frozensets and find intersection
        other_data_set = set(frozenset(record.items()) for record in other_data)
        intersection = [record for record in self.data if frozenset(record.items()) in other_data_set]

        return ResultDataParser(intersection)

    def difference_with(self, other_data):
        """
        Find the difference between the current data and specified data.
        Args:
            other_data (ResultDataParser): The specified data to compare with.
        Returns:
            ResultDataParser: New instance containing the difference.
        """
        if not isinstance(other_data, ResultDataParser):
            raise ValueError("other_data must be a \"ResultDataParser\" class")

        other_data_set = set(frozenset(record.items()) for record in other_data.data)
        difference = [record for record in self.data if frozenset(record.items()) not in other_data_set]

        return ResultDataParser(difference)

    def merge_with(self, other_data):
        """
        Merge the current data with the specified data.
        Args:
            other_data (ResultDataParser): The specified data to merge with.
        Returns:
            ResultDataParser: New instance containing the merged data.
        """
        if not isinstance(other_data, ResultDataParser):
            raise ValueError("other_data must be a \"ResultDataParser\" class")

        merged_data = self.data + [record for record in other_data.data if
                                   frozenset(record.items()) not in set(frozenset(r.items()) for r in self.data)]
        return ResultDataParser(merged_data)

    def remove_key(self, key_to_remove):
        """
        Remove a specified key from all data records.
        Args:
            key_to_remove (str): The key to be removed from the data records.
        Returns:
            ResultDataParser: New instance with the key removed from all records.
        """
        modified_data = []
        for record in self.data:
            # Create a copy of the record and remove the key if it exists
            modified_record = {key: value for key, value in record.items() if key != key_to_remove}
            modified_data.append(modified_record)

        return ResultDataParser(modified_data)
