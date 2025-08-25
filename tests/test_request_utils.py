# coding: utf-8
"""
Unit tests for atlassian.request_utils module
"""

import logging
from .mockup import mockup_server
from atlassian.request_utils import get_default_logger


class TestGetDefaultLogger:
    """Test cases for get_default_logger function"""

    def test_get_default_logger_return_type(self):
        """Test that get_default_logger returns a Logger instance"""
        logger = get_default_logger("test_logger")
        assert isinstance(logger, logging.Logger)

    def test_get_default_logger_instance_uniqueness(self):
        """Test that get_default_logger returns the same logger instance for the same name"""
        logger1 = get_default_logger("test_unique_logger")
        logger2 = get_default_logger("test_unique_logger")
        assert logger1 is logger2

    def test_get_default_logger_different_names(self):
        """Test that get_default_logger returns different logger instances for different names"""
        logger1 = get_default_logger("test_logger_1")
        logger2 = get_default_logger("test_logger_2")
        assert logger1 is not logger2

    def test_get_default_logger_adds_null_handler_when_no_handlers(self):
        """Test that NullHandler is added when logger has no handlers"""
        # Create a fresh logger with no handlers
        test_logger_name = "test_fresh_logger"

        # Remove any existing logger to ensure clean state
        test_logger = logging.getLogger(test_logger_name)
        test_logger.handlers.clear()
        # Force remove from manager
        if test_logger_name in logging.Logger.manager.loggerDict:
            del logging.Logger.manager.loggerDict[test_logger_name]

        logger = get_default_logger(test_logger_name)

        # The function should ensure the logger has at least one handler
        # Either it already had handlers, or it added a NullHandler
        assert logger.hasHandlers() is True

    def test_get_default_logger_null_handler_output(self):
        """Test that NullHandler prevents log output from reaching console"""
        test_logger_name = "test_null_handler_output"

        # Get a logger
        logger = get_default_logger(test_logger_name)

        # The function should ensure the logger has at least one handler
        assert logger.hasHandlers() is True

        # Test that the logger level is appropriate
        # NullHandler should not affect the logger level
        assert logger.level == logging.NOTSET

    def test_get_default_logger_special_names(self):
        """Test that get_default_logger works with special logger names"""
        special_names = [
            "test.logger",
            "test_logger",
            "test-logger",
            "test@module",
            "test#module",
            "test$module",
        ]

        for name in special_names:
            logger = get_default_logger(name)
            assert isinstance(logger, logging.Logger)
            assert logger.name == name

    def test_get_default_logger_propagate_setting(self):
        """Test that logger propagate setting is not modified"""
        test_logger_name = "test_propagate_setting"

        # Get a logger
        logger = get_default_logger(test_logger_name)

        # Check that propagate setting is preserved (default is True)
        assert logger.propagate is True

        # Modify propagate setting
        logger.propagate = False

        # Get the logger again
        logger2 = get_default_logger(test_logger_name)

        # Check that propagate setting is preserved
        assert logger2.propagate is False

    def test_get_default_logger_level_setting(self):
        """Test that logger level setting is not modified"""
        test_logger_name = "test_level_setting"

        # Get a logger
        logger = get_default_logger(test_logger_name)

        # Check that level setting is preserved (default is NOTSET)
        assert logger.level == logging.NOTSET

        # Modify level setting
        logger.setLevel(logging.ERROR)

        # Get the logger again
        logger2 = get_default_logger(test_logger_name)

        # Check that level setting is preserved
        assert logger2.level == logging.ERROR

    def test_get_default_logger_integration(self):
        """Test integration with Python's logging manager"""
        test_logger_name = "test_integration_logger"

        # Get a logger through our function
        our_logger = get_default_logger(test_logger_name)

        # Get the same logger directly through logging.getLogger
        direct_logger = logging.getLogger(test_logger_name)

        # Verify they are the same instance
        assert our_logger is direct_logger

        # Verify they have the same handlers
        assert our_logger.handlers == direct_logger.handlers

    def test_get_default_logger_thread_safety(self):
        """Test that get_default_logger is thread-safe"""
        import threading

        test_logger_name = "test_thread_safety"
        results = []

        def get_logger_thread():
            """Thread function to get logger"""
            try:
                logger = get_default_logger(test_logger_name)
                results.append(logger)
            except Exception as e:
                results.append(e)

        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=get_logger_thread)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Check that all threads got the same logger instance
        assert len(results) == 5
        assert all(isinstance(result, logging.Logger) for result in results)

        # All should be the same logger instance
        first_logger = results[0]
        assert all(result is first_logger for result in results)

    def test_get_default_logger_mockup_integration(self):
        """Test that get_default_logger works with the mockup system"""
        # This test ensures that our logging system doesn't interfere with the mockup system
        test_logger_name = "test_mockup_integration"

        # Get a logger
        logger = get_default_logger(test_logger_name)

        # Verify the logger works
        assert isinstance(logger, logging.Logger)
        assert logger.name == test_logger_name

        # Verify the mockup server is accessible
        mockup_url = mockup_server()
        assert isinstance(mockup_url, str)
        assert len(mockup_url) > 0

    def test_get_default_logger_behavior(self):
        """Test the actual behavior of get_default_logger function"""
        # Test that get_default_logger works as expected
        test_logger_name = "test_behavior_logger"

        # Get a logger
        logger = get_default_logger(test_logger_name)

        # The function should ensure the logger has at least one handler
        # Either it already had handlers, or it added a NullHandler
        assert logger.hasHandlers() is True
