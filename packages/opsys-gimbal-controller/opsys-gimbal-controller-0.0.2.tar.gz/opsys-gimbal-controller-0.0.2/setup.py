import setuptools
from pathlib import Path


def get_install_requirements():
    """
    Extract packages from requirements.txt file to list

    Returns:
        list: list of packages
    """
    fname = Path(__file__).parent / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets


setuptools.setup(name='opsys-gimbal-controller',
                 version='0.0.2',
                 description='python package for gimbal devices control',
                 url='https://bitbucket.org/opsys_tech/opsys-gimbal-controller/src/master/',
                 download_url='https://bitbucket.org/opsys_tech/opsys-gimbal-controller/src/master/',
                 author='dmitry.borovensky',
                 install_requires=get_install_requirements(),
                 author_email='dmitry.borovensky@opsys-tech.com',
                 packages=setuptools.find_packages(),
                 package_data={'opsys_gimbal_controller': ['newmark/*.dll', 'thorlabs/*.dll']},
                 zip_safe=False)