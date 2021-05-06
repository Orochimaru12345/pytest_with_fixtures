# Install dependencies
```shell
python -m pip install --upgrade pip
python -m pip install --upgrade pytest
python -m pip install --upgrade requests
python -m pip install --upgrade pytest-html
```

# Run
```shell
// all
python -m pytest --html=report.html

// without multiply container restarts
python -m pytest --html=report.html -m "not requires_fresh_app"
```