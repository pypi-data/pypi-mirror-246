from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Sequence

from loguru import logger
from pdm.backend.base import Context


class PyFutureBuildHook:
    def __init__(self) -> None:
        self.target_str = os.environ.get("PYFUTURE_TARGET", None)

    @property
    def target(self) -> tuple[int, int]:
        if self.target_str is None:
            return sys.version_info[:2]
        else:
            return (int(self.target_str[2:3]), int(self.target_str[3:]))

    def hook_config(self, context: Context):
        return context.config.data.get("tool", {}).get("pdm", {}).get("build", {}).get("hooks", {}).get("pyfuture", {})

    def pdm_build_hook_enabled(self, context: Context):
        hook_config = self.hook_config(context)
        if self.target_str is None:
            self.target_str = hook_config.get("target", None)
        if context.target == "editable":
            if sys.version_info[:2] < (3, 12):
                raise RuntimeError("PyFuture cannot be installed by editable mode in Python < 3.12")
            elif self.target < (3, 12):
                # TODO: support editable
                # enable_editable = hook_config.get("enable_editable", True)
                # return context.target == "wheel" or (not enable_editable and context.target == "editable")
                logger.warning("Target config is ignored in editable mode")
                self.target_str = "py312"
        return context.target == "wheel"

    def pdm_build_initialize(self, context: Context) -> None:
        context.config.build_config["is-purelib"] = True
        if self.target_str is not None:
            context.builder.config_settings["--python-tag"] = self.target_str

    def pdm_build_update_files(self, context: Context, files: dict[str, Path]) -> None:
        try:
            from pyfuture.utils import transfer_file

            build_dir = context.ensure_build_dir()
            package_dir = Path(context.config.build_config.package_dir)
            includes = context.config.build_config.includes
            for include in includes:
                src_path = package_dir / include
                tgt_path = build_dir / include
                for src_file in src_path.glob("**/*.py"):
                    tgt_file = tgt_path / src_file.relative_to(src_path)
                    files[f"{tgt_file.relative_to(build_dir)}"] = tgt_file
                    transfer_file(src_file, tgt_file, target=self.target)
        except ImportError:
            logger.warning("PyFuture is not installed, skipping pyfuture build hook")
