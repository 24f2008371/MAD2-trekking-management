import os
from jinja2 import Environment, FileSystemLoader

def format_report(template_name, data):
    template_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    return template.render(data)
