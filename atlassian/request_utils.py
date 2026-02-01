import logging
from typing import Dict, Any, Union


def get_default_logger(name):
    """Get a logger from default logging manager. If no handler
    is associated, add a default NullHandler"""

    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        # If logging is not configured in the current project, configure
        # this logger to discard all logs messages. This will  avoid
        # redirecting errors to the default 'lastResort' StreamHandler
        logger.addHandler(logging.NullHandler())
    return logger


def is_adf_content(content: Union[Dict[str, Any], str]) -> bool:
    """
    Check if content is in ADF (Atlassian Document Format) format.

    :param content: Content to check (dict or string)
    :return: True if content appears to be ADF format
    """
    if isinstance(content, str):
        return False

    if not isinstance(content, dict):
        return False

    # Basic ADF structure validation
    return content.get("type") == "doc" and content.get("version") == 1 and "content" in content


def validate_adf_structure(adf_content: Dict[str, Any]) -> bool:
    """
    Perform basic validation of ADF document structure.

    :param adf_content: ADF content dictionary
    :return: True if structure is valid
    """
    if not isinstance(adf_content, dict):
        return False

    # Check required top-level fields
    if adf_content.get("type") != "doc":
        return False

    if adf_content.get("version") != 1:
        return False

    if "content" not in adf_content:
        return False

    # Content should be a list
    if not isinstance(adf_content["content"], list):
        return False

    return True


def get_content_type_header(content: Union[Dict[str, Any], str]) -> str:
    """
    Get appropriate Content-Type header based on content format.

    :param content: Content to analyze
    :return: Content-Type header value
    """
    if is_adf_content(content):
        return "application/json"
    else:
        # Default to JSON for other structured content
        return "application/json"


def detect_content_format(content: Union[Dict[str, Any], str]) -> str:
    """
    Detect the format of content (ADF, storage, wiki, etc.).

    :param content: Content to analyze
    :return: Content format identifier
    """
    if isinstance(content, str):
        # Simple heuristics for string content
        if content.strip().startswith("<"):
            return "storage"  # HTML-like storage format
        else:
            return "wiki"  # Wiki markup

    if is_adf_content(content):
        return "adf"

    # Default to unknown for other dict structures
    return "unknown"
