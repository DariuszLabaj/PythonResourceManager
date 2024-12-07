import os
from pathlib import Path
import xml.etree.ElementTree as ET

from .culture_info import CultureInfo
from ._singleton import Singleton


class ResourceManager(metaclass=Singleton):
    compiled = False

    def __init__(self, resource_file_path: str = "resources"):
        self.resources: dict[str, str] = {}
        self.localized_resources: dict[str, dict[str, str]] = {}
        self.__load_all_resources(resource_file_path)

    def __load_all_resources(self, resource_file_path: str):
        """
        Load all resource files: main `resources.xml` and localized files like `resources.en.xml`.
        """
        main_file = f"{resource_file_path}.xml"
        if os.path.exists(main_file):
            fallback = self.__load_resources(main_file)
            if fallback:
                self.resources = fallback
            else:
                raise ET.ParseError()
        else:
            raise FileNotFoundError(f"Main resource file {main_file} not found.")
        if "/" in resource_file_path or "\\" in resource_file_path:
            paths = resource_file_path.replace("\\", "/")
            pathData = "/".join(paths.split("/")[:-1])
            filename = paths.split("/")[-1]
            for file in os.listdir(pathData):
                if file.startswith(filename) and file.endswith(".xml") and file != (filename+".xml"):
                    culture_code = file.replace(filename + ".", "").replace(".xml", "")
                    resource = self.__load_resources(pathData+"/"+file)
                    if resource is not None:
                        self.localized_resources[culture_code] = resource
        else:
            for file in os.listdir():
                if file.startswith(resource_file_path) and file.endswith(".xml") and file != main_file:
                    culture_code = file.replace(resource_file_path + ".", "").replace(".xml", "")
                    resource = self.__load_resources(file)
                    if resource is not None:
                        self.localized_resources[culture_code] = resource
        if not ResourceManager.compiled:
            self.__generate_class(resource_file_path)

    def __load_resources(self, file_path: str) -> dict[str, str] | None:
        """
        Loads resources from a single XML file into a dictionary.
        """
        localizedResources: dict[str, str] = {}
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            for data in root.findall('data'):
                key = data.get('name')
                if (key is None):
                    continue
                element = data.find('value')
                if not (hasattr(element, "text")):
                    continue
                value = element.text  # type: ignore
                if (value is None):
                    continue
                localizedResources[key] = value
        except (FileNotFoundError, ET.ParseError):
            return None
        return localizedResources

    def get_string(self, key: str) -> str:
        """
       Retrieves a string for the current culture or falls back to the main resources.
       """
        current_culture = CultureInfo.CurrentCulture
        if current_culture in self.localized_resources:
            return self.localized_resources[current_culture].get(key, self.resources.get(key, f"[[{key}]]"))
        else:
            return self.resources.get(key, f"[[{key}]]")

    def __generate_class(self, output_file: str):
        """
        Generate a Python class with properties that return strings based on the current culture.
        """
        file_path = f"{output_file}_class.py"
        class_name = Path(output_file).name
        class_template = "from py_resource_manager import ResourceManager" \
            "\n" \
            "\n" \
            f"class {class_name.title()}Class:\n" \
            "    \"\"\"Auto-generated resource class\"\"\"\n" \
            "    _rm = ResourceManager()"\
            "\n" \
            "    def findString(self, value: str) -> str:\n"\
            "        return self._rm.get_string(value.replace(" ", "")).strip()\n"\
            "{properties}\n" \
            "\n" \
            f"{class_name} = {class_name}Class()"
        property_template = "\n" \
            "    @property\n" \
            "    def {key}(self) -> str:\n" \
            "        return self._rm.get_string(\"{key}\").strip()"
        properties = ""
        for key in self.resources.keys():
            properties += property_template.format(key=key)
        data = class_template.format(properties=properties)
        with open(file_path, "w") as file:
            file.write(data)
        ResourceManager.compiled = True
