"""
Publish script for pypenny package.

Reads the PyPI token from .pypi-token file and publishes the package using uv.
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Main entry point for the publish script."""
    try:
        # Read token from .pypi-token file
        token_file = Path('.pypi-token')
        
        if not token_file.exists():
            print("Error: .pypi-token file not found", file=sys.stderr)
            print("Please create a .pypi-token file with your PyPI token on the first line", file=sys.stderr)
            sys.exit(1)
        
        lines = token_file.read_text('utf-8').splitlines()
        token = None
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith('pypi'):
                token = stripped_line
                break
        
        if token is None:
            print("Error: No line starting with 'pypi' found in .pypi-token file.", file=sys.stderr)
            print("Please ensure your PyPI token line starts with 'pypi'.", file=sys.stderr)
            sys.exit(1)

        if not token: # This check handles cases where the line is just 'pypi' or 'pypi '
            print("Error: The identified PyPI token line is empty or invalid.", file=sys.stderr)
            sys.exit(1)
        
        # Run uv publish with the token
        print("Publishing package to PyPI...")
        result = subprocess.run(
            ['uv', 'publish', '-t', token],
            check=True,
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        print("✅ Package published successfully!")
        print("Check https://pypi.org/project/pypenny/ for the latest version.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to publish package", file=sys.stderr)
        print(e.stdout, file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
