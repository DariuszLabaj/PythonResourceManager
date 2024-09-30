from py_resource_manager import ResourceManager, CultureInfo
ResourceManager("Resources")
from Resources_class import Resources

if __name__ == "__main__":
    CultureInfo.SetCulture("pl_PL")
    print(Resources.helloWorld)