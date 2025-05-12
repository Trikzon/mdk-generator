# MDK Generator
A simple python script (`mdk-gen.py`) that recursively copies the content of a template folder to an output folder while replacing variables defined in a config file.

This is designed to standardize the build files across all of [my mods](https://github.com/stars/Trikzon/lists/minecraft-mods) making porting to new MC versions easier.

## Usage
```
python mdk-gen.py --config configs/mod.toml --template mdk-template --output ../mod-folder
```

The provided template only contains build files, which will overwrite any files with the same name in the output directory. This is destructive and cannot be undone, so I recommend using version control. All other files, such as java source code and assets, will be untouched and must be updated seperately.

### Configuration
MDK Generator uses TOML files for configuring the variables that are replaced.

A variable inside the template looks like
```
%MDKG_CATEGORY_VARIABLE%
```

and is defined in the TOML file like
```toml
[category]
variable = "foobar"
```

For example, the config
```toml
[fabric]
loom_version = "1.10-SNAPSHOT"
```

will replace the variable in the template
```
%MDKG_FABRIC_LOOM_VERSION%
```
