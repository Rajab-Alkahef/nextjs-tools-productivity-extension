import sys
import os
from pathlib import Path

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import to_camel_case, to_pascal_case


def generate_routes(feature_path: Path, feature_name: str):
    """Generate routes folder with route constants"""
    routes_path = feature_path / "routes"
    routes_path.mkdir(exist_ok=True)

    camel_case_name = to_camel_case(feature_name)
    pascal_case_name = to_pascal_case(feature_name)

    routes_content = f'''// Routes for {pascal_case_name}
export abstract class {pascal_case_name}Routes  {{
  // Add your routes here
  public static test= "/test"
}};
'''
    (routes_path / f"{camel_case_name}Routes.ts").write_text(routes_content, encoding='utf-8')
