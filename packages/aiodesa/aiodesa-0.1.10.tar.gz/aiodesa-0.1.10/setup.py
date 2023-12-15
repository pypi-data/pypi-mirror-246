# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiodesa', 'aiodesa.utils', 'aiodesa.utils.tables', 'aiodesa.utils.types']

package_data = \
{'': ['*']}

install_requires = \
['aiosqlite>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'aiodesa',
    'version': '0.1.10',
    'description': '',
    'long_description': '# Asyncio Dead Easy Sql API\n\n## Are you tired of re-writing SQLite DB\'s for your projects? Me too. AIODesa makes standing up simple, usable applications extremely easy and effective.\n\n### AIODesa offers a straightforward and 100% Python interface for managing asynchronous data access. By leveraging Python\'s built-ins and standard library, it seamlessly wraps around AioSqlite, providing a hassle-free experience. With AIODesa, you can define, generate, and commit data effortlessly, thanks to shared objects for tables and records.\n\nAIODesa aims to make defining SQL tables and records easy by utilizing dataclasses to define structure of both tables and records. No more re-writing schemas.\n\n## AioDesa\n\n![AIODesa](https://github.com/sockheadrps/AIODesa/blob/main/AIODesaEx.png?raw=true)\n\n## AIOSqlite\n\n![AIOSqlite](https://github.com/sockheadrps/AIODesa/blob/main/AIOSqliteEx.png?raw=true)\n\n# Usage\n\n__Install via pip__\n```\npip install aiodesa\n```\n\n<br>\n\n# Development:\n\nEnsure poetry is installed:\n\n```\npip install poetry\n```\n\nInstall project using poetry\n\n```\npoetry add git+https://github.com/sockheadrps/AIODesa.git\npoetry install\n```\n\ncreate a python file for using AIODesa and activate poetry virtual env to run it\n\n```\npoetry shell\npoetry run python main.py\n```\n\nSample API usage:\n\n```\nfrom aiodesa import Db\nimport asyncio\nfrom dataclasses import dataclass\nfrom aiodesa.utils.tables import ForeignKey, UniqueKey, PrimaryKey, set_key\n\n\nasync def main():\n\t# Define structure for both tables and records\n\t# Easily define key types\n\t@dataclass\n\t@set_key(PrimaryKey("username"), UniqueKey("id"), ForeignKey("username", "anothertable"))\n\tclass UserEcon:\n\t\tusername: str\n\t\tcredits: int | None = None\n\t\tpoints: int | None = None\n\t\tid: str | None = None\n\t\ttable_name: str = "user_economy"\n\n\n\tasync with Db("database.sqlite3") as db:\n\t\t# Create table from UserEcon class\n\t\tawait db.read_table_schemas(UserEcon)\n\n\t\t# Insert a record\n\t\trecord = db.insert(UserEcon.table_name)\n\t\tawait record(\'sockheadrps\', id="fffff")\n\n\t\t# Update a record\n\t\trecord = db.update(UserEcon.table_name, column_identifier="username")\n\t\tawait record(\'sockheadrps\', points=2330, id="1234")\n\t\t\n\nasyncio.run(main())\n\n```\n',
    'author': 'sockheadrps',
    'author_email': 'r.p.skiles@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
