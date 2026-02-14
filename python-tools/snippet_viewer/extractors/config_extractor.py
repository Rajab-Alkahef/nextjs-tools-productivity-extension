"""
Config generation snippets extractor
"""


def extract_config_snippets(extractor):
    """Extract config generation snippets in VS Code format"""
    config_snippet = {
        "name": "Form Configuration",
        "prefix": "next-form-config",
        "body": [
            "// Configuration for ${1:FeatureName}",
            "import { DynamicForm } from \"@/utils/types\";",
            "import { useTranslations } from \"next-intl\";",
            "import { MdNumbers } from \"react-icons/md\";",
            "import { z } from \"zod\";",
            "",
            "export const ${2:camelCaseName}Form = (isCreate: boolean) =>",
            "\tz",
            "\t\t.object({",
            "\t\t\tname: z.string().min(1, { message: \"required\" }),",
            "\t\t\t${3:// more fields}",
            "\t\t})",
            "\t\t.superRefine((data, ctx) => {",
            "\t\t\t${4:// validation logic}",
            "\t\t});",
            "",
            "export type ${2:camelCaseName}FormType = z.infer<",
            "\tReturnType<typeof ${2:camelCaseName}Form>",
            ">;",
            "",
            "export const Get${2:camelCaseName}Form = (): DynamicForm<${2:camelCaseName}FormType> => {",
            "\tconst t = useTranslations(\"${2:camelCaseName}\");",
            "",
            "\treturn {",
            "\t\tid: \"${2:camelCaseName}Form\",",
            "\t\ttitle: t(\"${2:camelCaseName}\"),",
            "\t\tfields: {",
            "\t\t\tname: {",
            "\t\t\t\tname: \"name\",",
            "\t\t\t\tlabel: t(\"name\"),",
            "\t\t\t\ttype: \"text\",",
            "\t\t\t\tplaceholder: t(\"enterName\"),",
            "\t\t\t\ticon: MdNumbers,",
            "\t\t\t},",
            "\t\t\t${5:// more fields}",
            "\t\t},",
            "\t\tendpoint: {},",
            "\t};",
            "};"
        ],
        "description": "Generates form configuration with Zod validation and DynamicForm"
    }
    extractor._add_vscode_snippet("Config", config_snippet)
