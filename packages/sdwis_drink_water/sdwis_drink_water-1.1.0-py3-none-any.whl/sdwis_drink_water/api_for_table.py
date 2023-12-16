import threading
import time

from tqdm import tqdm
import logging
import tabulate

from sdwis_drink_water.api import SdwisAPI
from sdwis_drink_water.configs import TABLES_LIST, EPA_REGION_ID, MAX_QUERY_DATA_LIMIT_A_TIME
from sdwis_drink_water.data_praser import ResultDataParser
from sdwis_drink_water.errors import SdwisQueryParamsException
from sdwis_drink_water.utils import get_table_description, _is_epa_region_param_valid, _is_table_has_epa_region, \
    process_table_column_condition, print_tabulate_result_with_divider, get_column_description

log = logging.getLogger(__name__)


class SdwisTable:
    """
    A class to interact with the SDWIS Table API.

    Attributes:
        sdwis_api (SdwisAPI): Instance of the SdwisAPI class.
    """

    def __init__(self, enable_cache=True, print_url=False):
        """
        Initializes the SdwisTable class.

        Parameters:
            enable_cache (bool): Flag to enable caching of requests.
            print_url (bool): Flag to enable printing the request URL.
        """
        self.table_name = "table_name"
        self.sdwis_api = SdwisAPI(enable_cache=enable_cache, print_url=print_url)

    def _get_data_by_request(self, query_url, print_to_console=False, multi_threads=False):
        """
        Internal method to get data by sending a request to the specified URL.

        Parameters:
            query_url (str): The URL to send the request to.
            print_to_console (bool): Flag to print the result to console.
            multi_threads (bool): Flag to enable multi-threading for the request.

        Returns:
            list: The query result as a list of dictionaries.
        """
        query_result = self.sdwis_api.get_request(query_url, multi_mode=multi_threads)
        if print_to_console:
            headers = query_result[0].keys()
            values = [list(record.values()) for record in query_result]
            # tabulate_result = tabulate.tabulate(values, headers=headers)
            # print_tabulate_result_with_divider(tabulate_result)
            table = tabulate.tabulate(values, headers, tablefmt="simple_grid")
            print(table)
        return query_result

    def _get_result_data_by_request(self, query_url, print_to_console=False):
        """
        Internal method to get data by sending a request to the specified URL.

        Parameters:
            query_url (str): The URL to send the request to.
            print_to_console (bool): Flag to print the result to console.

        Returns:
            ResultDataParser: The query result as a list of dictionaries.
        """
        query_result = self.sdwis_api.get_request(query_url)
        if print_to_console:
            headers = query_result[0].keys()
            values = [list(record.values()) for record in query_result]
            tabulate_result = tabulate.tabulate(values, headers=headers, tablefmt="simple_grid")
            print_tabulate_result_with_divider(tabulate_result)
        return ResultDataParser(query_result)

    def get_all_table_names(self, print_to_console=True):
        """
        Retrieves all table names from the SDWIS database.

        Parameters:
            print_to_console (bool): Flag to print the table names to console.

        Returns:
            list: A list of all table names.
        """
        if print_to_console:
            header = [self.table_name]
            tabulate_result = tabulate.tabulate([[i] for i in TABLES_LIST], headers=header)
            print_tabulate_result_with_divider(tabulate_result)
            return TABLES_LIST
        else:
            return TABLES_LIST

    def get_all_table_names_and_descriptions(self, print_to_console=True):
        """
        Retrieves all table names and their descriptions from the SDWIS database.

        Parameters:
            print_to_console (bool): Flag to print the table names and descriptions to console.

        Returns:
            list or dict: A list of table names and descriptions or a dictionary if not printed.
        """
        table_descriptions = []
        for table_name in tqdm(TABLES_LIST, desc='Fetching table descriptions from SDWIS Official Website'):
            description = get_table_description(table_name, session=self.sdwis_api.multi_threads_session)
            table_descriptions.append(description)

        if print_to_console:
            headers = ["table_name", "description"]
            table_name_description_list = [[TABLES_LIST[i], table_descriptions[i]] for i in range(len(TABLES_LIST))]
            tabulate_result = tabulate.tabulate(table_name_description_list, headers=headers, tablefmt="simple_grid")
            print_tabulate_result_with_divider(tabulate_result)
            return tabulate_result
        else:
            return dict(zip(TABLES_LIST, table_descriptions))

    def get_table_column_name_by_table_name(self, table_name="", print_to_console=True):
        """
        Retrieves column names for a specified table.

        Parameters:
            table_name (str): Name of the table.
            print_to_console (bool): Flag to print the column names to console.

        Returns:
            list: A list of column names for the specified table.
        """
        first_data = self.get_table_first_data_by_table_name(table_name=table_name, print_to_console=False)
        if print_to_console:
            column_names = list(first_data.get_all_keys())
            print(column_names)
            # headers = [f"COLUMN_{i + 1}" for i in range(len(column_names))]
            # tabulate_result = tabulate.tabulate([column_names], headers=headers, numalign="right", stralign="right")
            # print_tabulate_result_with_divider(tabulate_result)
        return first_data.get_all_keys()

    def get_columns_description_by_table_name(self, table_name="", print_to_console=True, multi_threads=False):
        """
        Retrieves descriptions for all columns of a specified table.

        Parameters:
            table_name (str): Name of the table.
            print_to_console (bool): Flag to print column descriptions to console.
            multi_threads (bool): Flag to enable multi threads requests.

        Returns:
            dict: A dictionary mapping column names to their descriptions.
        """
        first_data = self.get_table_first_data_by_table_name(table_name=table_name, print_to_console=False)
        column_names = list(first_data.get_all_keys())
        column_descriptions = []
        if multi_threads:
            def thread_task(column_name_):
                description_ = get_column_description(column_name_, session=self.sdwis_api.multi_threads_session)
                column_descriptions.append(description_)
                pbar.update(1)

            pbar = tqdm(total=len(column_names),
                        desc=f"Fetching column descriptions for {table_name}"
                             f" from SDWIS Official Website by multi_threads_mode")
            threads = []
            for column_name in column_names:
                thread = threading.Thread(target=thread_task, args=(column_name,))
                threads.append(thread)
                thread.start()
                if len(threads) >= len(column_names):
                    for t in threads:
                        t.join()
                    threads = []
            for t in threads:
                t.join()
            pbar.close()
        else:
            for column_name in tqdm(column_names,
                                    desc=f"Fetching column descriptions for {table_name} from SDWIS Official Website"):
                description = get_column_description(column_name, session=self.sdwis_api.session)
                column_descriptions.append(description)

        if print_to_console:
            headers = ["column_names", "description"]
            table_column_description_list = [[column_names[i], column_descriptions[i]] for i in
                                             range(len(column_names))]
            tabulate_result = tabulate.tabulate(table_column_description_list, headers=headers, tablefmt="simple_grid")
            print_tabulate_result_with_divider(tabulate_result)
        return dict(zip(column_names, column_descriptions))

    def get_table_data_number(self, table_name=""):
        """
        Retrieves the number of records in a specified table.

        Parameters:
            table_name (str): Name of the table.

        Returns:
            int: The total number of records in the table.
        """
        total_data_number = self.get_data_by_conditions(table_name=table_name, print_to_console=False, only_count=True)
        return total_data_number

    def get_table_first_data_by_table_name(self, table_name="", print_to_console=True):
        """
        Retrieves the first record of a specified table.

        Parameters:
            table_name (str): Name of the table.
            print_to_console (bool): Flag to print the first record to console.

        Returns:
            dict or ResultDataParser: The first record of the table.
        """
        return self.get_table_first_n_data_by_table_name(table_name=table_name, print_to_console=print_to_console, n=1)

    def get_table_first_n_data_by_table_name(self, table_name="", n=0, print_to_console=True, multi_threads=False):
        """
        Retrieves the first 'n' records of a specified table.

        Parameters:
            table_name (str): Name of the table.
            n (int): Number of records to retrieve.
            print_to_console (bool): Flag to print the records to console.
            multi_threads (bool): Flag to enable multi-threading.

        Returns:
            list or ResultDataParser: A list of the first 'n' records from the table.
        """
        # Handle requests exceeding the maximum limit, should divide to several request
        if n > MAX_QUERY_DATA_LIMIT_A_TIME:
            query_result = []
            print(table_name)
            total_data = self.get_data_by_conditions(table_name=table_name, print_to_console=False, only_count=True)
            if n >= total_data:
                print(
                    f"The data number in the database provided by the API is {total_data}."
                    f" Your request number exceeds this limit, please note.")
                n = total_data - 1

            # Calculate the number of full batches and the remainder for the last batch
            num_full_batches = n // MAX_QUERY_DATA_LIMIT_A_TIME
            remainder = n % MAX_QUERY_DATA_LIMIT_A_TIME
            batches = []
            for i in range(num_full_batches):
                start = i * MAX_QUERY_DATA_LIMIT_A_TIME
                end = (i + 1) * MAX_QUERY_DATA_LIMIT_A_TIME - 1
                batches.append([start, end])
            # Handling the last batch if there's a remainder
            if remainder != 0:
                start = num_full_batches * MAX_QUERY_DATA_LIMIT_A_TIME
                end = n - 1
                batches.append([start, end])
            if multi_threads:
                def thread_task(start_row_, end_row_):
                    query_url_ = f"{self.sdwis_api.base_url}/{table_name}/rows/{start_row_}:{end_row_}"
                    partial_query_result_ = self._get_data_by_request(query_url_,
                                                                      print_to_console=print_to_console,
                                                                      multi_threads=True)
                    query_result.extend(partial_query_result_)

                pbar = tqdm(total=len(batches),
                            desc=f"Fetching Data by multi_threads_mode")
                threads = []
                for i in tqdm(range(len(batches))):
                    start_row = batches[i][0]
                    end_row = batches[i][1]
                    thread = threading.Thread(target=thread_task, args=(start_row, end_row))
                    threads.append(thread)
                    if i > 10:
                        time.sleep(2)
                    thread.start()
                    if len(threads) >= len(batches):
                        for t in threads:
                            t.join()
                        threads = []
                for t in threads:
                    t.join()
                pbar.close()
            else:
                # Output the batches
                for i in tqdm(range(len(batches)), desc="Fetching Data"):
                    start_row = batches[i][0]
                    end_row = batches[i][1]
                    query_url = f"{self.sdwis_api.base_url}/{table_name}/rows/{start_row}:{end_row}"
                    partial_query_result = self._get_data_by_request(query_url, print_to_console=print_to_console)
                    query_result.extend(partial_query_result)
        else:
            query_url = f"{self.sdwis_api.base_url}/{table_name}/rows/0:{n - 1}"
            query_result = self._get_data_by_request(query_url, print_to_console=print_to_console)
        return ResultDataParser(query_result)

    def get_data_by_conditions(self, table_name="", condition1="", condition2="", condition3="", print_to_console=True,
                               only_count=False):
        """
        Retrieves data from a table based on specified conditions.

        Parameters:
            table_name (str): Name of the table.
            condition1(str): Conditions for data retrieval.
            condition2(str): Conditions for data retrieval.
            condition3(str): Conditions for data retrieval.
            print_to_console (bool): Flag to print the results to console.
            only_count (bool): Flag to retrieve only the count of matching records.

        Returns:
            list or int: List of matching records, or count of records if only_count is True.
        """
        if table_name == "":
            raise SdwisQueryParamsException("table name can't not be empty")
        #  conditions_list contains all the processed conditions
        conditions_url_list = [self.sdwis_api.base_url, table_name]
        conditions_list = []
        # Process each condition_handle if it's not empty
        if condition1 != "":
            conditions_list.append(process_table_column_condition(condition1))
        if condition2 != "":
            conditions_list.append(process_table_column_condition(condition2))
        if condition3 != "":
            conditions_list.append(process_table_column_condition(condition3))

        conditions_url_list = conditions_url_list + conditions_list
        query_url = "/".join(conditions_url_list)
        if only_count:
            total_number = self.sdwis_api.get_request(query_url, only_count=only_count)
            if print_to_console:
                header = ["CONDITION(s)", "DATA_NUMBER_MATCH_CONDITION"]
                tabulate_result = tabulate.tabulate([[" & ".join(conditions_list), total_number]], headers=header,
                                                    tablefmt="simple_grid")
                print_tabulate_result_with_divider(tabulate_result)
            return total_number
        else:
            return self._get_result_data_by_request(query_url)

    def summarize_data_by_epa_region(self, table_name="", print_to_console=True, multi_threads=False):
        """
        Summarizes data by EPA region for a specified table.

        Parameters:
            table_name (str): Name of the table.
            print_to_console (bool): Flag to print summary to console.
            multi_threads (bool): Flag to enable multi-threading.

        Returns:
            list: A list containing the data summary by EPA region.
        """
        _is_table_has_epa_region(table_name)
        data_number_list = []

        if multi_threads:
            def thread_task(multi_epa_region_id):
                multi_data_number = self.get_data_by_epa_region(table_name=table_name, epa_region=multi_epa_region_id,
                                                                only_count=True, print_to_console=False,
                                                                multi_mode=multi_threads)
                data_number_list.append(multi_data_number)
                pbar.update(1)

            pbar = tqdm(total=len(EPA_REGION_ID),
                        desc=f"Fetching the total amount of data by EPA region from the {table_name} data table")
            threads = []
            for epa_region_id in EPA_REGION_ID:
                thread = threading.Thread(target=thread_task, args=(epa_region_id,))
                threads.append(thread)
                thread.start()
                if len(threads) >= 10:
                    for t in threads:
                        t.join()
                    threads = []
            for t in threads:
                t.join()
            pbar.close()
        else:
            for epa_region_id in tqdm(EPA_REGION_ID,
                                      desc=F"Fetching the total amount of data by EPA region from the \"{table_name}\" "
                                           F"table"):
                data_number = self.get_data_by_epa_region(table_name=table_name, epa_region=epa_region_id,
                                                          only_count=True, print_to_console=False)
                data_number_list.append(data_number)

        if print_to_console:
            header = ["EPA_REGION_ID", f"{table_name}_TOTAL_NUMBER"]
            tabulate_result = tabulate.tabulate(
                [[f"EPA_REGION_{i}", data_number_list[i - 1]] for i in EPA_REGION_ID],
                headers=header, numalign="right", stralign="right", tablefmt="simple_grid")
            print_tabulate_result_with_divider(tabulate_result)
        else:
            return data_number_list

    def get_data_by_epa_region(self, table_name="", epa_region=1, print_to_console=True, only_count=False,
                               multi_mode=False):
        """
        Retrieves data from a table filtered by a specific EPA region.
        SAMPLE URL: https://data.epa.gov/efservice/LCR_SAMPLE/EPA_REGION/=/01/JSON
        Parameters:
            table_name (str): Name of the table.
            epa_region (int): EPA region number.
            print_to_console (bool): Flag to print the results to console.
            only_count (bool): Flag to retrieve only the count of records.
            multi_mode (bool): Flag to enable multi-threading.

        Returns:
            list or int: List of records or count of records if only_count is True.
        """
        _is_table_has_epa_region(table_name)
        _is_epa_region_param_valid(epa_region)
        column_name = "EPA_REGION"
        string_epa_region = f"0{epa_region}" if epa_region < 10 else epa_region
        query_url = f"{self.sdwis_api.base_url}/{table_name}/{column_name}/=/{string_epa_region}"
        if only_count:
            header = ["EPA_REGION_ID", f"{table_name}_TOTAL_NUMBER"]
            total_number = self.sdwis_api.get_request(query_url, only_count=only_count, multi_mode=multi_mode)
            if print_to_console:
                tabulate_result = tabulate.tabulate([[f"EPA_REGION_{string_epa_region}", total_number]], headers=header,
                                                    tablefmt="simple_grid")
                print_tabulate_result_with_divider(tabulate_result)
            return total_number
        else:
            return self._get_result_data_by_request(query_url, print_to_console=print_to_console)
