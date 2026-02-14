"""
Redux generation snippets extractor
"""


def extract_redux_snippets(extractor):
    """Extract redux generation snippets in VS Code format"""
    # Slice snippet
    slice_snippet = {
        "name": "Redux Slice",
        "prefix": "next-redux-slice",
        "body": [
            "import { createSlice, PayloadAction } from \"@reduxjs/toolkit\";",
            "import { initial${1:FeatureName}State } from \"./${2:camelCaseName}State\";",
            "",
            "const ${2:camelCaseName}Slice = createSlice({",
            "\tname: \"${2:camelCaseName}\",",
            "\tinitialState: initial${1:FeatureName}State,",
            "\treducers: {",
            "\t\t${3:// Add your reducers here}",
            "\t},",
            "});",
            "",
            "export const { } = ${2:camelCaseName}Slice.actions;",
            "export default ${2:camelCaseName}Slice.reducer;"
        ],
        "description": "Generates Redux slice with createSlice"
    }
    extractor._add_vscode_snippet("Redux", slice_snippet)

    # State snippet
    state_snippet = {
        "name": "Redux State",
        "prefix": "next-redux-state",
        "body": [
            "// State interface for ${1:FeatureName}",
            "export interface ${1:FeatureName}State {",
            "\t${2:// Add your state properties here}",
            "}",
            "",
            "export const initial${1:FeatureName}State: ${1:FeatureName}State = {",
            "\t${3:// Add your initial state here}",
            "};"
        ],
        "description": "Generates Redux state interface and initial state"
    }
    extractor._add_vscode_snippet("Redux", state_snippet)
