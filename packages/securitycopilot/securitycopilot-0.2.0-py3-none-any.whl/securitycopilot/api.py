# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------


from azure.core.credentials import TokenCredential
from azure.core.pipeline import Pipeline
from azure.core.rest import HttpRequest, HttpResponse
from azure.core.pipeline.transport import RequestsTransport
from azure.core.pipeline.policies import (
    UserAgentPolicy,
    HeadersPolicy,
    RetryPolicy,
    RedirectPolicy,
    BearerTokenCredentialPolicy,
    ContentDecodePolicy,
    NetworkTraceLoggingPolicy,
    ProxyPolicy
)



class SecurityCopilotAPIClient:
    """
    Client for the SecurityCopilot API. 


    Ref: https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/core/azure-core/CLIENT_LIBRARY_DEVELOPER.md
    """

    def __init__(self, credential: TokenCredential, baseurl, **kwargs):
        scopes = baseurl + '/.default'
        transport = kwargs.get('transport', RequestsTransport(**kwargs))
        policies = [
            kwargs.get('user_agent_policy', UserAgentPolicy("securitycopilotpythonapi", user_agent_use_env=True, **kwargs)),
            kwargs.get('headers_policy', HeadersPolicy( **kwargs)),
            kwargs.get('authentication_policy', BearerTokenCredentialPolicy(credential, scopes, **kwargs)),
            ContentDecodePolicy(),
            kwargs.get('proxy_policy', ProxyPolicy(**kwargs)),
            kwargs.get('redirect_policy', RedirectPolicy(**kwargs)),
            kwargs.get('retry_policy', RetryPolicy(**kwargs)),
            kwargs.get('logging_policy', NetworkTraceLoggingPolicy(**kwargs)),
        ]
        self._pipeline = Pipeline(transport, policies=policies)
        self._baseurl = baseurl
    
    def _run_request(self, method, endpoint, params={}, **kwargs) -> HttpResponse:
        self._http_request = HttpRequest(
            method, 
            '/'.join((self._baseurl, endpoint)),
            params = params,
            **kwargs)
        self._pipeline_response = self._pipeline.run(self._http_request, **kwargs)
        return self._pipeline_response.http_response
    
    def _GET(self, endpoint, params={}, **kwargs) -> HttpResponse:
        return self._run_request('GET', endpoint, params, **kwargs)

    def _POST(self, endpoint, params={}, json={}, **kwargs) -> HttpResponse:
        return self._run_request('POST', endpoint, params, json=json, **kwargs)