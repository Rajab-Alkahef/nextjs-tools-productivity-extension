import sys
import os
from pathlib import Path

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import to_camel_case, to_pascal_case


def generate_services(feature_path: Path, feature_name: str, query_file_name: str = None):
    """Generate services folder with endpoints and queries"""
    services_path = feature_path / "services"
    services_path.mkdir(exist_ok=True)

    camel_case_name = to_camel_case(feature_name)
    pascal_case_name = to_pascal_case(feature_name)

    # Generate endpoints
    endpoints_content = f'''// API endpoints for {pascal_case_name}
export abstract class {pascal_case_name}EndPoints  {{
  // Add your endpoints here
  public static test = "/test";
}};
'''
    (services_path / f"{camel_case_name}EndPoints.ts").write_text(
        endpoints_content, encoding='utf-8')

    # Generate queries
    queries_path = services_path / "queries"
    queries_path.mkdir(exist_ok=True)

    query_file_name = query_file_name or f"useGetAll{pascal_case_name}"
    query_content = f'''import {{ useCbsQuery }}from "@/hooks/useCbsQuery";
import {{ usePathname }} from "next/navigation";
import {{ {pascal_case_name}EndPoints }} from "../../services/{camel_case_name}EndPoints";
import {{ {pascal_case_name}Interface }} from "../../types/interfaces/{camel_case_name}Interface";
import {{ modulesApi }} from "@/utils/fetching/types";



export const useGetAll{pascal_case_name} = ({{
  page,
  module = "till"

}}: {{
  page?: number;
  module?: modulesApi

}}) => {{
  const pathname = usePathname();
  const {{ data, isLoading, isFetching, refetch }} =
    useCbsQuery<{pascal_case_name}Interface>(
      [
        "{camel_case_name}",
        pathname,
        page,
        
      ],
      
      {pascal_case_name}EndPoints.test,
      {{ module: module }},
      {{
        pageNum: page,
      
      }}
    );

  return {{ data, isLoading, isFetching, refetch }};
}};

'''
    (queries_path / f"{query_file_name}.ts").write_text(query_content, encoding='utf-8')


def generate_mutations(feature_path: Path, feature_name: str, mutation_file_name: str):
    """Generate mutations folder with mutation hook"""
    mutations_path = feature_path / "services" / "mutations"
    mutations_path.mkdir(exist_ok=True)

    camel_case_name = to_camel_case(feature_name)
    
    mutation_content = f'''import {{ useCbsMutation }} from "@/hooks/useCbsQuery";
import {{ toast }} from "react-toastify";
import {{ modulesApi }} from "@/utils/fetching/types";


export const use{mutation_file_name}Mutation = ({{
  url,
  onError,
  onSuccess,
  module  = "till"
}}: {{
  url: string;
  onError: () => void;
  onSuccess: () => void;
  module?: modulesApi
}}) => {{
  const {{
    mutate: {camel_case_name},
    isPending,
    data,
    isSuccess,
    isError,
  }} = useCbsMutation(
    url,
    {{ module: module }},
    {{
      onSuccess: (data) => {{
        if (data.succeeded) {{

          toast.success(data.message ?? "Request created successfully");
          onSuccess();
        }} else {{
          toast.dismiss();

          toast.error(data.message ?? "Failed to create request");
          onError();
        }}
      }},
      onError: (error) => {{
        console.error(error);
        toast.dismiss();

        toast.error("Server error occurred");
        onError();
      }},
    }}
  );

  return {{ {camel_case_name}, isPending, data, isSuccess, isError }};
}};

'''
    (mutations_path / f"use{mutation_file_name}Mutation.ts").write_text(mutation_content, encoding='utf-8')
