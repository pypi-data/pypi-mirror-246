# -*- coding: utf-8 -*-

from virtualenv_bootstrap import api


def test():
    _ = api


if __name__ == "__main__":
    from virtualenv_bootstrap.tests import run_cov_test

    run_cov_test(__file__, "virtualenv_bootstrap.api", preview=False)
