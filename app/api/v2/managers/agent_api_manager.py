from app.api.v2.managers.base_api_manager import BaseApiManager


class AgentApiManager(BaseApiManager):
    def __init__(self, data_svc, file_svc):
        super().__init__(data_svc=data_svc, file_svc=file_svc)

    async def get_deploy_commands(self, ability_id: str):
        abilities = await self._data_svc.locate('abilities', {'ability_id': ability_id})

        raw_abilities = []
        for ability in abilities:
            for executor in ability.executors:
                variations = [{'description': v.description, 'command': v.raw_command} for v in executor.variations]
                raw_abilities.append({'platform': executor.platform, 'executor': executor.name,
                                      'description': ability.description, 'command': executor.command,
                                      'variations': variations})

        app_config = {
            k: v for k, v in self.get_config().items() if k.startswith('app.')
        } | {f'agents.{k}': v for k, v in self.get_config(name='agents').items()}

        return dict(abilities=raw_abilities, app_config=app_config)
