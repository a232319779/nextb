# -*- coding: utf-8 -*-
# @Time    :   2021/08/18 18:48:13
# @Author  :   ddvv
# @公众号   :   NextB
# @File    :   setup.py
# @Software:   Visual Studio Code
# @Desc    :   None


from setuptools import setup, find_packages

depends = [
]

setup(
    name="nextb",
    version="1.0.1",
    packages=find_packages(exclude=[]),

    zip_safe=False,

    entry_points={
        "console_scripts": [
            "nextb-base-data = nextb.tools.show_base_data:run",
        ],
    },

    install_requires=depends,

    dependency_links=[
    ],

    include_package_data=True,

    license="ddvv",

    author="ddvv",
    author_email="dadavivi512@gmail.com",
    description="nextb",
)