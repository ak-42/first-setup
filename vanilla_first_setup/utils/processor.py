# processor.py
#
# Copyright 2022 mirkobrombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundationat version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import logging
import tempfile
import subprocess


logger = logging.getLogger("FirstSetup::Processor")


class Processor:

    @staticmethod
    def run(log_path, commands):
        logger.info("processing the following commands: \n%s" %
                    '\n'.join(commands))

        # generating a temporary file to store all the commands so we can
        # run them all at once
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("#!/bin/sh\n")
            f.write("# This file was created by FirstSetup\n")
            f.write("# Do not edit this file manually\n\n")

            for command in commands:
                f.write(f"{command}\n")

            f.flush()
            f.close()

            # setting the file executable
            os.chmod(f.name, 0o755)

            # here we run the file trough pkexec to get root privileges
            # log the output to the log file
            proc = subprocess.run(
                ["pkexec", "sh", f.name],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )

            # write the output to the log file so the packager can see what
            # happened during the installation process
            try:
                with open(log_path, 'a') as log:
                    log.write(proc.stdout.decode('utf-8'))
                    log.flush()
            except Exception as e:
                logger.warning("failed to write to the log file: %s" % e)
                logger.warning("the output of the commands is: %s" % proc.stdout)

            if proc.returncode != 0:
                logger.critical(
                    "Error while processing commands, see log for details.")
                return False

        autostart_file = os.path.expanduser(
            "~/.config/autostart/io.github.vanilla-os.FirstSetup.desktop")
        if os.path.exists(autostart_file):
            os.remove(autostart_file)

        return True
