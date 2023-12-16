class SdwisHTTPException(Exception):
    """
    Exception raised for HTTP-related errors in the SDWIS package.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, message="An HTTP error occurred in the SDWIS package"):
        super().__init__(message)


class SdwisQueryParamsException(Exception):
    """
    Exception raised for errors related to query parameters in SDWIS API requests.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, message="A query parameter error occurred in the SDWIS package"):
        super().__init__(message)


class SdwisResultDataParserException(Exception):
    """
    Exception raised for errors encountered while parsing results data from SDWIS API.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, message="A data parsing error occurred in the SDWIS package"):
        super().__init__(message)
