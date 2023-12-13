import os
from importlib.util import spec_from_file_location, module_from_spec
import inspect

from zrcl3.list_module import get_imports_via_ast
from zrcl3.io import create_bkup

def gather_init_vars(directory : str):
    pkg = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith(".py"):
                continue

            pkg_path = os.path.join(root, file)
            pkg_name = pkg_path.replace("\\", ".").replace("/", ".").replace(".py", "")
            if pkg_name.endswith("__init__"):
                pkg_name = pkg_name[:-9]
            
            spec = spec_from_file_location(file, os.path.join(root, file))
            module = module_from_spec(spec)
            spec.loader.exec_module(module) 

            import_list = get_imports_via_ast(pkg_path)

            specified_all = getattr(module, "__all__", None)

            if specified_all is not None and len(specified_all) > 0:
                pkg[pkg_name] = specified_all
            else:
                pkg[pkg_name] = []
                for name, element in inspect.getmembers(module):
                    if name.startswith("_"):
                        continue
                    
                    if name in import_list or name in import_list.values():
                        continue

                    pkg[pkg_name].append(name)

    return pkg

def generate_init(directory : str, safe : bool = False):
    pkg = gather_init_vars(directory)

    if os.path.exists(os.path.join(directory, "__init__.py")):
        create_bkup(
            os.path.join(directory, "__init__.py"),
            os.getcwd(),
        )

    with open(os.path.join(directory, "__init__.py"), "w") as f:
        tabcount =1 if not safe else 2


        for name, elements in pkg.items():
            if safe:
                f.write("try:\n")
                f.write("\t") 

            f.write(f"from {name} import (\n")
            for element in elements:
                f.write('\t' * tabcount)
                f.write(f"{element}, \n")

            f.write("\t" * (tabcount-1))
            f.write(")\n")

            if safe:
                f.write("except ImportError:\n")
                for element in elements:
                    f.write(f"\t{element} = None\n")
                f.write("\n")