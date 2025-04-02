"""
Jira API specific error classes
"""

import json
import logging
from typing import Dict, Optional, Union

from requests import Response

from atlassian.errors import (
    ApiConflictError,
    ApiError,
    ApiNotFoundError,
    ApiPermissionError,
    ApiValueError,
)

log = logging.getLogger(__name__)


class JiraApiError(ApiError):
    """Base class for Jira API errors with enhanced metadata"""

    def __init__(self, message: str, response: Optional[Response] = None, reason: Optional[str] = None):
        """
        Initialize a JiraApiError

        Args:
            message: Error message
            response: Optional HTTP response object
            reason: Optional reason message
        """
        self.response = response
        self.status_code = response.status_code if response else None
        
        # Extract error details from JSON response if available
        self.error_messages = []
        self.errors = {}
        
        if response and response.text:
            try:
                error_data = json.loads(response.text)
                self.error_messages = error_data.get("errorMessages", [])
                self.errors = error_data.get("errors", {})
                
                # If reason not provided, try to extract it from the response
                if not reason:
                    if self.error_messages:
                        reason = self.error_messages[0]
                    elif self.errors and isinstance(self.errors, dict):
                        reason = next(iter(self.errors.values()), None)
            except json.JSONDecodeError:
                # If the response is not JSON, use the raw text
                if not reason and response.text:
                    reason = response.text[:100]  # Truncate long error messages
        
        super().__init__(message, reason=reason)
    
    def __str__(self) -> str:
        """User-friendly string representation of the error"""
        result = self.args[0] if self.args else "Jira API Error"
        if self.status_code:
            result = f"{result} (HTTP {self.status_code})"
        if self.error_messages:
            result = f"{result}: {', '.join(self.error_messages)}"
        elif self.reason:
            result = f"{result}: {self.reason}"
        return result


class JiraNotFoundError(JiraApiError, ApiNotFoundError):
    """Raised when a requested resource is not found (404)"""
    pass


class JiraPermissionError(JiraApiError, ApiPermissionError):
    """Raised when the user doesn't have permission to access a resource (403)"""
    pass


class JiraValueError(JiraApiError, ApiValueError):
    """Raised when there's a problem with the values provided (400)"""
    pass


class JiraConflictError(JiraApiError, ApiConflictError):
    """Raised when there's a conflict with the current state of the resource (409)"""
    pass


class JiraAuthenticationError(JiraApiError):
    """Raised when authentication fails (401)"""
    pass


class JiraRateLimitError(JiraApiError):
    """Raised when API rate limit is exceeded (429)"""
    
    def __init__(self, message: str, response: Optional[Response] = None, reason: Optional[str] = None):
        super().__init__(message, response, reason)
        
        # Extract retry-after information if available
        if response and 'Retry-After' in response.headers:
            self.retry_after = int(response.headers['Retry-After'])
        else:
            self.retry_after = None


class JiraServerError(JiraApiError):
    """Raised when the Jira server encounters an error (5xx)"""
    pass


def raise_error_from_response(response: Response, message: Optional[str] = None) -> None:
    """
    Raise an appropriate error based on the response status code

    Args:
        response: HTTP response object
        message: Optional custom error message

    Raises:
        JiraNotFoundError: When status code is 404
        JiraPermissionError: When status code is 403
        JiraAuthenticationError: When status code is 401
        JiraValueError: When status code is 400
        JiraConflictError: When status code is 409
        JiraRateLimitError: When status code is 429
        JiraServerError: When status code is 5xx
        JiraApiError: For any other error status code
    """
    if response.status_code < 400:
        return
        
    default_message = f"Jira API error: {response.status_code} {response.reason}"
    error_message = message or default_message
    
    if response.status_code == 404:
        raise JiraNotFoundError(error_message, response)
    elif response.status_code == 403:
        raise JiraPermissionError(error_message, response)
    elif response.status_code == 401:
        raise JiraAuthenticationError(error_message, response)
    elif response.status_code == 400:
        raise JiraValueError(error_message, response)
    elif response.status_code == 409:
        raise JiraConflictError(error_message, response)
    elif response.status_code == 429:
        raise JiraRateLimitError(error_message, response)
    elif 500 <= response.status_code < 600:
        raise JiraServerError(error_message, response)
    else:
        raise JiraApiError(error_message, response) 