# Skillcorner

![Coverage](https://img.shields.io/gitlab/pipeline-coverage/public-corner%2Fskillcorner)
![Build](https://img.shields.io/gitlab/pipeline-status/public-corner%2Fskillcorner)
![PyPI - Version](https://img.shields.io/pypi/v/:skillcorner)
![Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/gitlab/license/public-corner%2Fskillcorner)

Python sdk for [SkillCorner API](https://www.skillcorner.com/api/docs).

Powered by [fitrequest](https://gitlab.com/public-corner/fitrequest).

## Help

See [documentation](https://skillcorner.readthedocs.io/en/latest/) for more details.

## Installation

Install using `pip install -U skillcorner`.
See the [installation](https://skillcorner.readthedocs.io/en/latest/getting_started.html#installation) section in the documentation.

## A Simple Example
See the [examples](https://skillcorner.readthedocs.io/en/latest/getting_started.html#examples) section in the documentation.
```py
from skillcorner.client import SkillcornerClient

client = SkillcornerClient(<SKILLCORNER_USERNAME>, <SKILLCORNER_PASSWORD>)

teams = client.get_teams()
```

## Contact
You can contact Skillcorner Team at: support@skillcorner.com.
