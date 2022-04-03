# Installation Requirements

The `noise` module used in our application requires the following:
[Visual CPP Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

If you do NOT install the build tools the noise module will fail to install. Thus, this
project will not work.

Run the pip install on our `requirements.txt` file.

```bash
pip install -r requirements.txt
```

If you were ever wondering how this file is created... 
```bash
pip freeze > requirements.txt
```

If using a virtual environment it'll grab all the things being used INSIDE this venv. 
Makes it easy to share projects with other people. Otherwise, this command will output
all the modules installed on your machine, whether they're actually needed or not.

---
[Previous Section](overview.md) | [Next Section](ui_ui_element.md)