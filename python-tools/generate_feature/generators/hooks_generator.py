import sys
import os
from pathlib import Path

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import to_pascal_case


def generate_hooks(feature_path: Path, feature_name: str):
    """Generate hooks folder with custom hook"""
    hooks_path = feature_path / "hooks"
    hooks_path.mkdir(exist_ok=True)

    pascal_case_name = to_pascal_case(feature_name)
    hook_content = f'''export const use{pascal_case_name} = () => {{
  // Add your hook logic here
  return {{}};
}}
'''
    (hooks_path / f"use{pascal_case_name}.ts").write_text(hook_content, encoding='utf-8')
