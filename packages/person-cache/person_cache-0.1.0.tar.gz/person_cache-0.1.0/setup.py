from setuptools import setup, find_packages

setup(
    name='person_cache',
    packages=['person_cache'],
    version='0.1.0',
    author="Tiago Ventura",
    author_email="tiago.barbano@gmail.com",
    description="Simple caching library for Python",
    install_requires=["aioredis>=2.0.1", "redis>=4.3.3"],
    keywords=['redis', 'aioredis', 'cache', 'Memory'],
    python_requires='>=3.8',
    scripts=['main.py'],
    # Outras informações como autor, descrição, etc.
)