from setuptools import setup, find_packages
import subprocess

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

def request_gdal_version():
    try:
        r = subprocess.run(['gdal-config', '--version'], stdout=subprocess.PIPE )
        version = r.stdout.decode('utf-8').strip('\n')
        print("GDAL %s detected on the system, using 'gdal=%s'" % (version, version))
        return version
    except Exception as ex:  # pylint: disable=broad-except
        return '3.2.2'

setup(
    name="majamask",
    version = "1.0.0",
    description = "Creates a simplified rastermask from CLM and MG2 masks",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    url="https://gitlab.orfeo-toolbox.org/maja/maja",
    author="CS Group France",
    author_email="axelle.pochet@csgroup.eu",
    license="Apache Version 2",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux"
    ],
    packages=["majamask"],
    install_requires=["gdal=="+request_gdal_version(), 'numba==0.56.4', 'Pillow'],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'rastermask = majamask.rastermask:main'
        ]
    },
)