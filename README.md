# Installable Python Project

This is a template for a baic Python project that can be installed with pip. The project demonstrates the following concepts:

- Whitelist model for `.gitignore`
- Basic project folder layout
- Configuring an installable Python package using `pyproject.toml`
- Retrieving useful directories with `pathlib`
- The difference in behavior between running a script and importing a module.
- Basic object oriented programming concepts in Python.


## Installation

To begin, first clone the repository and enter it:

```sh
git clone https://github.com/profminton/installable_project_structure.git
cd installable_project_structure
```

To see how it works, first install it into a Python environment of your choice in editable mode. For instance, to install it using a venv created inside ther repository directory do the following:

```sh
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

This will install a module called `example_project` along with all of its dependencies. Then try out the two scripts in the `examples` folder.

If you want to use this in a different environment that is not co-located with the repository, just point to the path where the repository is located in your pip command:

```sh
pip install -e /path/to/installable_project_structure/
```

## The whitelist .gitignore

I like to use a *whitelist* model for my `.gitignore` files. The idea is simply to ignore everything by default and then list only the files (or file patterns) and directories that you want tracked. This cuts down on having to guess what kinds of files and folders need to be ignored so they don't accidentally get committed to the repo (things like, venv folders, python cache files, VS Code workspace files, etc.)

## Project folder layout

The project uses a fairly typical project layout:

```
installable_project_structure
├── .gitignore
├── data
│   └── .gitignore
├── examples
│   ├── example_fit.py
│   └── example_outputs.py
├── LICENSE
├── plots
│   └── .gitignore
├── pyproject.toml
├── README.md
├── src
│   └── example_project
│       ├── __init__.py
│       └── main.py
└── tests
    └── test_example.py
```

The main `.gitgnore` file in the root of the project is the only one with content in it. The ones contained in the `data` and `plots` folders only exist so that those folders can be tracked even when they are "empty", as git tracks files not folders. Therefore a clean clone of this repo will come pre-loaded with those folders.

The `pyproject.toml` file is what pip uses to install the project as an importable module using the contents of the `src` folder. The `__init__.py` file allows the `example_project` folder to be treated as a module, with any Python scripts inside as submodules. I've included a basic set of import statements as a way of "flattening" the namespace of the project (see the comments inside for details).

## Retrieving useful directories with pathlib

Never hard-code paths in your project scripts, as these won't work on other computers (or even your own computer if you reorganize things!).  Instead, make use of the `pathlib` to manage folder locations, filenames, etc. I've included a basic example that shows how to retrieve directories based on the locations of the scripts being run.

## Scripts that are run directly vs imported

Ever wonder what that mysterious bit of code does that you often see in Python scripts that looks like this?

```py
if __name__ == "__main__":
    # stuff
    ...
```

This is used to define code that is only run when the script is run directly vs when it is run on import.  When you call `import example_project` in a script, all of the code in the `main.py` file is run. up until it gets to that line. The value of the special variable `__name__` will __not__ be `"__main__"`, it will instead be `"example_project.main"`. Only the scipt that you actually ran using the Python interpreter will have that value.

Therefore, if you run the `main.py` file directly, then `__name__` __will__ be called `"__main__"` and that code will execute. 

```sh
$ python -c "import example_project"
This should always appear.
```

```sh
$ python src/example_project/main.py
This should always appear.
This won't appear when I'm imported.
I am a function.
I was imported by myself
I am located in /Users/daminton/git/installable_project_structure/src/example_project
My current working directory is /Users/daminton/git/installable_project_structure
```
