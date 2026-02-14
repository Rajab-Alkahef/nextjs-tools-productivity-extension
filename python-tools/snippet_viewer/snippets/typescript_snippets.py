"""
TypeScript snippets definitions in VS Code format
"""

# ============================================================================
# VS CODE SNIPPETS CONFIGURATION
# ============================================================================
# To add a new TypeScript snippet, add a dictionary to the snippets_list below
# Format (VS Code snippet format):
# {
#     "name": "Snippet Display Name",
#     "prefix": "trigger-word",
#     "body": [
#         "line 1 of code",
#         "line 2 of code",
#         "$1"  // $1, $2, etc. are tab stops
#     ],
#     "description": "What this snippet does"
# }
# ============================================================================

TYPESCRIPT_SNIPPETS = [
    {
        "name": "TypeScript Interface",
        "prefix": "ts-interface",
        "body": [
            "export interface ${1:InterfaceName} {",
            "\t${2:// properties}",
            "\tid: string;",
            "\tname: string;",
            "}"
        ],
        "description": "Basic TypeScript interface definition"
    },
    {
        "name": "TypeScript Type Alias",
        "prefix": "ts-type",
        "body": [
            "export type ${1:TypeName} = {",
            "\t${2:// properties}",
            "\tid: string;",
            "\tname: string;",
            "};"
        ],
        "description": "Type alias for complex types"
    },
    {
        "name": "TypeScript Enum",
        "prefix": "ts-enum",
        "body": [
            "export enum ${1:EnumName} {",
            "\t${2:VALUE1} = \"${3:value1}\",",
            "\t${4:VALUE2} = \"${5:value2}\"",
            "}"
        ],
        "description": "TypeScript enum definition"
    },
    {
        "name": "TypeScript Generic Function",
        "prefix": "ts-generic-fn",
        "body": [
            "export function ${1:functionName}<T extends ${2:BaseType}>(",
            "\t${3:data}: T,",
            "\tcallback: (item: T) => void",
            "): T {",
            "\tcallback(${3:data});",
            "\treturn ${3:data};",
            "}"
        ],
        "description": "Generic function with type parameters"
    },
    {
        "name": "TypeScript Class",
        "prefix": "ts-class",
        "body": [
            "export class ${1:ClassName} {",
            "\tprivate ${2:property}: ${3:string};",
            "",
            "\tconstructor(${2:property}: ${3:string}) {",
            "\t\tthis.${2:property} = ${2:property};",
            "\t}",
            "",
            "\t${4:// methods}",
            "}"
        ],
        "description": "TypeScript class with constructor"
    },
    {
        "name": "TypeScript Async Function",
        "prefix": "ts-async",
        "body": [
            "export async function ${1:functionName}(",
            "\t${2:param}: ${3:string}",
            "): Promise<${4:ReturnType} | null> {",
            "\ttry {",
            "\t\tconst response = await ${5:fetch}(${6:url});",
            "\t\t",
            "\t\tif (!response.ok) {",
            "\t\t\tthrow new Error(`Failed: ${response.statusText}`);",
            "\t\t}",
            "\t\t",
            "\t\tconst data: ${4:ReturnType} = await response.json();",
            "\t\treturn data;",
            "\t} catch (error) {",
            "\t\tconsole.error('Error:', error);",
            "\t\treturn null;",
            "\t}",
            "}"
        ],
        "description": "Async function with error handling"
    },
    {
        "name": "TypeScript React Component",
        "prefix": "ts-react-component",
        "body": [
            "import { ReactNode } from 'react';",
            "",
            "export interface ${1:ComponentName}Props {",
            "\t${2:// props}",
            "\tid: string;",
            "\tname: string;",
            "\tchildren?: ReactNode;",
            "}",
            "",
            "export function ${1:ComponentName}({",
            "\tid,",
            "\tname,",
            "\tchildren",
            "}: ${1:ComponentName}Props) {",
            "\treturn (",
            "\t\t<div>",
            "\t\t\t<h2>{name}</h2>",
            "\t\t\t{children}",
            "\t\t</div>",
            "\t);",
            "}"
        ],
        "description": "TypeScript React component with props"
    },
    {
        "name": "TypeScript Type Guard",
        "prefix": "ts-typeguard",
        "body": [
            "export function is${1:TypeName}(",
            "\tobj: unknown",
            "): obj is ${1:TypeName} {",
            "\treturn (",
            "\t\ttypeof obj === 'object' &&",
            "\t\tobj !== null &&",
            "\t\t'${2:id}' in obj &&",
            "\t\ttypeof (obj as ${1:TypeName}).${2:id} === 'string'",
            "\t);",
            "}"
        ],
        "description": "Type guard function for runtime type checking"
    },
    {
        "name": "TypeScript Utility Types",
        "prefix": "ts-utility",
        "body": [
            "// Partial - makes all properties optional",
            "type Partial${1:TypeName} = Partial<${2:BaseType}>;",
            "",
            "// Required - makes all properties required",
            "type Required${1:TypeName} = Required<${2:BaseType}>;",
            "",
            "// Pick - select specific properties",
            "type ${1:TypeName}Summary = Pick<${2:BaseType}, '${3:id}' | '${4:name}'>;",
            "",
            "// Omit - exclude specific properties",
            "type ${1:TypeName}WithoutDates = Omit<${2:BaseType}, '${5:createdAt}' | '${6:updatedAt}'>;"
        ],
        "description": "Common TypeScript utility types"
    },
    {
        "name": "TypeScript Discriminated Union",
        "prefix": "ts-union",
        "body": [
            "type ${1:StateName} =",
            "\t| { status: 'idle' }",
            "\t| { status: 'loading' }",
            "\t| { status: 'success'; data: ${2:DataType} }",
            "\t| { status: 'error'; error: Error };",
            "",
            "function handle${1:StateName}(state: ${1:StateName}) {",
            "\tswitch (state.status) {",
            "\t\tcase 'idle':",
            "\t\t\treturn 'Initial state';",
            "\t\tcase 'loading':",
            "\t\t\treturn 'Loading...';",
            "\t\tcase 'success':",
            "\t\t\treturn state.data;",
            "\t\tcase 'error':",
            "\t\t\treturn state.error.message;",
            "\t}",
            "}"
        ],
        "description": "Discriminated union for type-safe state management"
    },
    {
        "name": "Console Log",
        "prefix": "log",
        "body": [
            "console.log('${1:message}');",
            "${2}"
        ],
        "description": "Log output to console"
    },
    {
        "name": "TypeScript Arrow Function",
        "prefix": "ts-arrow",
        "body": [
            "const ${1:functionName} = (${2:param}: ${3:string}): ${4:ReturnType} => {",
            "\t${5:// body}",
            "\treturn ${6:value};",
            "};"
        ],
        "description": "TypeScript arrow function with types"
    },
    {
        "name": "TypeScript Mapped Type",
        "prefix": "ts-mapped",
        "body": [
            "type ${1:NewType} = {",
            "\treadonly [K in keyof ${2:BaseType}]: ${2:BaseType}[K];",
            "};"
        ],
        "description": "Mapped type for transforming object types"
    }
]
