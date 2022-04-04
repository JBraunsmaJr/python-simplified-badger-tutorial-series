# Environment

## Pycharm
If you're using Pycharm you can skip this and move to [Next Section](ui_ui_element.md)

## Other IDE
We need to create a virtual environment for our project

The `noise` module used in our application requires the following:
[Visual CPP Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

If you do NOT install the build tools the noise module will fail to install. Thus, this
project will not work.

A virtual environment makes it easy to use different versions of modules between
projects as well as easy to share with other devs!

Without a virtual environment... you end up sharing ALL the things installed on your machine
versus what's ACTUALLY needed for your project.

Open a terminal and navigate to this project directory

```bash
python3 -m venv ./venv
```

Activate environment and install requirements
```bash
./venv/Scripts/activate
pip install -r requirements.txt
```

You can then run the application via 
```bash
python ./game.py
```

## How to make requirements.txt
If you were ever wondering how this `requirements.txt` file was created... 
```bash
pip freeze > requirements.txt
```

If using a virtual environment it'll grab all the things being used INSIDE this venv. 
Makes it easy to share projects with other people. Otherwise, this command will output
all the modules installed on your machine, whether they're actually needed or not.

---
[Previous Section](overview.md) | [Next Section](ui_ui_element.md)