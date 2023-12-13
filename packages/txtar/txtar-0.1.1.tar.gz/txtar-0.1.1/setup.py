# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['txtar']

package_data = \
{'': ['*']}

install_requires = \
['pyfakefs>=5.3.2,<6.0.0']

setup_kwargs = {
    'name': 'txtar',
    'version': '0.1.1',
    'description': "Port of golang's txtar, a trivial tar-like format for unit tests",
    'long_description': '# txtar\n\n`txtar` is a Python reimplementation of Go\'s txtar format, a tool for bundling and managing multiple text files in a single archive.\n\n## Features\n\n- Parse `txtar` formatted text into structured data.\n- Serialize structured data back into `txtar` format.\n- Unpack `txtar` archives into the file system.\n\n\n## Usage\n\n### In unit tests\n\n```python\nfrom pathlib import Path\nimport os\n\ndef test_my_function():\n    # Define the txtar structure for sysfs-like files\n    txtar_content = """\n-- sys/class/thermal/thermal_zone0/temp --\n55000\n-- sys/class/power_supply/BAT0/capacity --\n45\n-- sys/block/sda/size --\n1024000\n"""\n\n    with MockFS.from_string(txtar_content):\n        assert os.path.exists("/sys/class/thermal/thermal_zone0/temp")\n        assert os.path.exists("/sys/class/power_supply/BAT0/capacity")\n        assert os.path.exists("/sys/block/sda/size")\n\n        assert Path("/sys/block/sda/size").exists()\n```\n\n### Reading a file\n```python\nfrom txtar import TxTar\n\ncontent = "..."  # txtar formatted string\narchive = TxTar.parse(content)\n```\n\n### Serializing to txtar Format\n\n```python\nfrom txtar import TxTar, File\n\narchive = TxTar(\n    comments=["Example txtar archive"],\n    files=[File(name="example.txt", lines=["Hello", "World"])]\n)\ncontent = archive.serialize()\n```\n\n### Unpacking an Archive\n\n```python\nfrom pathlib import Path\nfrom txtar import TxTar\n\narchive = TxTar.parse("...")\narchive.unpack_in(Path("/path/to/unpack"))\n```\n\n## Development\n\n * Install dependencies: `poetry install`\n * Run tests with `pytest`.\n\n## Releasing\n\n```\npoetry publish --build --username __token__ --password $PYPI_PASSWORD\n```\n',
    'author': 'david',
    'author_email': 'davidventura27@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/davidventura/txtar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
