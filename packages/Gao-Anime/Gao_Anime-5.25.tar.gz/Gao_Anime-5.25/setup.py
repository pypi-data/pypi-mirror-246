#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.  1》》》
# 写入自己的内容 start——1
NAME = 'Gao_Anime'  # 为项目取名，这个名字就是 pip install xxx的xxx
DESCRIPTION = 'AI Head'
URL = 'https://github.com/CuteCar384/Gao_Anime'
EMAIL = '1664625666@qq.com'
AUTHOR = 'Huang'
REQUIRES_PYTHON = '>=3.8'
VERSION = '5.25'  # 为项目指定目前的版本号
# end——1
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# What packages are required for this module to be executed?
REQUIRED = [
    # 'requests', 'maya', 'records',
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# 写入自己的内容 start——2
# Where the magic happens:
setup(
    name="Gao_Anime",  # 和前边的保持一致
    version=about['__version__'],
    description="AI Head",
    long_description=open('README.md', 'r', encoding='utf-8').read(),  # 默认是readme文件。
    long_description_content_type='text/markdown',
    author="Huang",
    author_email="1664625666@qq.com",
    python_requires=">=3.8",
    url="https://github.com/CuteCar384/Gao_Anime",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),

    # end——2
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    # REQUIRED 是项目依赖的库
    install_requires=[
        'aiofiles==23.2.1',
        'aiohttp==3.9.1',
        'aiosignal==1.3.1',
        'altair==5.2.0',
        'annotated-types==0.6.0',
        'anyio==3.7.1',
        'argon2-cffi==23.1.0',
        'argon2-cffi-bindings==21.2.0',
        'arrow==1.2.3',
        'astor==0.8.1',
        'async-lru==2.0.4',
        'async-timeout==4.0.3',
        'attrs==23.1.0',
        'Babel==2.12.1',
        'bce-python-sdk==0.8.97',
        'beautifulsoup4==4.12.2',
        'bleach==6.0.0',
        'blinker==1.7.0',
        'certifi==2023.11.17',
        'cffi==1.15.1',
        'charset-normalizer==3.3.2',
        'click==8.1.7',
        'colorama==0.4.6',
        'colorlog==6.8.0',
        'contourpy==1.1.0',
        'cycler==0.11.0',
        'd2l==1.0.3',
        'datasets==2.15.0',
        'decorator==5.1.1',
        'defusedxml==0.7.1',
        'dill==0.3.4',
        'easydict==1.11',
        'exceptiongroup==1.1.3',
        'fastapi==0.105.0',
        'ffmpy==0.3.1',
        'filelock==3.13.1',
        'Flask==3.0.0',
        'flask-babel==4.0.0',
        'fonttools==4.42.1',
        'fqdn==1.5.1',
        'frozenlist==1.4.0',
        'fsspec==2023.10.0',
        'future==0.18.3',
        'Gao-Anime==5.24',
        'gradio==4.9.0',
        'gradio_client==0.7.2',
        'h11==0.14.0',
        'httpcore==1.0.2',
        'httpx==0.25.2',
        'huggingface-hub==0.19.4',
        'idna==3.6',
        'importlib-metadata==7.0.0',
        'importlib-resources==6.0.1',
        'ipywidgets==8.1.0',
        'isoduration==20.11.0',
        'itsdangerous==2.1.2',
        'jieba==0.42.1',
        'Jinja2==3.1.2',
        'joblib==1.3.2',
        'jsonpointer==2.4',
        'jsonschema==4.19.0',
        'jsonschema-specifications==2023.7.1',
        'jupyter==1.0.0',
        'jupyter-console==6.6.3',
        'jupyter-events==0.7.0',
        'jupyter-lsp==2.2.0',
        'jupyter_server==2.7.3',
        'jupyter_server_terminals==0.4.4',
        'jupyterlab==4.0.5',
        'jupyterlab-pygments==0.2.2',
        'jupyterlab-widgets==3.0.8',
        'jupyterlab_server==2.25.0',
        'kiwisolver==1.4.5',
        'markdown-it-py==3.0.0',
        'MarkupSafe==2.1.3',
        'matplotlib==3.7.4',
        'mdurl==0.1.2',
        'mistune==3.0.1',
        'multidict==6.0.4',
        'multiprocess==0.70.12.2',
        'nbclient==0.8.0',
        'nbconvert==7.8.0',
        'nbformat==5.9.2',
        'notebook==7.0.3',
        'notebook_shim==0.2.3',
        'numpy==1.24.4',
        'onnx==1.15.0',
        'opencv-python==4.8.1.78',
        'opt-einsum==3.3.0',
        'orjson==3.9.10',
        'packaging==23.2',
        'paddle2onnx==1.0.6',
        'paddlefsl==1.1.0',
        'paddlehub==2.4.0',
        'paddlenlp==2.6.1',
        'paddlepaddle==2.5.2',
        'pandas==2.0.3',
        'Pillow==10.1.0',
        'pkgutil_resolve_name==1.3.10',
        'protobuf==3.20.2',
        'psutil==5.9.6',
        'pyarrow==14.0.1',
        'pyarrow-hotfix==0.6',
        'pycryptodome==3.19.0',
        'pydantic==2.5.2',
        'pydantic_core==2.14.5',
        'pydub==0.25.1',
        'Pygments==2.17.2',
        'pyparsing==3.1.1',
        'python-dateutil==2.8.2',
        'python-multipart==0.0.6',
        'pytz==2023.3.post1',
        'PyYAML==6.0.1',
        'pyzmq==25.1.2',
        'qtconsole==5.4.4',
        'rarfile==4.1',
        'referencing==0.30.2',
        'requests==2.31.0',
        'rich==13.7.0',
        'rpds-py==0.13.2',
        'safetensors==0.4.1',
        'scikit-learn==1.3.2',
        'scipy==1.10.1',
        'semantic-version==2.10.0',
        'sentencepiece==0.1.99',
        'seqeval==1.2.2',
        'shellingham==1.5.4',
        'six==1.16.0',
        'sniffio==1.3.0',
        'starlette==0.27.0',
        'terminado==0.17.1',
        'threadpoolctl==3.2.0',
        'tomlkit==0.12.0',
        'toolz==0.12.0',
        'tqdm==4.66.1',
        'typer==0.9.0',
        'typing_extensions==4.9.0',
        'tzdata==2023.3',
        'urllib3==2.1.0',
        'uvicorn==0.24.0.post1',
        'visualdl==2.5.3',
        'websockets==11.0.3',
        'Werkzeug==3.0.1',
        'xxhash==3.4.1',
        'yarl==1.9.4',
        'zipp==3.17.0',
    ],

extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
