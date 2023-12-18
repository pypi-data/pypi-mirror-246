from setuptools import setup, find_packages

setup(
    name='aitoolsAPI',  # Название вашей библиотеки
    version='0.2',  # Начальная версия
    packages=find_packages(),  # Автоматический поиск пакетов в вашем проекте
    install_requires=[
        'httpx',  # Зависимости, которые необходимы для работы вашей библиотеки
    ],
    # Дополнительные метаданные о пакете
    author='Opo',
    author_email='admin@opo.k.vu',
    description='A lightweight library that makes it easy to use Stable Diffusion XL and GPT.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/Master05710/aitoolsAPI',
    license='MIT',
)
