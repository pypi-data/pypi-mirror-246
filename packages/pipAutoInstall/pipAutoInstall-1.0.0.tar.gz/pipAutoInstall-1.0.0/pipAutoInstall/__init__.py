from subprocess import run

def tryToImport(module, args='*'):
    try:
        exec(f"from {module} import {args}")
    except ModuleNotFoundError:
        run(["pip", "install", module])
        exec(f"from {module} import {args}")
