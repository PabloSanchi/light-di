from typing import Type, Dict, Any
import inspect

DEFAULT_QUALIFIER = "default"

class DependencyContainer:
    def __init__(self):
        self._abstract_to_impl: Dict[Type, Dict[str, Type]] = {}
        self._primary_impl: Dict[Type, Type] = {}

    def register_impl(self, abstract_cls: Type, impl_cls: Type, qualifier: str = None, primary: bool = False):
        """Registers an implementation for an abstract class."""
        if abstract_cls not in self._abstract_to_impl:
            self._abstract_to_impl[abstract_cls] = {}
    
        key = qualifier or DEFAULT_QUALIFIER
        self._abstract_to_impl[abstract_cls][key] = impl_cls
    
        if primary:
            self._primary_impl[abstract_cls] = impl_cls

        if abstract_cls not in self._primary_impl and DEFAULT_QUALIFIER not in self._abstract_to_impl[abstract_cls]:
            self._primary_impl[abstract_cls] = impl_cls
    
    def resolve(self, cls: Type, qualifier: str = None) -> Any:
        """Resolves a class or abstract class to its implementation."""
        if cls in self._abstract_to_impl:
            if qualifier:
                if qualifier not in self._abstract_to_impl[cls]:
                    raise KeyError(f"No implementation found for {cls} with qualifier '{qualifier}'")

                impl_cls = self._abstract_to_impl[cls][qualifier]
            else:
                impl_cls = self._primary_impl.get(cls) or self._abstract_to_impl[cls].get(DEFAULT_QUALIFIER)
                if not impl_cls:
                    raise KeyError(f"No default or primary implementation found for {cls}")

            return self._resolve_with_dependencies(impl_cls)
        elif inspect.isabstract(cls):
            raise TypeError(f"Cannot instantiate abstract class {cls.__name__}.")
        else:
            return self._resolve_with_dependencies(cls)
    

    def _resolve_with_dependencies(self, cls: Type) -> Any:
        """Resolve dependencies for the constructor and instantiate the class."""
        sig = inspect.signature(cls)
        resolved_args = {}
        for name, param in sig.parameters.items():
            if param.annotation != param.empty:
                qualifier = getattr(param.annotation, "__qualifier__", None)
                resolved_args[name] = self.resolve(param.annotation, qualifier)
        return cls(**resolved_args)


container = DependencyContainer()


def implementation(qualifier: str = None, primary: bool = False):
    """Decorator to register an implementation for an abstract class."""
    def decorator(impl_cls: Type):
        bases = inspect.getmro(impl_cls)
        abstract_cls = next(
            (base for base in bases if inspect.isabstract(base) and base is not impl_cls),
            None
        )
        if not abstract_cls:
            raise RuntimeError(
                f"Cannot infer abstract class for {impl_cls}. "
                "Ensure it inherits from an abstract base class."
            )

        container.register_impl(abstract_cls, impl_cls, qualifier, primary)
        return impl_cls
    return decorator


def inject(cls: Type):
    """Decorator to automatically inject dependencies into a class."""
    def wrapper(*args, **kwargs):
        sig = inspect.signature(cls)
        resolved_args = {}
        for name, param in sig.parameters.items():
            if name not in kwargs and param.annotation != param.empty:
                qualifier = getattr(param.annotation, "__qualifier__", None)
                resolved_args[name] = container.resolve(param.annotation, qualifier)
        resolved_args.update(kwargs)
        return cls(*args, **resolved_args)
    return wrapper

def wire(var_type: Type, qualifier: str = None):
    """Function to wire a dependency to a variable."""
    return container.resolve(var_type, qualifier)
