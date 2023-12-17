# nationalmhfilter

The package showcases the statistics for each state in the United States, and mental heanlth care records of different social groups, providing evidence and directions to improve healthcare services.

## Installation

```bash
$ pip install nationalmhfilter
```

## Usage

To retrieve the overall mental health service situation of a state
```bash
get_service_counts_by_state(records_clean, state)
```

To get the counts of people who received a specific service across the nation
```bash
get_service_counts(records_clean, service_indicator)
```

To get the service overview of people with the specified presence of symptoms of anxiety/depressionn 
```bash
display_indicators_for_symptom_presence(records_clean, presence_filter)
```

Specify query parameters in terms of age, sex, gender identity, race, and education to get service records
```bash
get_service_indicators_by_parameters(records_clean, age=None, sex=None, race=None, education=None, gender_identity=None)
```
Refer to parameters.md and example.ipynb to fully use the filters. Users are able to get the general understanding of disparities of current mental health services in the US. The multiple filters allow people who interested in mental healthcare issues flexibly contrast between states, age and gender groups, and education levels. It showcases potential challenges faced by various social subgroups, prompting a need to improve healthcare services.

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`nationalmhfilter` was created by Fanxi Wang. It is licensed under the terms of the MIT license.

## Credits

`nationalmhfilter` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
