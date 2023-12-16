# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['healthcheck']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-healthchecklib',
    'version': '0.1.1',
    'description': 'Opinionated healthcheck library',
    'long_description': '# Python Healthcheck Lib\n\nThis is an opinionated library to help with structuring healthchecks in your python application.\n\nIt will not help you with the healthcheck logic itself, but it will help you build the response in a standard format.\n\nWe aim at supporting almost exactly the standard described in https://datatracker.ietf.org/doc/html/draft-inadarei-api-health-check. Although it\'s just a expired draft, it seems to be the better standard on healthchecks out there as of this writing.\n\nThis standard is not fully supported yet, see the [roadmap](#roadmap) for more information.\n\n## Installation\n\n```bash\n# With pip\npip install python-healthchecklib\n\n# With poetry\npoetry add python-healthchecklib\n```\n\n## Concepts\n\nThe main concepts to keep in mind when using this library are the `service` and `components` concepts.\n\nWe consider a `service` to be the application as a whole. It\'s the thing that is running and that you want to check the health of.\n\nWe consider `components` to be the different parts of the application that you want to check the health of, being them internal or external. For example, if you have a web application, you might want to check the health of the database, the cache, internal components, etc.\n\nYou\'ll be responsible for implementing the healthcheck logic for each component, but this library will help you build the response in a standard format and define the health of the `service` based on the health of its `components`.\n\n## Usage\n\nThe lib exposes asynchronous methods, which makes it easy to use with either sync or async codebases.\n\n```python\nfrom healthcheck import Healthcheck, HealthcheckDatastoreComponent, HealthcheckCallbackResponse\n\n# Create a healthcheck instance\nhealthcheck = Healthcheck(\n    name="My Service"\n)\n\n# Create a component\ndb_component = HealthcheckDatastoreComponent(\n    name="MySQL",\n)\n\n# Define the healthcheck logic for the component.\n# They should be async functions that return a HealthcheckCallbackResponse\nasync def db_healthcheck():\n    # Implement some logic to check the health of the database\n    return HealthcheckCallbackResponse(\n        status="pass",\n        output="Database is healthy",\n        affects_service_health=True\n    )\n\n# Add the healthcheck logic to the component\ndb_component.add_healthcheck(db_healthcheck)\n\n# You can add more than one healthcheck to a component, which means that this is a component made of multiple instances.\nasync def db_healthcheck_2():\n    # Implement some logic to check the health of the database\n    return HealthcheckCallbackResponse(\n        status="warn",\n        output="Responsive but high latency",\n        affects_service_health=False\n    )\n\ndb_component.add_healthcheck(db_healthcheck_2)\n\n# Add the component to the healthcheck\nhealthcheck.add_component(db_component)\n\n# Get the health status of the service\nstatus = await healthcheck.run()\n\n# In case you\'re in a sync context, you can use `asyncio.run` to run the async code:\nstatus = asyncio.run(healthcheck.run())\n\n# Print the status\nprint(status)\n\n# {\n#   "status": "pass",\n#   "description": "Health status of My Service",\n#   "checks": {\n#     "MySQL": [\n#       {\n#         "status": "pass",\n#         "output": "Database is healthy",\n#         "componentType": "datastore",\n#         "componentName": "MySQL\n#       },\n#       {\n#         "status": "warn",\n#         "output": "Responsive but high latency",\n#         "componentType": "datastore",\n#         "componentName": "MySQL\n#       }\n#     ]\n#   }\n# }\n```\n\n## Roadmap\n\n- [ ] Support for manually setting the component health status (instead of passing a callback)\n- [ ] Support for the optional fields in the service status described in https://datatracker.ietf.org/doc/html/draft-inadarei-api-health-check#name-status\n- [ ] Support for the optional fields in the component staus described in https://datatracker.ietf.org/doc/html/draft-inadarei-api-health-check#name-the-checks-object\n- [ ] Support for defining customized keys for the component status object\n\nWe welcome contributions to help us achieve these goals. See below how to contribute.\n\n## Contributing\n\nSee the [contributing guide](CONTRIBUTING.md) for more information.\n\n## License\n\nBy contributing to python-healthchecklib, you agree that your contributions will be licensed under the [MIT License](https://opensource.org/licenses/MIT).',
    'author': 'Hathor Team',
    'author_email': 'contact@hathor.network',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/HathorNetwork/python-healthcheck-lib/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
