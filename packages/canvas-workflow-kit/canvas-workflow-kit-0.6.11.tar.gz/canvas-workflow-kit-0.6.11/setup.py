# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['canvas_workflow_kit',
 'canvas_workflow_kit.builtin_cqms',
 'canvas_workflow_kit.builtin_cqms.future',
 'canvas_workflow_kit.builtin_cqms.stubs',
 'canvas_workflow_kit.builtin_cqms.tests',
 'canvas_workflow_kit.builtin_cqms.tests.mixins',
 'canvas_workflow_kit.internal',
 'canvas_workflow_kit.tests',
 'canvas_workflow_kit.tests.get_protocols_unittest',
 'canvas_workflow_kit.tests.mock_data.empty',
 'canvas_workflow_kit.tests.sdk',
 'canvas_workflow_kit.tests.value_set',
 'canvas_workflow_kit.value_set',
 'canvas_workflow_kit.value_set.customer_value_sets',
 'canvas_workflow_kit.value_set.v2021',
 'canvas_workflow_kit.value_set.v2022']

package_data = \
{'': ['*'],
 'canvas_workflow_kit.builtin_cqms.stubs': ['.mypy_cache/3.6/*',
                                            '.mypy_cache/3.6/collections/*'],
 'canvas_workflow_kit.builtin_cqms.tests': ['mock_data/cms122v6_diabetes_no/*',
                                            'mock_data/cms122v6_diabetes_yesnotest/*',
                                            'mock_data/cms122v6_diabetes_yeswithtest/*',
                                            'mock_data/cms123v6_diabetes_no/*',
                                            'mock_data/cms123v6_diabetes_yes/*',
                                            'mock_data/cms123v6_diabetes_yesdone/*',
                                            'mock_data/cms125v6_woman_due/*',
                                            'mock_data/cms125v6_woman_mammography/*',
                                            'mock_data/cms125v6_woman_mastectomy/*',
                                            'mock_data/cms130v6_patient_due/*',
                                            'mock_data/cms130v6_patient_satisfied/*',
                                            'mock_data/cms131v6_diabetes_no/*',
                                            'mock_data/cms131v6_diabetes_yesnoreferralreport/*',
                                            'mock_data/cms131v6_diabetes_yeswithreferralreport/*',
                                            'mock_data/cms134v6_diabetes_no/*',
                                            'mock_data/cms134v6_diabetes_yes/*',
                                            'mock_data/cms134v6_diabetes_yes_only/*',
                                            'mock_data/cms138v6/*',
                                            'mock_data/diabetes_mixin/*',
                                            'mock_data/diabetic1/*',
                                            'mock_data/feet1/*',
                                            'mock_data/hcc001v1/*',
                                            'mock_data/hcc002v2_diagnosed/*',
                                            'mock_data/hcc003v1_diagnosed/*',
                                            'mock_data/hcc004v1/*',
                                            'mock_data/hcc005v1/*',
                                            'mock_data/patient/*'],
 'canvas_workflow_kit.tests': ['mock_data/*',
                               'mock_data/full/*',
                               'mock_data/partial/*'],
 'canvas_workflow_kit.tests.sdk': ['mock_data/bmi1/*',
                                   'mock_data/bmi1_with_instruction/*',
                                   'mock_data/bmi2/*',
                                   'mock_data/depression1/*',
                                   'mock_data/depression2/*',
                                   'mock_data/diabetic1/*',
                                   'mock_data/diabetic2/*',
                                   'mock_data/diabetic3/*',
                                   'mock_data/diabetic4/*',
                                   'mock_data/example/*',
                                   'mock_data/fall1/*',
                                   'mock_data/feet1/*',
                                   'mock_data/fluvax/*',
                                   'mock_data/highrisk1/*',
                                   'mock_data/nonsmoker/*',
                                   'mock_data/referral/*']}

install_requires = \
['arrow',
 'cached-property>=1.5.0,<1.6.0',
 'click',
 'memoization>=0.4.0,<0.5.0',
 'python-decouple>=3.0.0,<4.0.0',
 'requests>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['canvas-cli = canvas_workflow_kit.canvas_cli:cli']}

setup_kwargs = {
    'name': 'canvas-workflow-kit',
    'version': '0.6.11',
    'description': 'Development kit to empower customization of your Canvas instance',
    'long_description': None,
    'author': 'Canvas Team',
    'author_email': 'engineering@canvasmedical.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
