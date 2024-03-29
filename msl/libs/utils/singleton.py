# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Python Singleton BaseClass
#
# Usage:
#
# class MyClass(Singleton, otherClass):
#   pass
#
# ----------------------------------------------------------------------------------------


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Singleton instance creation."""
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance
