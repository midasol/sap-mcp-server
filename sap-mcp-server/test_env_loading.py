#!/usr/bin/env python3
"""
Test script to verify .env.server loading and SAP configuration
Run this to check if your SAP credentials are properly configured
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
import os

def test_env_loading():
    """Test environment variable loading from .env.server"""

    # Load environment variables
    env_path = Path(__file__).parent / ".env.server"
    if not env_path.exists():
        env_path = Path(__file__).parent / ".env"

    print(f"🔍 Loading environment from: {env_path}")
    print(f"   File exists: {env_path.exists()}")
    print()

    load_dotenv(dotenv_path=env_path)

    # Check required SAP variables
    required_vars = [
        "SAP_HOST",
        "SAP_PORT",
        "SAP_CLIENT",
        "SAP_USERNAME",
        "SAP_PASSWORD"
    ]

    print("📋 Environment Variables Check:")
    print("=" * 60)

    all_ok = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if var in ["SAP_PASSWORD", "SAP_USERNAME"]:
                display_value = "*" * 8 if value else "NOT SET"
            else:
                display_value = value

            # Check for placeholder values
            is_placeholder = value in [
                "your-sap-server.com",
                "your_username",
                "your_password"
            ]

            status = "⚠️  PLACEHOLDER" if is_placeholder else "✅ SET"
            print(f"{status} {var:20s} = {display_value}")

            if is_placeholder:
                all_ok = False
        else:
            print(f"❌ MISSING {var:20s}")
            all_ok = False

    print("=" * 60)
    print()

    # Try to create SAPConnectionConfig
    if all_ok:
        print("✅ All environment variables are set with real values")
        print("\nTesting SAPConnectionConfig creation...")

        try:
            from sap_mcp.config.settings import SAPConnectionConfig
            config = SAPConnectionConfig()
            print("✅ SAPConnectionConfig created successfully!")
            print(f"   Host: {config.host}")
            print(f"   Port: {config.port}")
            print(f"   Client: {config.client}")
            print(f"   Username: {'*' * len(config.username)}")
            print(f"   SSL Verify: {config.verify_ssl}")
            return True
        except Exception as e:
            print(f"❌ Failed to create SAPConnectionConfig: {e}")
            return False
    else:
        print("❌ Some environment variables are missing or have placeholder values")
        print("\n📝 Action Required:")
        print("   1. Edit .env.server file")
        print("   2. Replace placeholder values with actual SAP credentials:")
        print("      - SAP_HOST: Your actual SAP server hostname")
        print("      - SAP_USERNAME: Your SAP username")
        print("      - SAP_PASSWORD: Your SAP password")
        print("   3. Run this test again")
        return False

if __name__ == "__main__":
    success = test_env_loading()
    sys.exit(0 if success else 1)
