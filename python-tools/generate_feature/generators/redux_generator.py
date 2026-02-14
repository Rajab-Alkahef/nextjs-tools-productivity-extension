import sys
import os
from pathlib import Path

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import to_camel_case, to_pascal_case


def generate_redux(feature_path: Path, feature_name: str):
    """Generate redux folder with slices and state"""
    redux_path = feature_path / "redux"
    redux_path.mkdir(exist_ok=True)

    camel_case_name = to_camel_case(feature_name)
    pascal_case_name = to_pascal_case(feature_name)

    slices_content = f'''import {{ createSlice, PayloadAction }} from "@reduxjs/toolkit";
import {{ initial{pascal_case_name}State }} from "./{camel_case_name}State";



const {camel_case_name}Slice = createSlice({{
  name: "{camel_case_name}",
  initialState: initial{pascal_case_name}State,
  reducers: {{
    // Add your reducers here
  }},
}});

export const {{ }} = {camel_case_name}Slice.actions;
export default {camel_case_name}Slice.reducer;
'''
    (redux_path / f"{camel_case_name}Slices.ts").write_text(
        slices_content, encoding='utf-8')

    state_content = f'''// State interface for {pascal_case_name}
export interface {pascal_case_name}State {{
  // Add your state properties here
}}

export const initial{pascal_case_name}State: {pascal_case_name}State = {{
  // Add your initial state here
}};
'''
    (redux_path / f"{camel_case_name}State.ts").write_text(state_content, encoding='utf-8')
