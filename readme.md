# Install dependencies
```shell
python -m pip install --upgrade pip
python -m pip install --upgrade pytest
python -m pip install --upgrade requests
python -m pip install --upgrade pytest-html
python -m pip install --upgrade docker
```

# Run
```shell
// all
python -m pytest --html=report.html

// without multiply container restarts
python -m pytest --html=report.html -m "not requires_fresh_app"
```

# Requirements
System must have Docker installed.

Docker must have the 'test_app:latest' image.