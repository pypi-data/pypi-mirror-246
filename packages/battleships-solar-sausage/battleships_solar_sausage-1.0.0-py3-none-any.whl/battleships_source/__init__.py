#update documentation html
#sphinx-build -b html docs docs/_build

#create distribution package
#python setup.py sdist bdist_wheel

#pypi test
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*