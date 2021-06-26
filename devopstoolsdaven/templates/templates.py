import chevron

from devopstoolsdaven.common.config import get_file_path

TEMPLATES = 'templates'


def simple_render(template: str, data: dict) -> str:
    return chevron.render(template=template, data=data)


class Templates(object):

    def __init__(self, templates_folder: str) -> None:
        self.__templates_folder: str = templates_folder

    def render(self, template_name: str, data: dict) -> str:
        file_path = get_file_path(self.__templates_folder, '{}.mustache'.format(template_name))
        template: str
        with open(file_path, mode='r') as f:
            template = f.read()
        return simple_render(template, data)
