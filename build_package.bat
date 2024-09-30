@echo off
:: Build Python package script
:: Ensure that setuptools and wheel are installed
echo Installing required tools (setuptools, wheel)...
pip install setuptools wheel

:: Build the package
echo Building the package...
python setup.py sdist bdist_wheel

echo Package build complete
pause