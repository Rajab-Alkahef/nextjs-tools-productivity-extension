import sys
import os
from pathlib import Path

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import to_pascal_case


def generate_components(feature_path: Path, feature_name: str):
    """Generate components folder with Container"""
    components_path = feature_path / "components"
    components_path.mkdir(exist_ok=True)

    pascal_case_name = to_pascal_case(feature_name)
    container_content = f'''import BasePage from "@/components/BasePage";

export default function {pascal_case_name}Container() {{
  return (
    <BasePage>
      <div className="flex flex-col bg-card rounded-xl space-y-4">
     
      </div>
    </BasePage>
  );
}}
'''
    (components_path / f"{pascal_case_name}Container.tsx").write_text(
        container_content, encoding='utf-8')
