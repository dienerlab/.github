# -*- coding: utf-8 -*-

import os
import sys
from subprocess import Popen, PIPE

has_conda = os.path.exists("%s/miniconda3/condabin/conda" % os.environ["HOME"])

MINICONDA_PATH = (
    "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
)
GITHUB_PATH = (
    "https://raw.githubusercontent.com/dienerlab/.github/main"
)
HOME = os.environ["HOME"]


def cleanup():
    """Remove downloaded files."""
    if os.path.exists("Miniconda3-latest-Linux-x86_64.sh"):
        os.remove("Miniconda3-latest-Linux-x86_64.sh")
    print("Cleaned up unneeded files.")


def run_and_check(args, check, message, failure, success):
    """Run a command and check that it worked."""
    print(f":: {message}")
    r = Popen(args, env=os.environ, stdout=PIPE, stderr=PIPE,
              universal_newlines=True)
    o, e = r.communicate()
    out = o + e
    if r.returncode == 0 and check in out:
        print(f":: {success}")
    else:
        print(f":: {failure} \n [error] {out}")
        cleanup()
        sys.exit(1)


if __name__ == "__main__":
    run_and_check(
        ["mv", "{HOME}/.bashrc", "{HOME}/.bashrc.old"],
        "",
        "Backing up old bashrc...",
        "failed backing up :/",
        "Done."
    )

    run_and_check(
            ["wget", f"{GITHUB_PATH}/.bashrc"],
            "saved",
            "Downloading bashrc...",
            "failed downloading bashrc 😭",
            "Done."
        )

    run_and_check(
            ["wget", f"{GITHUB_PATH}/.tmux.conf"],
            "saved",
            "Downloading tmux config",
            "failed downloading config 😭",
            "Done."
        )

    if not has_conda:
        run_and_check(
            ["wget", MINICONDA_PATH],
            "saved",
            "Downloading miniconda...",
            "failed downloading miniconda 😭",
            "Done."
        )

        run_and_check(
            ["bash", "Miniconda3-latest-Linux-x86_64.sh", "-bfp",
             "%s/miniconda3" % os.environ["HOME"]],
            "installation finished.",
            "Installing miniconda...",
            "could not install miniconda :/",
            "Installed miniconda to `~/miniconda3`."
        )
    else:
        print("Miniconda is already installed. Skipped.")

    run_and_check(
        ["%s/miniconda3/condabin/conda" % os.environ["HOME"], "init"],
        "",
        "Running conda init...",
        "failed initializing conda :/",
        "Initialized."
    )

    cleanup()

    print(":: Everything is A-OK. We recommend you connect and "
          "disconnect from the sever to start clean :D")
