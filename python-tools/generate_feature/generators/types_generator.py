import sys
import os
from pathlib import Path

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import to_camel_case, to_pascal_case


def generate_types(feature_path: Path, feature_name: str):
    """Generate types folder with interfaces and enums"""
    types_path = feature_path / "types"
    types_path.mkdir(exist_ok=True)
    (types_path / "interfaces").mkdir(exist_ok=True)
    (types_path / "enums").mkdir(exist_ok=True)

    camel_case_name = to_camel_case(feature_name)
    pascal_case_name = to_pascal_case(feature_name)
    
    interface_content = f'''export interface {pascal_case_name}Interface {{
  // Add your interface here
}}
'''
    (types_path / "interfaces" / f"{camel_case_name}Interface.ts").write_text(
        interface_content, encoding='utf-8')
