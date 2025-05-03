from __future__ import annotations
from ..utils import Plugin
from ..network import NetworkClient
from ..plugins.common import ORGBPlugin
from ..plugins.effects import EffectsPlugin

PLUGIN_NAMES = {
    "OpenRGB Effects Plugin": EffectsPlugin
}


def create_plugin(plugin: Plugin, comms: NetworkClient) -> ORGBPlugin:
    return PLUGIN_NAMES[plugin.name](plugin, comms)