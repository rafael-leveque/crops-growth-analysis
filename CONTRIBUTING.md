# Crops growth analysis

## Structure

The project is divided into three parts:

````
.
├── crops_growth_analysis
│   ├── extract
│   ├── process
|   ├── display
│   └── store
└── data
````

- The `extract` part is responsible for reading csv and loading sentinel-2 items.
- The `process` part is responsible for loading images and calculating the NDVI and NDWI.
- The `store` part is responsible for storing the NDVI and NDWI values in a database.
- The `display` part is responsible for displaying the NDVI and NDWI values.


## Lint

To lint the project, you can use the makefile :

```bash
make lint
```

Lint uses the following tools:

- [black](https://github.com/psf/black) : code formatter
- [flake8](https://flake8.pycqa.org/) : code linter
- [pylint](https://www.pylint.org/) : code linter
- [isort](https://pycqa.github.io/isort/) : import sorter
- [mypy](http://mypy-lang.org/) : static type checker

## Test

Currently, the project has no tests. May be interstin to add some in the future, testing csv extraction, sentinel data validity, process results, etc...

## Contributing

Since no tickets are used, commits names are prefixed with the correct edited part : Extract, Process, Store, Display, etc...

