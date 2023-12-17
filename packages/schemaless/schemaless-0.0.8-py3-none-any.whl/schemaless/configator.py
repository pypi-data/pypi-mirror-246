import typing
import schemaless.domain
import schemaless.webhook
import schemaless.bases
import schemaless.http_client
import schemaless.config


class Configator:
    def __init__(
        self,
        http_client: typing.Optional[schemaless.bases.BaseHTTP] = None,
        domain_client: typing.Optional[schemaless.domain.Domain] = None,
        webhook_client: typing.Optional[schemaless.webhook.Webhook] = None,
        domain_list: typing.Optional[
            typing.List[schemaless.domain.CreateDomainBody]
        ] = None,
        webhook_list: typing.Optional[
            typing.List[schemaless.webhook.RegisterWebhookBody]
        ] = None,
        override: bool = False,
    ):
        self._http_client = http_client
        self._domain_client = domain_client
        self._webhook_client = webhook_client
        self._domain_list = domain_list or []
        self._webhook_list = webhook_list or []
        self._override = override

    @classmethod
    def from_config(cls, config: schemaless.config.Config) -> "Configator":
        return cls(
            http_client=schemaless.http_client.HTTP.from_config(config),
            domain_client=schemaless.domain.Domain.from_config(config),
            webhook_client=schemaless.webhook.Webhook.from_config(config),
        )

    def add_domain(self, domain: schemaless.domain.CreateDomainBody) -> "Configator":
        self._domain_list.append(domain)
        return self

    def add_webhook(
        self, webhook: schemaless.webhook.RegisterWebhookBody
    ) -> "Configator":
        self._webhook_list.append(webhook)
        return self

    def set_override(self, override: bool) -> "Configator":
        self._override = override
        return self

    async def commit(self):
        for domain in self._domain_list:
            await self._domain_client.create(domain)

        for webhook in self._webhook_list:
            await self._webhook_client.register(webhook)
