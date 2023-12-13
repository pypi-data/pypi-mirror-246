from .base import BaseClient as __BaseClient, convert_bool, BaseDictObject as __BaseDictObject
from typing import List as _List


class RestrictionList(__BaseDictObject):
    """
    A list of restrictions for the specified Amazon catalog item.
    """

    def __init__(self, data):
        super().__init__(data)
        if "restrictions" in data:
            self.restrictions: _List[Restriction] = [Restriction(datum) for datum in data["restrictions"]]
        else:
            self.restrictions: _List[Restriction] = []


class Restriction(__BaseDictObject):
    """
    A listing restriction, optionally qualified by a condition, with a list of reasons for the restriction.
    """

    def __init__(self, data):
        super().__init__(data)
        if "marketplaceId" in data:
            self.marketplaceId: str = self._get_value(str, "marketplaceId")
        else:
            self.marketplaceId: str = None
        if "conditionType" in data:
            self.conditionType: str = self._get_value(str, "conditionType")
        else:
            self.conditionType: str = None
        if "reasons" in data:
            self.reasons: _List[Reason] = [Reason(datum) for datum in data["reasons"]]
        else:
            self.reasons: _List[Reason] = []


class Reason(__BaseDictObject):
    """
    A reason for the restriction, including path forward links that may allow Selling Partners to remove the restriction, if available.
    """

    def __init__(self, data):
        super().__init__(data)
        if "message" in data:
            self.message: str = self._get_value(str, "message")
        else:
            self.message: str = None
        if "reasonCode" in data:
            self.reasonCode: str = self._get_value(str, "reasonCode")
        else:
            self.reasonCode: str = None
        if "links" in data:
            self.links: _List[Link] = [Link(datum) for datum in data["links"]]
        else:
            self.links: _List[Link] = []


class Link(__BaseDictObject):
    """
    A link to resources related to a listing restriction.
    """

    def __init__(self, data):
        super().__init__(data)
        if "resource" in data:
            self.resource: str = self._get_value(str, "resource")
        else:
            self.resource: str = None
        if "verb" in data:
            self.verb: str = self._get_value(str, "verb")
        else:
            self.verb: str = None
        if "title" in data:
            self.title: str = self._get_value(str, "title")
        else:
            self.title: str = None
        if "type" in data:
            self.type: str = self._get_value(str, "type")
        else:
            self.type: str = None


class Error(__BaseDictObject):
    """
    Error response returned when the request is unsuccessful.
    """

    def __init__(self, data):
        super().__init__(data)
        if "code" in data:
            self.code: str = self._get_value(str, "code")
        else:
            self.code: str = None
        if "message" in data:
            self.message: str = self._get_value(str, "message")
        else:
            self.message: str = None
        if "details" in data:
            self.details: str = self._get_value(str, "details")
        else:
            self.details: str = None


class ErrorList(list, _List["Error"]):
    """
    A list of error responses returned when a request is unsuccessful.
    """

    def __init__(self, data):
        super().__init__([Error(datum) for datum in data])
        self.data = data


class ListingsRestrictions20210801Client(__BaseClient):
    def getListingsRestrictions(
        self,
        asin: str,
        sellerId: str,
        marketplaceIds: _List[str],
        conditionType: str = None,
        reasonLocale: str = None,
    ):
        """
                Returns listing restrictions for an item in the Amazon Catalog.
        **Usage Plan:**
        | Rate (requests per second) | Burst |
        | ---- | ---- |
        | 5 | 10 |
        The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values then those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).
        """
        url = f"/listings/2021-08-01/restrictions"
        params = {}
        if asin is not None:
            params["asin"] = asin
        if conditionType is not None:
            params["conditionType"] = conditionType
        if sellerId is not None:
            params["sellerId"] = sellerId
        if marketplaceIds is not None:
            params["marketplaceIds"] = ",".join(map(str, marketplaceIds))
        if reasonLocale is not None:
            params["reasonLocale"] = reasonLocale
        response = self.request(
            path=url,
            method="GET",
            params=params,
        )
        response_type = {
            200: RestrictionList,
            400: ErrorList,
            403: ErrorList,
            404: ErrorList,
            413: ErrorList,
            415: ErrorList,
            429: ErrorList,
            500: ErrorList,
            503: ErrorList,
        }.get(response.status_code, None)
        return None if response_type is None else response_type(self._get_response_json(response))
