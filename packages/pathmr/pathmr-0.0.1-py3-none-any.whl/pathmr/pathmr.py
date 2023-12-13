from contextlib import contextmanager
import os
import os.path


class ImproperlyConfigured(Exception):
    pass


def has_stuff(path):
    if isinstance(path, (Pathmr, PathmrFile)):
        return True
    if isinstance(path, (list, tuple)) and not isinstance(path, str):
        return len(path) > 0 and all(element not in (0, "") for element in path)
    if isinstance(path, str):
        return len(path) > 0
    return False


class Pathmr(os.PathLike):
    """Contains code from django-environs (see LICENSE)
    https://github.com/joke2k/django-environ/blob/main/environ/environ.py
    """

    @classmethod
    def resolve(cls, *paths):
        resolved_path = cls._absolute_join("", *paths)
        if os.path.isdir(resolved_path):
            return Pathmr(resolved_path)
        elif os.path.isfile(resolved_path):
            """its totally cool for a class to be aware of its own subclass, right?"""
            return PathmrFile(resolved_path)
        else:
            raise ValueError(f"Path does not exist: {resolved_path}")

    def path(self, *paths, **kwargs):
        resolved_path = self._absolute_join(self.__root__, *paths)
        if os.path.isdir(resolved_path):
            return Pathmr(resolved_path)
        raise ValueError(f"Path does not exist: {resolved_path}")

    @staticmethod
    def arg_type(arg):
        try:
            return Pathmr(arg)
        except Exception:
            raise ValueError(Exception)

    def isdir(self):
        return os.path.isdir(self.__str__())

    def isfile(self):
        return os.path.isfile(self.__str__())

    @property
    def parent(self):
        return os.path.dirname(self.__root__)

    def cd(self, start="", *paths, **kwargs):
        if start:
            self.__root__ = self._absolute_join(start, *paths)
        os.chdir(self.__root__)
        return self.__root__

    @property
    def root(self):
        return self.__root__

    def __init__(self, start="", *paths, **kwargs):
        absolute = self._absolute_join(start, *paths)
        self.__root__ = absolute

    def __call__(self, *paths, **kwargs):
        return self._absolute_join(self.__root__, *paths)

    def __eq__(self, other):
        return (
            self.__root__ == other
            if isinstance(other, str)
            else self.__root__ == other.__root__
            if isinstance(other, (Pathmr, PathmrFile))
            else False
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if not isinstance(other, Pathmr):
            return Pathmr(self.__root__, other)
        return Pathmr(self.__root__, other.__root__)

    def __sub__(self, other):
        if isinstance(other, int):
            return self.path(self.parent * other)
        elif isinstance(other, str):
            if self.__root__.endswith(other):
                return Pathmr(self.__root__.rstrip(other))
        raise TypeError(
            "unsupported operand type(s) for -: '{self}' and '{other}' "
            + "unless value of {self} ends with value of {other}".format(
                self=type(self), other=type(other)
            )
        )

    def __invert__(self):
        return self.parent

    def __contains__(self, item):
        base_path = self.__root__
        if len(base_path) > 1:
            base_path = os.path.join(base_path, "")
        return item.__root__.startswith(base_path)

    def __repr__(self):
        return "<Path:{}>".format(self.__root__)

    def __str__(self):
        return self.__root__

    def __unicode__(self):
        return self.__str__()

    def __fspath__(self):
        return self.__str__()

    @staticmethod
    def _absolute_join(base, *paths):
        base = os.path.realpath(base)
        absolute_path = (
            os.path.realpath(os.path.join(base, *paths)) if has_stuff(paths) else base
        )
        if not os.path.isdir(absolute_path):
            raise ImproperlyConfigured(
                "Directory does not exist: {}".format(absolute_path)
            )
        return absolute_path


class PathmrFile(Pathmr):
    def __init__(self, start="", *paths, **kwargs):
        super().__init__(start, *paths, **kwargs)
        self.basename, self.ext = os.path.splitext(os.path.basename(self.root))

    def __repr__(self):
        return "<Path:{}>".format(self.__root__)

    def isfile(self):
        """Doesn't matter if exists"""
        return True

    def isdir(self):
        return False

    def basename(self):
        return os.path.basename(self.__root__)

    @property
    def exists(self):
        return os.path.isfile(self.__root__)

    @contextmanager
    def read(self, mode="r"):
        name = self.__root__
        f = open(name, mode)
        try:
            yield f, name
        finally:
            f.close()

    @staticmethod
    def _absolute_join(base, *paths, **kwargs):
        real = os.path.realpath(base)
        # if no extra arguments are provided, assume that base is a file
        if not has_stuff(paths):
            absolute_path = real
        else:
            absolute_path = os.path.realpath(
                os.path.join(os.path.dirname(real), *paths)
            )

        if os.path.isdir(absolute_path):
            raise ImproperlyConfigured(
                "File must not be an existing directory: {}".format(absolute_path)
            )

        # here we make sure parent directory exists
        if not os.path.isfile(absolute_path):
            parent = os.path.dirname(absolute_path)
            if not os.path.isdir(parent):
                raise ImproperlyConfigured(
                    f"Parent directory does not exist: {parent}."
                    + "File doesn't need to exist, but its containing folder does"
                )

        return absolute_path

    def path(self, *paths):
        resolved_path = self._absolute_join(self.parent, *paths)
        if os.path.isdir(resolved_path):
            return Pathmr(resolved_path)
        raise ValueError(f"Path does not exist: {resolved_path}")

    @staticmethod
    def arg_type(arg):
        try:
            return PathmrFile(arg)
        except Exception:
            raise ValueError(Exception)
