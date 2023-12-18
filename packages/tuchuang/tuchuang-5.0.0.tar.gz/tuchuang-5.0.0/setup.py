from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tuchuang',
    version='5.0.0',
    description='一个免费而简单图床(喜欢就关注:python学霸微信公众号)',
    author='Python学霸',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author_email='python@xueba.com',
    packages=['tuchuang'],
    install_requires=['requests'],
)