import setuptools
from pathlib import Path

setuptools.setup(
    name='pybullet_workshop_23',
    version='0.2.0',
    description="A OpenAI Gym Env for pybullet and vision",
    long_description=Path("Readme.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="pybullet_workshop_23*"),
    install_requires=['gym']
)