# -*- coding: utf-8 -*-

import typing as T
import sys
import subprocess
import dataclasses
import shutil
from pathlib import Path


@dataclasses.dataclass
class Project:
    # fmt: off
    dir_project_root: T.Optional[Path] = dataclasses.field(default=None)
    python_version: T.Optional[str] = dataclasses.field(default=None)
    path_requirements_txt_or_pyproject_toml: T.Optional[Path] = dataclasses.field(default=None)
    # fmt: on

    def __post_init__(self):
        if self.dir_project_root is None:
            self.dir_project_root = Path.cwd()
        if self.path_requirements_txt_or_pyproject_toml is None:
            path_requirements = self.dir_project_root / "requirements.txt"
            path_pyproject = self.dir_project_root / "pyproject.toml"
            if path_requirements.exists():
                self.path_requirements_txt_or_pyproject_toml = path_requirements
            elif path_pyproject.exists():
                self.path_requirements_txt_or_pyproject_toml = path_pyproject
            else:
                raise RuntimeError(
                    f"Neither requirements.txt nor pyproject.toml exists in {self.dir_project_root}"
                )

    @property
    def dir_venv(self) -> Path:
        return self.dir_project_root.joinpath(".venv")

    @property
    def path_venv_bin(self) -> Path:
        return self.dir_venv / "bin"

    @property
    def path_venv_bin_python(self) -> Path:
        return self.path_venv_bin / "python"

    @property
    def path_venv_bin_pip(self) -> Path:
        return self.path_venv_bin / "pip"

    @property
    def path_caller_python(self):
        return Path(sys.executable)

    @property
    def path_caller_pip(self):
        return self.path_caller_python.parent / "pip"

    @property
    def path_caller_virtualenv(self):
        return self.path_caller_python.parent / "virtualenv"

    def install_caller_virtualenv(self):
        if self.path_caller_virtualenv.exists() is False:
            args = [f"{self.path_caller_pip}", "install", "virtualenv"]
            subprocess.run(args, check=True)

    @property
    def base_interpreter(self) -> str:
        if self.python_version is None:
            return sys.executable
        # example: 3.9
        elif self.python_version[0].isdigit():
            return f"python{self.python_version}"
        # example: python3.9
        elif self.python_version.startswith("python"):
            return self.python_version
        # example: /path/to/python/interpreter
        else:
            return str(self.python_version)

    def create_virtualenv(
        self,
        recreate: bool = False,
    ):
        print(f"🐍 Create virtualenv at {self.dir_venv}")
        self.install_caller_virtualenv()

        if self.dir_venv.exists():
            if recreate:
                shutil.rmtree(self.dir_venv, ignore_errors=True)
            else:
                print(f"  ✅ Virtualenv already exists")
                return
        args = [
            f"{self.path_caller_virtualenv}",
            "-p",
            f"{self.base_interpreter}",
            f"{self.dir_venv}",
        ]
        subprocess.run(args, check=True)
        print("  ✅ Done")

    def install_dependencies_in_virtualenv(self):
        print(f"💾 Install necessary dependencies in virtualenv")
        if self.path_requirements_txt_or_pyproject_toml.name == "requirements.txt":
            args = [
                f"{self.path_venv_bin_pip}",
                "install",
                "-q",
                "--disable-pip-version-check",
                "-r",
                f"{self.path_requirements_txt_or_pyproject_toml}",
            ]
            subprocess.run(args, check=True)
            print("  ✅ Done")
        elif self.path_requirements_txt_or_pyproject_toml.name == "pyproject.toml":
            raise NotImplementedError

    def bootstrap(
        self,
        recreate_venv: bool = False,
    ):
        """
        Bootstrap.
        """
        self.create_virtualenv(recreate=recreate_venv)
        self.install_dependencies_in_virtualenv()
