import logging
import requests_cache
from requests.exceptions import Timeout
import requests
from sdwis_drink_water.data_praser import SDWISJSONParser
from sdwis_drink_water.errors import SdwisHTTPException, SdwisQueryParamsException
from sdwis_drink_water.utils import get_table_description, _is_epa_region_param_valid, _is_table_has_epa_region

log = logging.getLogger(__name__)


class SdwisAPI:
    """
    The SdwisAPI class provides an interface to interact with the EPA's SDWIS data service.
    It supports making HTTP requests with optional caching and retries.

    Attributes:
        base_url (str): The base URL for the EPA's data service.
        retry_count (int): Number of times to retry a request on failure.
        retry_delay (int): Delay between retries in seconds.
        timeout (int): Timeout for the HTTP requests.
        enable_cache (bool): Flag to enable or disable request caching.
        cache_time (int): Duration for which the cache is valid.
        print_url (bool): Flag to enable or disable printing of the request URL.
        user_agent (str): User agent string for the HTTP requests.
    """
    def __init__(
            self, base_url='https://data.epa.gov/efservice', retry_count=0, retry_delay=0,
            timeout=10, user_agent=None, enable_cache=True, cache_time=3600, print_url=False
    ):
        """
        Initializes the SdwisAPI object with given configuration.

        Parameters:
            base_url (str): The base URL for the EPA's data service.
            retry_count (int): Number of times to retry a request on failure.
            retry_delay (int): Delay between retries in seconds.
            timeout (int): Timeout for the HTTP requests.
            user_agent (str): User agent string for the HTTP requests.
            enable_cache (bool): Flag to enable or disable request caching.
            cache_time (int): Duration for which the cache is valid.
            print_url (bool): Flag to enable or disable printing of the request URL.
        """
        self.base_url = base_url
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.enable_cache = enable_cache
        self.cache_time = cache_time
        self.print_url = print_url
        self.parser = SDWISJSONParser()

        if user_agent is None:
            user_agent = (
                f"sdwis_drink_water"
            )
        self.user_agent = user_agent

        if self.enable_cache:
            self.session = requests_cache.CachedSession('sdwis_drink_water_cache', expire_after=self.cache_time)
        else:
            self.session = requests.Session()
        self.multi_threads_session = requests.Session()

    def get_request(self, url, endpoint_parameters=(), params=None, only_count=False,
                    headers=None, use_cache=True, multi_mode=False, **kwargs):
        """
        Sends a GET request to the specified URL with optional parameters.

        Parameters:
            url (str): The URL to send the request to.
            endpoint_parameters (tuple): Additional parameters for the endpoint.
            params (dict): Query parameters for the request.
            only_count (bool): Flag to return only count in the response.
            headers (dict): HTTP headers for the request.
            use_cache (bool): Flag to use cache for the request.
            multi_mode (bool): Flag to enable or disable multi-threading mode.
            kwargs: Additional keyword arguments.

        Returns:
            dict or int: Parsed JSON response from the API / Or number

        Raises:
            SdwisHTTPException: If the HTTP request fails or returns an error.
        """
        if only_count:
            url = f"{url}/COUNT"

        # only handle data of json format response
        url = f"{url}/JSON"

        if self.print_url:
            # print(f"=" * 100)
            print(f"FETCHING DATA FROM: {url}")
        if headers is None:
            headers = {"Content-Type": "application/json"}
        headers["User-Agent"] = self.user_agent

        if params is None:
            params = {}
        for k, arg in kwargs.items():
            if arg is None:
                continue
            if k not in endpoint_parameters + (
                    "include_ext_edit_control", "tweet_mode"
            ):
                log.warning(f'Unexpected parameter: {k}')
            params[k] = str(arg)
        log.debug("PARAMS: %r", params)

        fail_counter = 0
        success = False
        resp = None
        while fail_counter <= self.retry_count:
            try:
                if multi_mode:
                    resp = self.multi_threads_session.request(
                        method="GET", url=url, params=params, headers=headers, timeout=self.timeout
                    )
                else:
                    resp = self.session.request(
                        method="GET", url=url, params=params, headers=headers, timeout=self.timeout
                    )
                if resp.status_code == 200:
                    success = True
                    break
            except Timeout:
                print(f"Timeout Exception: counter={fail_counter}/{self.retry_count} || query_url:{url}")
            except Exception as e:
                print(
                    f"Exception: counter={fail_counter}/{self.retry_count} || query_url:{url}")
            finally:
                self.multi_threads_session.close()
                self.session.close()

        if success is False or resp is None:
            if resp is None:
                raise SdwisHTTPException("EmptyResponse")
            if resp.status_code == 400:
                raise SdwisHTTPException("BadRequest")
            if resp.status_code == 401:
                raise SdwisHTTPException("Unauthorized")
            if resp.status_code == 403:
                raise SdwisHTTPException("Forbidden")
            if resp.status_code == 404:
                raise SdwisHTTPException("NotFound")
            if resp.status_code == 429:
                raise SdwisHTTPException("TooManyRequests")
            if resp.status_code >= 500:
                raise SdwisHTTPException("ServerError")
            # if not 200 and above error status code
            raise SdwisHTTPException(resp)
        else:
            json_result = self.parser.parse(resp.text)
            if only_count:
                json_result = self.parser.parse_count_result(json_result)
            return json_result
