import logging
from typing import Any, Dict, Generator, Iterable

from ...annotation_types.collection import LabelCollection, LabelGenerator
from .label import NDLabel

logger = logging.getLogger(__name__)

IGNORE_IF_NONE = ["page", "unit", "messageId"]


class NDJsonConverter:

    @staticmethod
    def deserialize(json_data: Iterable[Dict[str, Any]]) -> LabelGenerator:
        """
        Converts ndjson data (prediction import format) into the common labelbox format.

        Args:
            json_data: An iterable representing the ndjson data
        Returns:
            LabelGenerator containing the ndjson data.
        """
        data = NDLabel(**{'annotations': json_data})
        res = data.to_common()
        return res

    @staticmethod
    def serialize(
            labels: LabelCollection) -> Generator[Dict[str, Any], None, None]:
        """
        Converts a labelbox common object to the labelbox ndjson format (prediction import format)

        Note that this function might fail for objects that are not supported by mal.
        Not all edge cases are handling by custom exceptions, if you get a cryptic pydantic error message it is probably due to this.
        We will continue to improve the error messages and add helper functions to deal with this.

        Args:
            labels: Either a list of Label objects or a LabelGenerator
        Returns:
            A generator for accessing the ndjson representation of the data
        """
        for example in NDLabel.from_common(labels):
            res = example.dict(by_alias=True)
            for k, v in list(res.items()):
                if k in IGNORE_IF_NONE and v is None:
                    del res[k]
            yield res
