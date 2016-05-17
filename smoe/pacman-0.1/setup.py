from setuptools import setup, find_packages

setup(
    name='pacman',
    version='0.1',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    dependency_links=[],
    package_data={'pac': ['layouts/*.lay',
    'test_cases/CONFIG',
    'test_cases/q1/*',
    'test_cases/q2/*',
    'test_cases/q3/*',
    'test_cases/q4/*',
    'test_cases/q5/*',
    'test_cases/q6/*',
    'test_cases/q7/*',
    'test_cases/q8/*',
    'test_cases/extra/*',
    ]}
)
