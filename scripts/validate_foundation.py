import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    ".env.example",
    ".gitignore",
    ".dockerignore",
    ".pre-commit-config.yaml",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "Makefile",
    "README.md",
    "SECURITY.md",
    "VERSION",
    "docker-compose.yml",
    "package.json",
    "pyproject.toml",
]


REQUIRED_DIRECTORIES = [
    "apps",
    "core",
    "runtime",
    "adapters",
    "plugins",
    "security",
    "contracts",
    "packages",
    "config",
    "infrastructure",
    "tests",
    "examples",
    "docs",
    "scripts",
    ".github",
]


def validate_files() -> list[str]:
    errors: list[str] = []

    for relative_path in REQUIRED_FILES:
        path = ROOT / relative_path

        if not path.is_file():
            errors.append(f"Missing required file: {relative_path}")

    return errors


def validate_directories() -> list[str]:
    errors: list[str] = []

    for relative_path in REQUIRED_DIRECTORIES:
        path = ROOT / relative_path

        if not path.is_dir():
            errors.append(f"Missing required directory: {relative_path}")

    return errors


def main() -> int:
    errors = validate_files()
    errors.extend(validate_directories())

    if errors:
        print("Nexora foundation validation FAILED.")

        for error in errors:
            print(f"- {error}")

        return 1

    print("Nexora foundation validation PASSED.")
    print(f"Repository: {ROOT}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
