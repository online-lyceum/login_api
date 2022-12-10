from setuptools import setup, find_packages


install_requires = [
    'asyncpg',
    'pydantic',
    'fastapi',
    'uvicorn',
    'sqlalchemy[asyncio]',
    'gunicorn',
    'pyotp'
]

setup(
    name='login_api',
    version="0.0.1.dev1",
    description='Lyceum LoginAPI',
    platforms=['POSIX'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
        ]
    }
)
