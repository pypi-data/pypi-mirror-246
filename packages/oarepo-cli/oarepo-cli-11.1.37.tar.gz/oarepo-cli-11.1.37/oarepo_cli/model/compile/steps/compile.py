import venv
from pathlib import Path

import yaml

from oarepo_cli.model.utils import ModelWizardStep
from oarepo_cli.package_versions import OAREPO_MODEL_BUILDER_VERSION
from oarepo_cli.utils import pip_install, run_cmdline
from oarepo_cli.wizard import WizardStep


class CompileWizardStep(ModelWizardStep, WizardStep):
    def after_run(self):
        if self.data.running_in_docker:
            venv_dir = Path("/tmp/oarepo-model-builder")
        else:
            venv_dir = (
                self.data.project_dir
                / ".venv"
                / f"oarepo-model-builder-{self.model_name}"
            )
        print("model builder venv dir", venv_dir)
        venv_dir = venv_dir.absolute()
        if not venv_dir.exists():
            venv_args = [str(venv_dir)]
            if self.data.running_in_docker:
                venv_args.append("--system-site-packages")
            venv.main(venv_args)

        run_cmdline(
            venv_dir / "bin" / "pip",
            "list",
            cwd=self.model_dir,
        )

        pip_install(
            venv_dir / "bin" / "pip",
            "OAREPO_MODEL_BUILDER_VERSION",
            f"oarepo-model-builder{OAREPO_MODEL_BUILDER_VERSION}",
            "https://github.com/oarepo/oarepo-model-builder",
        )

        with open(self.model_dir / "model.yaml") as f:
            model_data = yaml.safe_load(f)

        # install plugins from model.yaml
        self._install_plugins_from_model(model_data, venv_dir)

        # install plugins from included files
        uses = model_data.get("use") or []
        if not isinstance(uses, list):
            uses = [uses]

        for use in uses:
            if not use.startswith("."):
                # can not currently find plugins in uses
                # that are registered as entrypoints
                continue
            with open(self.model_dir.joinpath(use)) as f:
                used_data = yaml.safe_load(f)
                self._install_plugins_from_model(used_data, venv_dir)

        run_cmdline(
            venv_dir / "bin" / "oarepo-compile-model",
            "-vvv",
            "model.yaml",
            cwd=self.model_dir,
        )

    def _install_plugins_from_model(self, model_data, venv_dir):
        plugins = model_data.get("plugins", {}).get("packages", [])
        for package in plugins:
            run_cmdline(
                venv_dir / "bin" / "pip",
                "install",
                package,
                cwd=self.model_dir,
            )

    def should_run(self):
        # always run as there is an optional step for merge/overwrite changes
        return True
