from madtornado4.core import fs, VERSION

from setuptools import setup

with open("requirements.txt", "r", encoding="utf-8") as fp:
    install_requires = list(map(lambda x: x.strip("\n"), fp.readlines()))

setup(
    name="madtornado4",
    python_requires=">=3.5",
    version=VERSION,
    author="SystemLight",
    author_email="1466335092@qq.com",
    maintainer="SystemLight",
    maintainer_email="1466335092@qq.com",
    url="https://github.com/SystemLight/madtornado4",
    license="MIT",
    description="Madtornado is a tool for generating Tornado projects for MVC.【生成tornado MVC项目模板 CLI脚手架(scaffolding)】",
    long_description=fs.read("README.md"),
    long_description_content_type='text/markdown',
    download_url="https://github.com/SystemLight/madtornado4/releases",
    install_requires=install_requires,
    platforms=["Windows", "Linux"],
    keywords=[
        "tornado", "web", "http_server", "mt", "Mad_tornado", "madtornado",
        "Tornado project template", "python3", "mvc", "mad", "generate the Tornado project",
        "tornado cli", "tornado mvc", "tornado脚手架", "生成tornado项目"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    py_modules=["mad"],
    scripts=["mad.py"],
    entry_points={
        "console_scripts": [
            "mad = mad:main"
        ]
    }
)
