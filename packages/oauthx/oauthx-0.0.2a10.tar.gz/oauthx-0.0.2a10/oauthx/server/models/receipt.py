# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import contextlib
import datetime
from typing import Any
from typing import Literal

import pydantic

from oauthx.lib.protocols import IStorage
from oauthx.lib.types import OIDCIssuerIdentifier
from oauthx.server.protocols import ISubject
from oauthx.server.types import ClaimSetKey
from .claim import Claim


class Receipt(pydantic.BaseModel):
    id: int
    obtained: datetime.datetime
    processed: set[str] = set()
    provider: OIDCIssuerIdentifier
    purpose: Literal['IDENTIFY', 'INVITE', 'LOGIN', 'VERIFY_ACCOUNT']
    received: set[str]
    sub: int

    @property
    def claims(self) -> list[Claim]:
        return self._claims
    
    @property
    def claimset_id(self) -> ClaimSetKey:
        return ClaimSetKey(self.provider, self.sub)

    _claims: list[Claim] = pydantic.PrivateAttr(default_factory=list)
    _futures: list[asyncio.Future[Claim]] = pydantic.PrivateAttr(default_factory=list)
    _storage: IStorage | None = pydantic.PrivateAttr(default=None)
    _subject: ISubject | None = pydantic.PrivateAttr(default=None)

    @contextlib.asynccontextmanager
    async def transaction(self, subject: ISubject, storage: IStorage):
        if self._claims:
            raise ValueError("Transaction is already committed.")
        self._subject = subject
        self._storage = storage
        try:
            yield self
            self._claims = await asyncio.gather(*self._futures)
            self._futures = []
            await self._storage.persist(self)
        finally:
            self._storage = None

    def add(
        self,
        kind: Any,
        value: Any,
        *,
        issuer: Literal['self'] | OIDCIssuerIdentifier | None = None,
        ial: int = 0
    ) -> Claim | None:
        """Add a new claim to the :class:`Receipt`."""
        if value is None:
            return
        if kind not in self.received:
            raise ValueError(
                f"Claim '{kind}' is not registered as obtained with this "
                "receipt."
            )
        self.processed.add(kind)
        coro = self._create_claim(
            kind=kind,
            value=value,
            issuer=issuer,
            ial=ial
        )
        self._futures.append(asyncio.ensure_future(coro))

    async def _create_claim(self, kind: str, value: Any, **kwargs: Any) -> Claim:
        assert self._storage is not None
        assert self._subject is not None
        claim = Claim.model_validate({
            **kwargs,
            'kind': kind,
            'id': await self._storage.allocate_identifier(Claim),
            'obtained': self.obtained,
            'provider': self.provider,
            'receipt_id': self.id,
            'sub': self.sub,
            'value': value
        })
        await claim.mask(self._subject.get_masking_key())
        assert claim.is_masked()
        await claim.encrypt(self._subject)
        return claim