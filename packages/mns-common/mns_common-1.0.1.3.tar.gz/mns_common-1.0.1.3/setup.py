from setuptools import setup

setup(
    name='mns_common',
    version='1.0.1.3',
    packages=["mns_common", "mns_common.api", "mns_common.db", 'mns_common.utils'],
    install_requires=[],  # 如果有依赖项，可以在这里列出
)
