# python-dia

A library for producing and manipulating
[Dia diagrams](http://dia-installer.de/) files.
[More on my website](https://sosie-js.github.io/python-dia/)

## Limitations

* This version does provide pythondia access only to objects. 
Thus, you have to use the dia api to run the meaning on each code change,
meaning you will have to close , open dia and watch errors on console to fix the 
script. Invalid scripts will not be accessible from dia app.

* For now, only objects UML Class and Database Table are supported

## Contributing

Feel free to add other object and fixes.

## Development

### Compile .egg

```shell
$ ./package.sh
```

### Upload to PyPI

1. Create an API Token from the Web UI. (Edit your `~/.pypirc` with the generated token.)
2. Install Twine
```shell
$ python3 -m pip install --user --upgrade twine
```
3. Upload the bundle
```shell
$ python3 -m twine upload dist/*
```

Note: The upload to PyPI is currently assured by GitHub Actions.


### Release

1. Increase the version number in `setup.py`.
2. Commit and push.
3. Create a new tag in GitHub to trigger the CI pipeline.

