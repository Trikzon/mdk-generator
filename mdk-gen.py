#!/usr/bin/python3

import argparse
from pathlib import Path
import tomllib


def parse_config(config_file: str) -> dict[str, str]:
    config = dict()

    try:
        with open(args.config, "rb") as f:
            toml_data = tomllib.load(f)
    except Exception as e:
        print(f"Could not read config file {config_file}: {e}")
        exit(-1)
    
    for category in toml_data:
        if type(toml_data[category]) == str:
            mdkg_var = f"%MDKG_{category}%".upper()
            config[mdkg_var] = toml_data[category]

            continue

        for var in toml_data[category]:
            mdkg_var = f"%MDKG_{category}_{var}%".upper()
            config[mdkg_var] = toml_data[category][var]
    
    return config


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="MDK Generator")
    parser.add_argument("--config", default="config.toml")
    parser.add_argument("--template", default="mdk-template")
    parser.add_argument("--output", default="output")
    args = parser.parse_args()

    config = parse_config(args.config)

    template_path = Path(args.template)
    output_path = Path(args.output)

    for file_path in template_path.rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(template_path)
            target_path = output_path / relative_path

            target_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                with open(file_path, "r", encoding="utf-8") as src_file:
                    content = src_file.read()
                
                for variable, value in config.items():
                    content = content.replace(variable, value)
                
                with open(target_path, "w", encoding="utf-8") as dst_file:
                    dst_file.write(content)
                
            except:
                print(f"Copying file {file_path} as a binary file without transformation.")

                with open(file_path, "rb") as src_file:
                    with open(target_path, "wb") as dst_file:
                        dst_file.write(src_file.read())
