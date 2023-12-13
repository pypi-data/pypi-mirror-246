from setuptools import setup, find_packages

setup(
    name='person_cache',
    packages=['person_cache'],
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    version='1.0.0',
    url="https://github.com/tiagoBarbano/person_cache",
    author="Tiago Ventura",
    author_email="tiago.barbano@gmail.com",
    description="Simple caching library for Python",
    install_requires=["aioredis>=2.0.1", "redis>=4.3.3"],
    keywords=['redis', 'aioredis', 'cache', 'Memory'],
    python_requires='>=3.8',
    scripts=['person_cache/main.py'],
    # Outras informações como autor, descrição, etc.
)