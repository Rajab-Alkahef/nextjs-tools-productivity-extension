import sys
import os
from pathlib import Path

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import to_pascal_case


def generate_page(feature_path: Path, feature_name: str, use_dynamic_route: bool):
    """Generate page.tsx file"""
    page_folder = feature_path
    if use_dynamic_route:
        dynamic_folder = feature_path / "[[...id]]"
        dynamic_folder.mkdir(exist_ok=True)
        page_folder = dynamic_folder

    pascal_case_name = to_pascal_case(feature_name)
    import_path = "../components" if use_dynamic_route else "./components"
    page_content = f'''import {pascal_case_name}Container from "{import_path}/{pascal_case_name}Container";
export default function {pascal_case_name}Page() {{
  return <{pascal_case_name}Container />;
}}
'''
    (page_folder / "page.tsx").write_text(page_content, encoding='utf-8')
