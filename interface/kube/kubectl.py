from systems.command.types import module
from utility.temp import temp_dir

import os


class Command(
    module.ModuleActionCommand
):
    def get_priority(self):
        return -80

    def groups_allowed(self):
        return 'kubernetes-admin'

    def parse_passthrough(self):
        return True

    def exec(self):
        with temp_dir() as temp:
            config_path = os.path.join(self.manager.data_dir, '.kube')

            command = ['kubectl', '--insecure-skip-tls-verify=true'] + self.options.get('args', [])
            success = self.sh(
                command,
                env = {
                    "KUBECONFIG": os.path.join(temp.link(config_path), 'config')
                },
                cwd = self.manager.module_dir,
                display = True
            )
            if not success:
                self.error("Kubectl command failed: {}".format(" ".join(command)))
