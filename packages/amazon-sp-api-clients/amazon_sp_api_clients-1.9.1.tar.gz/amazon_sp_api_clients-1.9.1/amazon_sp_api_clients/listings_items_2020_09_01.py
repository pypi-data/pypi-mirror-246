from .base import BaseClient as __BaseClient, convert_bool, BaseDictObject as __BaseDictObject
from typing import List as _List


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


class ErrorList(__BaseDictObject):
    """
    A list of error responses returned when a request is unsuccessful.
    """

    def __init__(self, data):
        super().__init__(data)
        if "errors" in data:
            self.errors: _List[Error] = [Error(datum) for datum in data["errors"]]
        else:
            self.errors: _List[Error] = []


class Issue(__BaseDictObject):
    """
    An issue with a listings item.
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
        if "severity" in data:
            self.severity: str = self._get_value(str, "severity")
        else:
            self.severity: str = None
        if "attributeName" in data:
            self.attributeName: str = self._get_value(str, "attributeName")
        else:
            self.attributeName: str = None


class PatchOperation(__BaseDictObject):
    """
    Individual JSON Patch operation for an HTTP PATCH request.
    """

    def __init__(self, data):
        super().__init__(data)
        if "op" in data:
            self.op: str = self._get_value(str, "op")
        else:
            self.op: str = None
        if "path" in data:
            self.path: str = self._get_value(str, "path")
        else:
            self.path: str = None
        if "value" in data:
            self.value: _List[dict] = [dict(datum) for datum in data["value"]]
        else:
            self.value: _List[dict] = []


class ListingsItemPatchRequest(__BaseDictObject):
    """
    The request body schema for the patchListingsItem operation.
    """

    def __init__(self, data):
        super().__init__(data)
        if "productType" in data:
            self.productType: str = self._get_value(str, "productType")
        else:
            self.productType: str = None
        if "patches" in data:
            self.patches: _List[PatchOperation] = [PatchOperation(datum) for datum in data["patches"]]
        else:
            self.patches: _List[PatchOperation] = []


class ListingsItemPutRequest(__BaseDictObject):
    """
    The request body schema for the putListingsItem operation.
    """

    def __init__(self, data):
        super().__init__(data)
        if "productType" in data:
            self.productType: str = self._get_value(str, "productType")
        else:
            self.productType: str = None
        if "requirements" in data:
            self.requirements: str = self._get_value(str, "requirements")
        else:
            self.requirements: str = None
        if "attributes" in data:
            self.attributes: dict = self._get_value(dict, "attributes")
        else:
            self.attributes: dict = None


class ListingsItemSubmissionResponse(__BaseDictObject):
    """
    Response containing the results of a submission to the Selling Partner API for Listings Items.
    """

    def __init__(self, data):
        super().__init__(data)
        if "sku" in data:
            self.sku: str = self._get_value(str, "sku")
        else:
            self.sku: str = None
        if "status" in data:
            self.status: str = self._get_value(str, "status")
        else:
            self.status: str = None
        if "submissionId" in data:
            self.submissionId: str = self._get_value(str, "submissionId")
        else:
            self.submissionId: str = None
        if "issues" in data:
            self.issues: _List[Issue] = [Issue(datum) for datum in data["issues"]]
        else:
            self.issues: _List[Issue] = []


class ListingsItems20200901Client(__BaseClient):
    def putListingsItem(
        self,
        data: ListingsItemPutRequest,
        sellerId: str,
        sku: str,
        marketplaceIds: _List[str],
        issueLocale: str = None,
    ):
        """
                Creates a new or fully-updates an existing listings item for a selling partner.
        **Note:** The parameters associated with this operation may contain special characters that must be encoded to successfully call the API. To avoid errors with SKUs when encoding URLs, refer to [URL Encoding](https://developer-docs.amazon.com/sp-api/docs/url-encoding).
        **Usage Plan:**
        | Rate (requests per second) | Burst |
        | ---- | ---- |
        | 5 | 10 |
        The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).
        """
        url = f"/listings/2020-09-01/items/{sellerId}/{sku}"
        params = {}
        if marketplaceIds is not None:
            params["marketplaceIds"] = ",".join(map(str, marketplaceIds))
        if issueLocale is not None:
            params["issueLocale"] = issueLocale
        response = self.request(
            path=url,
            method="PUT",
            params=params,
            data=data.data,
        )
        response_type = {
            200: ListingsItemSubmissionResponse,
            400: ErrorList,
            403: ErrorList,
            413: ErrorList,
            415: ErrorList,
            429: ErrorList,
            500: ErrorList,
            503: ErrorList,
        }.get(response.status_code, None)
        return None if response_type is None else response_type(self._get_response_json(response))

    def deleteListingsItem(
        self,
        sellerId: str,
        sku: str,
        marketplaceIds: _List[str],
        issueLocale: str = None,
    ):
        """
                Delete a listings item for a selling partner.
        **Note:** The parameters associated with this operation may contain special characters that must be encoded to successfully call the API. To avoid errors with SKUs when encoding URLs, refer to [URL Encoding](https://developer-docs.amazon.com/sp-api/docs/url-encoding).
        **Usage Plan:**
        | Rate (requests per second) | Burst |
        | ---- | ---- |
        | 5 | 10 |
        The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).
        """
        url = f"/listings/2020-09-01/items/{sellerId}/{sku}"
        params = {}
        if marketplaceIds is not None:
            params["marketplaceIds"] = ",".join(map(str, marketplaceIds))
        if issueLocale is not None:
            params["issueLocale"] = issueLocale
        response = self.request(
            path=url,
            method="DELETE",
            params=params,
        )
        response_type = {
            200: ListingsItemSubmissionResponse,
            400: ErrorList,
            403: ErrorList,
            413: ErrorList,
            415: ErrorList,
            429: ErrorList,
            500: ErrorList,
            503: ErrorList,
        }.get(response.status_code, None)
        return None if response_type is None else response_type(self._get_response_json(response))

    def patchListingsItem(
        self,
        data: ListingsItemPatchRequest,
        sellerId: str,
        sku: str,
        marketplaceIds: _List[str],
        issueLocale: str = None,
    ):
        """
                Partially update (patch) a listings item for a selling partner. Only top-level listings item attributes can be patched. Patching nested attributes is not supported.
        **Note:** The parameters associated with this operation may contain special characters that must be encoded to successfully call the API. To avoid errors with SKUs when encoding URLs, refer to [URL Encoding](https://developer-docs.amazon.com/sp-api/docs/url-encoding).
        **Usage Plan:**
        | Rate (requests per second) | Burst |
        | ---- | ---- |
        | 5 | 10 |
        The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).
        """
        url = f"/listings/2020-09-01/items/{sellerId}/{sku}"
        params = {}
        if marketplaceIds is not None:
            params["marketplaceIds"] = ",".join(map(str, marketplaceIds))
        if issueLocale is not None:
            params["issueLocale"] = issueLocale
        response = self.request(
            path=url,
            method="PATCH",
            params=params,
            data=data.data,
        )
        response_type = {
            200: ListingsItemSubmissionResponse,
            400: ErrorList,
            403: ErrorList,
            413: ErrorList,
            415: ErrorList,
            429: ErrorList,
            500: ErrorList,
            503: ErrorList,
        }.get(response.status_code, None)
        return None if response_type is None else response_type(self._get_response_json(response))
