# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import fastapi

from oauthx.lib.exceptions import InvalidRequest
from oauthx.server.params import CurrentSubject
from oauthx.server.params import ObjectFactory
from oauthx.server.params import PluginRunner
from oauthx.server.params import RequestSession
from oauthx.server.params import TokenIssuer
from oauthx.server.params import TokenSigner
from oauthx.server.request import Request
from oauthx.server.types import LoginRequired
from oauthx.server.types import InvalidResponseType
from oauthx.server.types import UnauthorizedClient
from ..baserequesthandler import BaseRequestHandler
from .params import Client
from .params import AuthorizationRequest
from .params import RedirectURI
from .params import ResponseMode
from .params import ResponseType
from .params import ResourceOwner
from .params import Scope
from .params import State


class AuthorizationRequestHandler(BaseRequestHandler):
    """Provides an interface for the resource owner to authorize a certain
    scope for a client, and redirect back to the clients' redirection
    endpoint.
    """
    __module__: str = 'oauthx.server.handlers'
    client: Client
    name: str = 'oauth2.authorize'
    path: str = '/authorize'
    redirect_uri: RedirectURI
    responses: dict[int | str, Any] = {
        400: {
            'description': (
                "Unrecoverable error that is not allowed to redirect"
            )
        }
    }
    response_class: type[fastapi.Response] = fastapi.responses.RedirectResponse
    response_description: str = "Redirect to the clients' redirection endpoint."
    response_type: ResponseType
    scope: Scope
    status_code: int = 302
    subject: CurrentSubject | None
    summary: str = "Authorization Endpoint"

    def setup(
        self,
        *,
        issuer: TokenIssuer,
        client: Client,
        redirect_uri: RedirectURI,
        subject: CurrentSubject,
        params: AuthorizationRequest,
        plugins: PluginRunner,
        owner: ResourceOwner,
        response_mode: ResponseMode,
        response_type: ResponseType,
        scope: Scope,
        session: RequestSession,
        signer: TokenSigner,
        state: State,
        factory: ObjectFactory,
        **_: Any
    ):
        self.client = client
        self.factory = factory
        self.issuer = issuer
        self.owner = owner
        self.params = params
        self.plugins = plugins
        self.redirect_uri = redirect_uri
        self.response_mode = response_mode
        self.response_type = response_type
        self.scope = scope
        self.session = session
        self.signer = signer
        self.state = state
        self.subject = subject

    async def handle(self, request: Request) -> fastapi.Response:
        if self.subject is None:
            raise LoginRequired(
                client=self.client,
                deny_url=await self.response_mode.deny()
            )
        if self.owner is None:
            raise NotImplementedError

        if not self.client.can_grant(self.response_mode.grants()):
            raise UnauthorizedClient

        if not self.state and self.client.requires_state():
            raise InvalidRequest(
                "The client requires the use of the state "
                "parameter."
            )

        # If the authorization request was not pushed, persist
        # the parameters.
        if self.params is None:
            self.params = await self.factory.request(
                client=self.client, # type: ignore
                request=self.request,
                redirect_uri=self.redirect_uri
            )
        await self.storage.persist(self.params)
        response = await self.plugins.validate_scope(
            client=self.client,
            request=self.params,
            scope=self.params.scope
        )
        if response is not None:
            return response
        assert self.params.id
        authorization = await self.factory.authorization(
            request=self.params,
            client_id=self.client.id,
            scope=self.scope,
            sub=self.subject.get_primary_key(), # type: ignore
            lifecycle='GRANTED',
        )
        await self.storage.persist(authorization)
        await self.storage.delete(self.params)
        return await self.response_mode.redirect(
            signer=self.signer,
            code=await self.issuer.authorization_code(
                signer=self.signer,
                client=self.client,
                owner=self.owner,
                authorization_id=authorization.id,
                sub=self.subject.get_primary_key(), # type: ignore
                redirect_uri=self.params.redirect_uri
            )
        )