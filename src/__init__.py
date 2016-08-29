"""Netify: turn boring things into stuff for the net."""
from .startup import cli_main
from .startup import uwsgi_main

__ALL__ = [cli_main, uwsgi_main]
