"""
This module is an example of a feature module.
A feature can be implemented as a function or a class.
Examples are shown for both below.
"""

from typing import List  # type hinting or annotation


def example_feature_function(feature_argument: str) -> List[str]:
    """
    Performs a feature operation.

    :param feature_argument: Feature argument.
    :return: Result of operation.
    """

    return NotImplementedError


class ExampleFeatureClass:
    def __init__(self, feature_argument: str):
        self.feature_argument = feature_argument

    def example_feature(self) -> List[str]:
        """
        Performs a feature operation.

        :return: Result of operation.
        """

        return NotImplementedError
