import os.path
import sys
from inspect import iscoroutinefunction
from importlib import import_module
from typing import Callable

from bald_spider.settings.settings_manager import SettingsManager


async def common_call(func: Callable, *args, **kwargs):
    if iscoroutinefunction(func):
        return await func(*args, **kwargs)
    else:
        return func(*args, **kwargs)

def _get_closest(path="."):
    path = os.path.abspath(path)
    return path

def _init_env():
    closest = _get_closest()
    if closest:
        project_dir = os.path.dirname(closest)
        sys.path.append(project_dir)

def get_settings(settings="settings"):
    _settings = SettingsManager()
    _init_env()
    _settings.set_settings(settings)
    return _settings

def merge_settings(spider, settings):
    if hasattr(spider, "custom_settings"):
        custom_settings = getattr(spider, "custom_settings")
        settings.update(custom_settings)

def load_class(path):
    if not isinstance(path, str):
        if callable(path):
            return path
        else:
            raise TypeError(f"args expected string or object, got: {type(path)}")

    module, name = path.rsplit(".", 1)
    mod = import_module(module)
    try:
        cls = getattr(mod, name)
    except AttributeError:
        raise NameError(f"Module {module!r} doesn't define any object named {name!r}")
    return cls