import sys
import os
from pathlib import Path

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import to_camel_case, to_pascal_case


def generate_config(feature_path: Path, feature_name: str, config_file_name: str = None):
    """Generate config folder with form configuration"""
    config_path = feature_path / "config"
    config_path.mkdir(exist_ok=True)

    camel_case_name = to_camel_case(feature_name)
    pascal_case_name = to_pascal_case(feature_name)
    config_file_name = config_file_name or f"{camel_case_name}Config"
    
    config_content = f'''// Configuration for {pascal_case_name}
import {{ DynamicForm }} from "@/utils/types";
import {{ useTranslations }} from "next-intl";
import {{ MdNumbers }} from "react-icons/md";
import {{ z }} from "zod";

export const {camel_case_name}Form = (isCreate: boolean) =>
  z
    .object({{
      name: z.string().min(1, {{ message: "required" }}),

    }})
    .superRefine((data, ctx) => {{

    }});

export type {camel_case_name}FormType = z.infer<
  ReturnType<typeof {camel_case_name}Form>
>;

export const Get{camel_case_name}Form = (): DynamicForm<{camel_case_name}FormType> => {{
  const t = useTranslations("{camel_case_name}");

  return {{
    id: "{camel_case_name}Form",
    title: t("{camel_case_name}"),
    fields: {{
      name: {{
        name: "name",
        label: t("name"),
        type: "text",
        placeholder: t("enterName"),
        icon: MdNumbers,
      }},

    }},
    endpoint: {{}},
  }};
}};

'''
    (config_path / f"{config_file_name}.ts").write_text(config_content, encoding='utf-8')
