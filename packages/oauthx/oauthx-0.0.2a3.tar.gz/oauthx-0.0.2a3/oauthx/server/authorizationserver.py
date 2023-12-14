# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
from typing import Any
import fastapi
from aiopki.ext.jose import OIDCToken

from oauthx.lib.params import Logger
from oauthx.lib.types import OIDCIssuerIdentifier
from oauthx.server.protocols import IAuthorizationServer
from oauthx.server.protocols import ISubject
from .params import ContentEncryptionKey
from .params import ObjectFactory
from .params import Storage
from .subjectresolver import SubjectResolver


class AuthorizationServer(IAuthorizationServer):
    __module__: str = 'oauthx.server'
    factory: ObjectFactory
    storage: Storage
    subjects: SubjectResolver

    def __init__(
        self,
        logger: Logger,
        storage: Storage,
        encryption_key: ContentEncryptionKey,
        factory: ObjectFactory,
        subjects: SubjectResolver = fastapi.Depends(SubjectResolver)
    ):
        self.encryption_key = encryption_key
        self.factory = factory
        self.logger = logger
        self.storage = storage
        self.subjects = subjects

    async def onboard_oidc(self, token: OIDCToken) -> tuple[ISubject, bool]:
        created = False
        issuer = OIDCIssuerIdentifier(token.iss)
        principals = [
            token.email if token.email_verified else None,
            token.phone_number if token.phone_number_verified else None,
            token.subject_id,
            token.preferred_username
        ]
        results = await self.subjects.resolve_principals(principals)
        if len(set([x.owner for x in results if x is not None])) > 1:
            self.logger.warning("OIDC ID Token resolved to multiple principals.")
            raise self.AmbiguousPrincipal
        if not any(results):
            created = True
            subject = await self.factory.subject()
            await subject.encrypt_keys(self.encryption_key)
            await self.storage.persist(subject)
        else:
            assert results[0] is not None
            principal = results[0]
            subject = await self.storage.get(principal.owner)
            if subject is None:
                self.logger.critical(
                    "Could not retrieve Subject with the given Principal "
                    "(kind: %s, mask: %s)",
                    principal.kind, principal.masked
                )
                raise self.OrphanedPrincipal
            self.logger.debug(
                "Returning Subject authenticated with OIDC "
                "(iss: %s, sub: %s)",
                token.iss, str(subject.get_primary_key())
            )

        # Retrieve the Subject because its keys may be encrypted at
        # this point.
        pk = subject.get_primary_key()
        subject = await self.storage.get(pk)
        if created:
            self.logger.info(
                "Registered subject from OpenID Connect "
                "(iss: %s, sub: %s)",
                token.iss, pk
            )

        assert subject is not None
        await subject.decrypt_keys(self.encryption_key)
        await self.register_principal(
            issuer=OIDCIssuerIdentifier(token.iss),
            subject=subject,
            value=token.subject_id,
            created=created,
            verified=True
        )
        if token.email:
            await self.register_principal(
                issuer=OIDCIssuerIdentifier(token.iss),
                subject=subject,
                value=token.email,
                created=created,
                verified=token.email_verified
            )
        if token.phone_number:
            await self.register_principal(
                issuer=issuer,
                subject=subject,
                value=token.email,
                created=created,
                verified=token.phone_number_verified
            )

        receipt = await self.factory.receipt(
            provider=token.iss,
            sub=int(subject.get_primary_key()), # type: ignore
        )
        async with receipt.transaction(subject, self.storage) as tx:
            tx.add('birthdate', token.gender, issuer='self')
            tx.add('gender', token.gender, issuer='self')
            tx.add('email', token.email,
             issuer='self' if not token.email_verified else issuer)
            tx.add('phone_number', token.phone_number,
             issuer='self' if not token.phone_number_verified else issuer)
            tx.add('name', token.name, issuer='self')
            tx.add('given_name', token.given_name, issuer='self')
            tx.add('middle_name', token.middle_name, issuer='self')
            tx.add('family_name', token.family_name, issuer='self')
            tx.add('nickname', token.nickname, issuer='self')

        return subject, created

    async def register_principal(
        self,
        *,
        issuer: OIDCIssuerIdentifier,
        subject: ISubject,
        value: Any,
        created: bool = False,
        verified: bool = False
    ) -> None:
        now = datetime.datetime.now(datetime.timezone.utc)
        new = await self.factory.principal(
            subject=subject,
            issuer=issuer,
            owner=subject.get_primary_key(), # type: ignore
            now=now,
            value=value,
            verified=verified
        )
        old = await self.storage.get(new.masked)
        if not old or not old.is_verified():
            await new.encrypt(subject)
            await self.storage.persist(new)