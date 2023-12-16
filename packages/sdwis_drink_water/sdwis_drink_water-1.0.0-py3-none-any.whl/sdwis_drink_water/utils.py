import re
from bs4 import BeautifulSoup

from sdwis_drink_water.errors import SdwisQueryParamsException

CHECK_API_SITE_REMINDER = "Please check official site for more information: https://www.epa.gov/enviro/sdwis-model#table_names"

TABLE_COLUMN_INCLUDE_EPA_REGION = ["GEOGRAPHIC_AREA", "LCR_SAMPLE_RESULT", "LCR_SAMPLE", "WATER_SYSTEM",
                                   "WATER_SYSTEM_FACILITY", "VIOLATION"]

BASE_TABLE_PAGE_URL = "https://enviro.epa.gov/enviro/ef_metadata_html.ef_metadata_table?p_table_name={}&p_topic=SDWIS"

CHECK_TABLE_PAGE_REMINDER = "Please check table structure for more information: "


# Helper function to process a condition_handle
def process_table_column_condition(condition_handle):
    """
    Processes a condition string for a table column.

    Parameters:
        condition_handle (str): A condition string in the format 'column>value'.

    Returns:
        str: A processed string in the format 'column/operator/value'.

    Raises:
        ValueError: If the condition string is not in the expected format.
    """
    # Split the condition_handle into its components (assumes a string like 'column>value')
    # Regular expression to match the condition pattern
    if "result_sign_code" in condition_handle:
        column = "result_sign_code"
        operator_value = condition_handle.strip().replace("result_sign_code", "")
        operator = operator_value[0]
        value = operator_value[1]
    else:
        match = re.match(r"(.*?)(>=|<=|!=|==|=|>|<)(.*)", condition_handle)
        if not match:
            raise ValueError("Condition string is not in the expected format.")

        column, operator, value = match.groups()
    parts = [column.strip(), operator.strip(), value.strip()]

    if len(parts) == 3:
        return "/".join(parts)
    else:
        raise ValueError("condition param must be a string with three parts: column, operator, and value")


def extract_description_from_description_page(html_content, desc_string='Description:'):
    """
    Extracts a description from an HTML page.

    Parameters:
        html_content (str): HTML content of the page.
        desc_string (str): The description tag to search for.

    Returns:
        str: The extracted description text or an error message.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    description_tag = soup.find('b', string=desc_string)
    # check to prevent errors
    if description_tag:
        if description_tag.next_sibling:
            description_text = description_tag.next_sibling.text.strip()
        else:
            error_text = (
                    'Description tag found, but didn\'t find content \n'
                    'Perhaps Envirofacts have modificated of the Page architecture.\n' + CHECK_API_SITE_REMINDER)
            return error_text
    else:
        error_text = (
                'Description tag not found \n'
                'Perhaps Envirofacts have modificated of the Page architecture.\n' + CHECK_API_SITE_REMINDER)
        return error_text
    return description_text


def extract_description_from_table_description_page(html_content):
    """
    Extracts a table description from an official site HTML page.

    Parameters:
        html_content (str): HTML content of the page.

    Returns:
        str: Extracted table description.
    """
    # Find the 'Description:' from official site
    return extract_description_from_description_page(html_content, desc_string='Description:')


def extract_description_from_column_description_page(html_content):
    """
    Extracts a column description from an official site HTML page.

    Parameters:
        html_content (str): HTML content of the page.

    Returns:
        str: Extracted column description.
    """
    # Find the 'Description: ' from official site
    return extract_description_from_description_page(html_content, desc_string='Description: ')


def get_table_description(table_name, session):
    """
    Retrieves the description of a table from the Envirofacts database.

    Parameters:
        table_name (str): Name of the table.
        session (requests.Session): The session used to make the request.

    Returns:
        str: Table description or an error message.
    """
    url = f"https://enviro.epa.gov/enviro/ef_metadata_html.ef_metadata_table?p_table_name={table_name}&p_topic=SDWIS"
    response = session.request(method="GET", url=url)
    if response.status_code == 200:
        return extract_description_from_table_description_page(response.text)
    else:
        error_text = (
            'Page not found \n'
            'Perhaps Envirofacts have modificated of the Envirofacts database architecture.\n'
            'Please check official site for more information: https://www.epa.gov/enviro/sdwis-model#table_names')
    return error_text


def get_column_description(column_name, session):
    """
    Retrieves the description of a column from the Envirofacts database.

    Parameters:
        column_name (str): Name of the column.
        session (requests.Session): The session used to make the request.

    Returns:
        str: Column description or an error message.
    """
    url = f"https://enviro.epa.gov/enviro/EF_METADATA_HTML.sdwis_page?p_column_name={column_name.upper()}"
    response = session.request(method="GET", url=url)
    if response.status_code == 200:
        return extract_description_from_column_description_page(response.text)
    else:
        error_text = (
            'Page not found \n'
            'Perhaps Envirofacts have modificated of the Envirofacts database architecture.\n'
            'Please check official site for more information: https://www.epa.gov/enviro/sdwis-model#table_names')
    return error_text


def print_tabulate_result_with_divider(tabulate_result):
    """
    Prints a tabulated result with dividers for better readability.

    Parameters:
        tabulate_result (str): The tabulated result to be printed.
    """
    divider = ">>" * 50
    print(f"{divider}\n{tabulate_result}\n{divider}")


def _is_table_has_epa_region(table_name):
    """
    Checks if a table includes an EPA region column.

    Parameters:
        table_name (str): Name of the table.

    Raises:
        SdwisQueryParamsException: If the table does not include an EPA region column.
    """
    if table_name not in TABLE_COLUMN_INCLUDE_EPA_REGION:
        raise SdwisQueryParamsException(f"{table_name} doesn't have \"EPA\" column\n" +
                                        CHECK_TABLE_PAGE_REMINDER + BASE_TABLE_PAGE_URL.format(table_name))


def _is_epa_region_param_valid(epa_region):
    """
    Validates the EPA region parameter.

    Parameters:
        epa_region (int): EPA region value to validate.

    Raises:
        SdwisQueryParamsException: If the epa_region is not an integer or not in the range 1-10.
    """
    if not isinstance(epa_region, int):
        raise SdwisQueryParamsException("epa_region should be int type")
    if epa_region < 0 or epa_region > 10:
        raise SdwisQueryParamsException("epa_region should be 1~10")
