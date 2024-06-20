#!/bin/bash

# Check if 'packages.json' exists
if [ ! -f "packages.json" ]; then
    echo "Error: 'packages.json' file not found."
    exit 1
fi

# Read 'packages.json' and install required packages
required_packages=$(python3 - << END
import json

with open('packages.json') as f:
    data = json.load(f)
    dependencies = data.get('dependencies', {})

    packages = []
    for package, version in dependencies.items():
        packages.append(f"{package}=={version}")

    print(" ".join(packages))
END
)

pip3 install --upgrade $required_packages
