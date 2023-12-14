# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# --------------------------------------------------------------------------


from time import sleep
from azure.identity import DefaultAzureCredential
from .api import SecurityCopilotAPIClient



_ENVPROD = 'prod'
_ENVDEV  = 'dev'

_ENDPOINTS = {
    _ENVDEV : 'https://api.medeina-dev.defender.microsoft.com',
    _ENVPROD : 'https://api.securitycopilot.microsoft.com',
}
_SCOPES = {
    _ENVDEV : 'https://api.medeina-dev.defender.microsoft.com/.default',
    _ENVPROD : 'https://api.securitycopilot.microsoft.com/.default',
}
_SOURCE = 'api.python'
_CONTEXT = {
    'apiclient': None,
    'cred': None,
    'env': _ENVPROD,
    'session': None,
    'tenant_id': None,
    'initialized': False,
    'session': None,
}


def init(interactive_auth:bool = True, tenant_id:str = None, dev:bool = False, **apikwargs):
    """Initializes the Security Copilot client, optionally setting params that apply to subsequent interactions.

    :keyword bool interactive_auth: Whether to enable browser-based interactive login. Defaults to True.
    :keyword str tenant_id: Optional tenant ID for token requests. Recommended if your user account has
        access to more than one tenant.
    :keyword bool dev: Whether to point to the development environment (defaults to False).
    :raises SecurityCopilotClientError: if the package is already initiated
    """
    if _CONTEXT['initialized']:
        raise SecurityCopilotClientError('Package is already initialized')
    _CONTEXT['cred'] = DefaultAzureCredential(
        exclude_interactive_browser_credential = not interactive_auth
    )
    _CONTEXT['tenant_id'] = tenant_id
    if dev:
        _CONTEXT['env'] = _ENVDEV
    _CONTEXT['apiclient'] = SecurityCopilotAPIClient(
        _CONTEXT['cred'],
        _ENDPOINTS[_CONTEXT['env']],
        **apikwargs
    )
    _CONTEXT['initialized'] = True

def submit_prompt(prompt:str) -> 'Session': 
    """Submit a prompt to the SecurityCopilot API."""
    _ensure_init()
    _ensure_session()
    prompt = _CONTEXT['session'].submit_prompt(prompt, source=_SOURCE).evaluate()
    return _CONTEXT['session']

def run_skill(skillname:str, params={}) -> 'Session': 
    """Submit a skill type prompt to the SecurityCopilot API."""
    _ensure_init()
    _ensure_session()
    prompt = _CONTEXT['session'].run_skill(skillname, params, source=_SOURCE).evaluate()
    return _CONTEXT['session']

def get_session() -> 'Session':
    return _CONTEXT['session']

def get_api() -> SecurityCopilotAPIClient:
    """Get the currently configured SecurityCopilot API client."""
    _ensure_init()
    return _CONTEXT['apiclient']

def _ensure_init():
    if not _CONTEXT['initialized']:
        raise SecurityCopilotClientError('Package is not yet initilized; run securitycopilot.init() first to begin')

def _ensure_session():
    from ._model import Session
    if _CONTEXT['session'] is None:
        _CONTEXT['session'] = Session()

def wait_for_response(sleeptime=3):
    while _CONTEXT['session'].is_prompt_pending:
        sleep(sleeptime)
        updates = _CONTEXT['session'].refresh()
        if updates is None:
            print ('Working...')
        else:
            print(_CONTEXT['session'].most_recent_prompt.last_completed_eval.result['content'])


class SecurityCopilotClientError(Exception):
    pass



from ._model import Session, Prompt, Evaluation
