
root_path=$(dirname "$0")/..  
cd $root_path
python setup.py sdist bdist_wheel upload
#python3 setup.py build 
#twine upload --verbose --repository-url https://upload.pypi.org/legacy/ dist/*
cd -
