git flow release start v$1
sed -i -e "s/__version__ = '.*'/__version__ = '$1'/g" flask_sandboy/__init__.py
rm -rf docs/_build
python setup.py develop
sphinx-build -aE docs build/docs > /dev/null
cd docs && make html && cd ..
git commit docs flask_sandboy/__init__.py -m "Update to version v$1"
git flow release finish v$1
python setup.py sdist upload -r pypi
python setup.py upload_docs -r pypi
