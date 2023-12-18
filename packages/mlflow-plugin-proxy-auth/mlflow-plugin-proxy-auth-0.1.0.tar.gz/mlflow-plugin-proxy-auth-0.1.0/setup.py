from setuptools import find_packages, setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="mlflow-plugin-proxy-auth",
    version='0.1.0',
    author="Matúš Námešný",
    author_email="matus@namesny.com",
    description="Provides authentication to Mlflow server using Proxy-Authorization header.",
    url = "https://github.com/LordMathis/mlflow-plugin-proxy-auth",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["mlflow"],
    entry_points={
        "mlflow.request_auth_provider": "dummy-backend=mlflow_plugin_proxy_auth.proxy_auth_header_provider:ProxyAuthProvider",
    },
)
