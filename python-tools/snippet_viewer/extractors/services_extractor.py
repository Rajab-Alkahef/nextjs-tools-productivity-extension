"""
Services generation snippets extractor
"""


def extract_services_snippets(extractor):
    """Extract services generation snippets in VS Code format"""
    # Endpoints snippet
    endpoints_snippet = {
        "name": "API Endpoints",
        "prefix": "next-endpoints",
        "body": [
            "// API endpoints for ${1:FeatureName}",
            "export abstract class ${1:FeatureName}EndPoints {",
            "\t// Add your endpoints here",
            "\tpublic static ${2:endpointName} = \"/${3:endpoint-path}\";",
            "}"
        ],
        "description": "Generates abstract class for API endpoints"
    }
    extractor._add_vscode_snippet("Services", endpoints_snippet)

    # Query snippet
    query_snippet = {
        "name": "React Query Hook",
        "prefix": "next-query",
        "body": [
            "import { useCbsQuery } from \"@/hooks/useCbsQuery\";",
            "import { usePathname } from \"next/navigation\";",
            "import { ${1:FeatureName}EndPoints } from \"../../services/${2:camelCaseName}EndPoints\";",
            "import { ${1:FeatureName}Interface } from \"../../types/interfaces/${2:camelCaseName}Interface\";",
            "import { modulesApi } from \"@/utils/fetching/types\";",
            "",
            "export const useGetAll${1:FeatureName} = ({",
            "\tpage,",
            "\tmodule = \"till\"",
            "}: {",
            "\tpage?: number;",
            "\tmodule?: modulesApi",
            "}) => {",
            "\tconst pathname = usePathname();",
            "\tconst { data, isLoading, isFetching, refetch } =",
            "\t\tuseCbsQuery<${1:FeatureName}Interface>(",
            "\t\t\t[",
            "\t\t\t\t\"${2:camelCaseName}\",",
            "\t\t\t\tpathname,",
            "\t\t\t\tpage,",
            "\t\t\t],",
            "\t\t\t${1:FeatureName}EndPoints.${3:endpointName},",
            "\t\t\t{ module: module },",
            "\t\t\t{",
            "\t\t\t\tpageNum: page,",
            "\t\t\t}",
            "\t\t);",
            "",
            "\treturn { data, isLoading, isFetching, refetch };",
            "};"
        ],
        "description": "Generates useQuery hook with useCbsQuery"
    }
    extractor._add_vscode_snippet("Services", query_snippet)

    # Mutation snippet
    mutation_snippet = {
        "name": "React Mutation Hook",
        "prefix": "next-mutation",
        "body": [
            "import { useCbsMutation } from \"@/hooks/useCbsQuery\";",
            "import { toast } from \"react-toastify\";",
            "import { modulesApi } from \"@/utils/fetching/types\";",
            "",
            "export const use${1:MutationName}Mutation = ({",
            "\turl,",
            "\tonError,",
            "\tonSuccess,",
            "\tmodule = \"till\"",
            "}: {",
            "\turl: string;",
            "\tonError: () => void;",
            "\tonSuccess: () => void;",
            "\tmodule?: modulesApi",
            "}) => {",
            "\tconst {",
            "\t\tmutate: ${2:camelCaseName},",
            "\t\tisPending,",
            "\t\tdata,",
            "\t\tisSuccess,",
            "\t\tisError,",
            "\t} = useCbsMutation(",
            "\t\turl,",
            "\t\t{ module: module },",
            "\t\t{",
            "\t\t\tonSuccess: (data) => {",
            "\t\t\t\tif (data.succeeded) {",
            "\t\t\t\t\ttoast.success(data.message ?? \"Request created successfully\");",
            "\t\t\t\t\tonSuccess();",
            "\t\t\t\t} else {",
            "\t\t\t\t\ttoast.dismiss();",
            "\t\t\t\t\ttoast.error(data.message ?? \"Failed to create request\");",
            "\t\t\t\t\tonError();",
            "\t\t\t\t}",
            "\t\t\t},",
            "\t\t\tonError: (error) => {",
            "\t\t\t\tconsole.error(error);",
            "\t\t\t\ttoast.dismiss();",
            "\t\t\t\ttoast.error(\"Server error occurred\");",
            "\t\t\t\tonError();",
            "\t\t\t},",
            "\t\t}",
            "\t);",
            "",
            "\treturn { ${2:camelCaseName}, isPending, data, isSuccess, isError };",
            "};"
        ],
        "description": "Generates useMutation hook with useCbsMutation"
    }
    extractor._add_vscode_snippet("Services", mutation_snippet)
