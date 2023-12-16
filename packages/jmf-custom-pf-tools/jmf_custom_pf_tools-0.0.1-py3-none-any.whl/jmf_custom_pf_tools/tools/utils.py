import yaml
from pathlib import Path
import re

def collect_tools_from_directory(base_dir) -> dict:
    tools = {}
    for f in Path(base_dir).glob("**/*.yaml"):
        with open(f, "r") as f:
            tools_in_file = yaml.safe_load(f)
            try:
                for identifier, tool in tools_in_file.items():
                    tools[identifier] = tool
            except:
                continue
    return tools


def list_package_tools():
    """List package tools"""
    import os
    print(os.getcwd())
    print(Path(__file__))
    yaml_dir = Path(__file__).parents[1] / "yamls"
    print(yaml_dir)
    return collect_tools_from_directory(yaml_dir)