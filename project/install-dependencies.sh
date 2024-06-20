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
        if package == "SQLAlchemy":
            packages.append(f"{package}=={version}")
        else:
            packages.append(f"{package}")
    print(" ".join(packages))
END
)

pip install --upgrade $required_packages
