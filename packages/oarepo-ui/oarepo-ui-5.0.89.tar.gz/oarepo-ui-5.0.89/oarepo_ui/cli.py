import json as json_lib
import sys
from pathlib import Path

import click
from flask.cli import with_appcontext
from oarepo_runtime.cli import oarepo

from oarepo_ui.proxies import current_oarepo_ui


@oarepo.group("ui")
def ui():
    """UI commands"""


@ui.command("renderers")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
@click.option("--json", is_flag=True, help="Format output as json")
@click.option("--output-file", help="Save output to this file")
@with_appcontext
def renderers(verbose, json, output_file):
    """List available UI renderers for (detail) page"""
    if output_file:
        of = open(output_file, "w")
    else:
        of = sys.stdout
    if json:
        json_data = []
        for macro, lib in sorted(current_oarepo_ui.templates.get_macros().items()):
            macro = macro[7:]
            json_data.append({"renderer": macro, "file": str(lib.filename)})
        json_lib.dump(json_data, of, indent=4, ensure_ascii=False)
    else:
        for macro, lib in sorted(current_oarepo_ui.templates.get_macros().items()):
            macro = macro[7:]
            if verbose:
                print(f"{macro:40s}: {lib.filename}", file=of)
            else:
                print(f"{macro:40s}: {Path(lib.filename).name}", file=of)
    if output_file:
        of.close()
