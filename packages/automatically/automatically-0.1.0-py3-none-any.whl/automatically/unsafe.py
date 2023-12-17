import sys
import importlib.abc
import importlib.machinery
import subprocess


def log(msg: str) -> None:
    print(f'DEBUG[automatically.unsafe]: {msg}', file=sys.stderr)


def pip_install(package: str) -> bool:
    '''Install a package using pip
    
    Args:
        package (str): The package to install. The input is not sanitized, and is passed directly to pip!
    
    Returns:
        bool: True if the package was installed successfully, False otherwise.
    '''
    try:
        out = subprocess.check_output([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        log(e)
        return False
    log(out)
    return True
    


class AutoFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        log(f"fullname: {fullname}, path: {path}, target: {target}")
        success = pip_install(fullname)
        if success:
            return importlib.machinery.PathFinder.find_spec(fullname)
        return None



# Create an instance of your finder
finder = AutoFinder()

# Add your finder to the meta path
sys.meta_path.append(finder)
