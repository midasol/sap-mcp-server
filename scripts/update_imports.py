#!/usr/bin/env python3
"""Update import statements in migrated files"""

import os
import re
from pathlib import Path
from typing import Dict, List

# Import mappings for server
IMPORT_MAPPINGS = {
    # Config imports
    r'from \.\.config\.schemas import': 'from sap_mcp_server.config.schemas import',
    r'from \.\.config\.services_loader import': 'from sap_mcp_server.config.loader import',
    r'from \.\.config\.settings import': 'from sap_mcp_server.config.settings import',

    # Core imports (from sap/ directory)
    r'from \.auth import': 'from sap_mcp_server.core.auth import',
    r'from \.exceptions import': 'from sap_mcp_server.core.exceptions import',
    r'from \.client import': 'from sap_mcp_server.core.sap_client import',

    # Protocol imports (removed)
    r'from \.\.protocol\.': '# REMOVED: from sap_mcp_server.tools.',
}


def update_file_imports(file_path: Path) -> bool:
    """Update imports in a single file

    Returns:
        True if file was modified, False otherwise
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content

        # Apply all import mappings
        for pattern, replacement in IMPORT_MAPPINGS.items():
            content = re.sub(pattern, replacement, content)

        # Write back if changed
        if content != original:
            file_path.write_text(content, encoding='utf-8')
            return True

        return False

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False


def main():
    """Main function"""
    print("🔄 Updating import statements in migrated files...")

    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Server source directory
    server_src = project_root / "packages/server/src/sap_mcp_server"

    if not server_src.exists():
        print(f"❌ Server source directory not found: {server_src}")
        print("   Run create_structure.sh first!")
        return 1

    # Track statistics
    files_processed = 0
    files_modified = 0

    # Process all Python files
    for py_file in server_src.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue

        files_processed += 1
        if update_file_imports(py_file):
            files_modified += 1
            print(f"✅ Updated: {py_file.relative_to(project_root)}")

    # Summary
    print()
    print(f"📊 Summary:")
    print(f"   Processed: {files_processed} files")
    print(f"   Modified:  {files_modified} files")

    if files_modified > 0:
        print()
        print("⚠️  Please review the changes and test the code!")
        print("   git diff packages/server/src/")

    return 0


if __name__ == "__main__":
    exit(main())
