'''
from jinja2 import Environment, FileSystemLoader
import yaml


env = Environment(loader=FileSystemLoader("."))# создание окружение для работы с шаблоном 
templ = env.get_template("configtxt/cfg_template.txt")# подставляем шаблон в окружение

liverpool = {"id": "11", "name": "Liverpool", "int": "Gi1/0/17", "ip": "10.1.1.10"}# значения
print(templ.render(liverpool))

# подсталяем переменные в шаблон и генерируем для каждого отдельный файл
from jinja2 import Environment, FileSystemLoader
import yaml

env = Environment(loader=FileSystemLoader('.') trim_blocks=True, lstrip_blocks=True)
template = env.get_template('configtxt/router_template.txt')

with open('configyaml/routers_info.yaml') as f:
    routers = yaml.safe_load(f)

for router in routers:
    r1_conf = router['name']+'_r1.txt'
    with open(r1_conf, 'w') as f:
        f.write(template.render(router))
 '''

