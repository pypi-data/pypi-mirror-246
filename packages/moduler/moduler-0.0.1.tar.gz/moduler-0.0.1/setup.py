import codecs
import glob
import os.path
import re

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop

install_requires = [
    "torch>=1.9.0",
    "grpcio>=1.38.0",
]

this_folder = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(this_folder, "moduler/__init__.py"), encoding="utf-8") as init_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", init_file.read(), re.M)
    version_string = version_match.group(1)


class ProtoCompile(build_py):
    def run(self):
        import grpc_tools.protoc
        output_path = "moduler/proto"

        cli_args = [
            "grpc_tools.protoc",
            "--proto_path=moduler/proto",
            # Python output
            f"--python_out={output_path}",
            f"--grpc_python_out={output_path}",
            # Mypy output
            f"--mypy_out={output_path}",
            f"--mypy_grpc_out={output_path}"
        ] + glob.glob("moduler/proto/*.proto")

        code = grpc_tools.protoc.main(cli_args)
        if code:
            raise ValueError(f"{' '.join(cli_args)} finished with exit code {code}")
        # Make pb2 imports in generated scripts relative
        for script in glob.iglob(f"{output_path}/*.py"):
            with open(script, "r+") as file:
                code = file.read()
                file.seek(0)
                file.write(re.sub(r"\n(import .+_pb2.*)", "from . \\1", code))
                file.truncate()


class Develop(develop):
    def run(self):
        self.reinitialize_command("build_py", build_lib=this_folder)
        self.run_command("build_py")
        super().run()


setup(
    name="moduler",
    version=version_string,
    cmdclass={"build_py": ProtoCompile, "develop": Develop},
    description="",
    long_description="Decentralized deep learning in PyTorch. Built to train models on thousands of volunteers "
    "across the world.",
    author="Babs Technologies",
    author_email="",
    url="https://github.com/Babs-Technologies/module",
    packages=find_packages(exclude=["tests"]),
    package_data={"moduler": ["proto/*"]},
    include_package_data=True,
    license="MIT",
    setup_requires=["grpcio-tools", "mypy-protobuf"],
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="deep learning, machine learning, gpu, distributed computing, volunteer computing",
)
