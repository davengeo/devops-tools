import chevron

from ..common.config import Config

TEMPLATES = 'templates'


def simple_render(template: str, data: dict) -> str:
    return chevron.render(template=template, data=data)


class Templates(object):

    def __init__(self, config: Config) -> None:
        self.config: Config = config

    def render(self, template_name: str, data: dict) -> str:
        file_path = self.config.get_file_path(TEMPLATES, '{}.mustache'.format(template_name))
        template: str
        with open(file_path, mode='r') as f:
            template = f.read()
        return simple_render(template, data)
