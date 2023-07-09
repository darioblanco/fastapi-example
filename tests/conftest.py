import os

my_plugins = [
    "tests.initialize",
]


def pytest_configure(config):
    os.environ["ENV"] = "test"

    # -------------------------------------
    # Load fixtures listed in 'my_plugins'.

    for plugin_module in my_plugins:
        config.pluginmanager.import_plugin(plugin_module)
