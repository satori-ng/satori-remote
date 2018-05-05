from setuptools import setup

import satoriremote as setupmod

setup(
    name=setupmod.__name__,
    description=setupmod.__desc__,
    version=setupmod.__version__,

    author="Satori-NG org",
    author_email=setupmod.__email__,

    packages=["satoriremote"],

    # entry_points={
    #     "console_scripts": [
    #         "hexwordify=hexwordify.__main__:main",
    #     ],
    # },
)
