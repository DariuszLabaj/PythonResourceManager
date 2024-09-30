from py_resource_manager import ResourceManager

class ResourcesClass:
   """Auto-generated resource class"""
   _rm = ResourceManager()

   @property
   def helloWorld(self) -> str:
       return self._rm.get_string("helloWorld").strip()

Resources = ResourcesClass()