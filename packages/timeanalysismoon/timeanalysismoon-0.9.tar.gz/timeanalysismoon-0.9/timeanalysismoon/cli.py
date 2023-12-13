import importlib
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: timeanalysismoon file_name (without extension)")
        sys.exit(1)

    file_name = sys.argv[1]
    run_time_analysis(file_name)

def run_time_analysis(file_name):
    try:
        module = importlib.import_module(f"timeanalysismoon.{file_name}")
        functions = [func for func in dir(module) if callable(getattr(module, func))]
        for func_name in functions:
            func = getattr(module, func_name)
            if callable(func):
                print(f"Performing time analysis for {file_name}.{func_name}")
                func()
    except ImportError:
        print(f"{file_name} file not found")

if __name__ == "__main__":
    main()