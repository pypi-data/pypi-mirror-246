from setuptools import setup

setup(
    name='mns-common',
    version='1.0.1.1',
    packages=["mns-common", "mns-common.api", "mns-common.db", 'mns-common.utils'],
    install_requires=[],  # 如果有依赖项，可以在这里列出
)
