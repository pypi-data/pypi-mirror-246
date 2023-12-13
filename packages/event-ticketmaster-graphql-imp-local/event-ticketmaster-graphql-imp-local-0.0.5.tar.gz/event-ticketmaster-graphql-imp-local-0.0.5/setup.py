import setuptools
PACKAGE_NAME = "event-ticketmaster-graphql-imp-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.5',  # update only the minor version each time # https://pypi.org/project/<short-project-name-with-underscores>/ # noqa
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles event-ticketmaster-graphql-imp-local Python",  # noqa
    long_description="PyPI Package for Circles event-ticketmaster-graphql-imp-local Python",  # noqa
    long_description_content_type='text/markdown',
    # TODO: Please update the URL below
    url="https://github.com/circles",  # https://pypi.org/project/<project-name>/  # noqa
    # packages=setuptools.find_packages(),
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    # TODO: Update which packages to include with this package
    install_requires=[
        'PyMySQL>=1.0.2',
        'pytest>=7.4.0',
        'mysql-connector>=2.2.9',
        'logzio-python-handler>= 4.1.0',
        'user-context-remote>=0.0.17',
        'python-sdk-local>=0.0.27'
    ],
)
