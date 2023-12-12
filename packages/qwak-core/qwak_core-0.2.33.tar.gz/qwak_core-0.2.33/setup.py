# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['_qwak_proto',
 '_qwak_proto.qwak.administration.account.v1',
 '_qwak_proto.qwak.administration.authenticated_user.v1',
 '_qwak_proto.qwak.administration.v0.authentication',
 '_qwak_proto.qwak.administration.v0.environments',
 '_qwak_proto.qwak.administration.v0.users',
 '_qwak_proto.qwak.admiral.user_application_instance.v0',
 '_qwak_proto.qwak.analytics',
 '_qwak_proto.qwak.audience.v1',
 '_qwak_proto.qwak.auto_scaling.v1',
 '_qwak_proto.qwak.automation.v1',
 '_qwak_proto.qwak.batch_job.v1',
 '_qwak_proto.qwak.build.v1',
 '_qwak_proto.qwak.build_settings',
 '_qwak_proto.qwak.builds',
 '_qwak_proto.qwak.data_versioning',
 '_qwak_proto.qwak.deployment',
 '_qwak_proto.qwak.ecosystem.v0',
 '_qwak_proto.qwak.execution.v1',
 '_qwak_proto.qwak.execution.v1.jobs',
 '_qwak_proto.qwak.execution.v1.jobs.reports',
 '_qwak_proto.qwak.execution.v1.state',
 '_qwak_proto.qwak.feature_store.entities',
 '_qwak_proto.qwak.feature_store.features',
 '_qwak_proto.qwak.feature_store.jobs',
 '_qwak_proto.qwak.feature_store.jobs.v1',
 '_qwak_proto.qwak.feature_store.reports',
 '_qwak_proto.qwak.feature_store.serving',
 '_qwak_proto.qwak.feature_store.serving.v1',
 '_qwak_proto.qwak.feature_store.sources',
 '_qwak_proto.qwak.features_operator.v1',
 '_qwak_proto.qwak.features_operator.v2',
 '_qwak_proto.qwak.features_operator.v3',
 '_qwak_proto.qwak.file_versioning',
 '_qwak_proto.qwak.fitness_service',
 '_qwak_proto.qwak.inference.feedback',
 '_qwak_proto.qwak.instance_template',
 '_qwak_proto.qwak.kube_deployment_captain',
 '_qwak_proto.qwak.logging',
 '_qwak_proto.qwak.models',
 '_qwak_proto.qwak.monitoring.v0',
 '_qwak_proto.qwak.projects',
 '_qwak_proto.qwak.secret_service',
 '_qwak_proto.qwak.self_service.account.v0',
 '_qwak_proto.qwak.self_service.user.v1',
 '_qwak_proto.qwak.traffic.v1',
 '_qwak_proto.qwak.user_application.common.v0',
 '_qwak_proto.qwak.user_application.v0',
 '_qwak_proto.qwak.vectors.v1',
 '_qwak_proto.qwak.vectors.v1.collection',
 '_qwak_proto.qwak.vectors.v1.collection.event',
 '_qwak_proto.qwak.workspace',
 'qwak',
 'qwak.automations',
 'qwak.clients',
 'qwak.clients._inner',
 'qwak.clients.administration',
 'qwak.clients.administration.authenticated_user',
 'qwak.clients.administration.authentication',
 'qwak.clients.administration.eco_system',
 'qwak.clients.administration.environment',
 'qwak.clients.administration.self_service',
 'qwak.clients.alert_management',
 'qwak.clients.alerts_registry',
 'qwak.clients.analytics',
 'qwak.clients.audience',
 'qwak.clients.automation_management',
 'qwak.clients.autoscaling',
 'qwak.clients.batch_job_management',
 'qwak.clients.build_management',
 'qwak.clients.build_orchestrator',
 'qwak.clients.data_versioning',
 'qwak.clients.deployment',
 'qwak.clients.feature_store',
 'qwak.clients.file_versioning',
 'qwak.clients.instance_template',
 'qwak.clients.kube_deployment_captain',
 'qwak.clients.logging_client',
 'qwak.clients.model_management',
 'qwak.clients.project',
 'qwak.clients.secret_service',
 'qwak.clients.user_application_instance',
 'qwak.clients.vector_store',
 'qwak.clients.workspace_manager',
 'qwak.exceptions',
 'qwak.feature_store',
 'qwak.feature_store._common',
 'qwak.feature_store.data_sources',
 'qwak.feature_store.data_sources.batch',
 'qwak.feature_store.data_sources.streaming',
 'qwak.feature_store.data_sources.streaming.kafka',
 'qwak.feature_store.entities',
 'qwak.feature_store.execution',
 'qwak.feature_store.feature_sets',
 'qwak.feature_store.offline',
 'qwak.feature_store.offline.athena',
 'qwak.feature_store.online',
 'qwak.feature_store.validations',
 'qwak.inner',
 'qwak.inner.build_config',
 'qwak.inner.build_logic',
 'qwak.inner.build_logic.build_loggers',
 'qwak.inner.build_logic.constants',
 'qwak.inner.build_logic.interface',
 'qwak.inner.build_logic.phases',
 'qwak.inner.build_logic.phases.phase_010_fetch_model',
 'qwak.inner.build_logic.phases.phase_010_fetch_model.fetch_strategy_manager',
 'qwak.inner.build_logic.phases.phase_010_fetch_model.fetch_strategy_manager.strategy',
 'qwak.inner.build_logic.phases.phase_010_fetch_model.fetch_strategy_manager.strategy.folder',
 'qwak.inner.build_logic.phases.phase_010_fetch_model.fetch_strategy_manager.strategy.git',
 'qwak.inner.build_logic.phases.phase_010_fetch_model.fetch_strategy_manager.strategy.zip',
 'qwak.inner.build_logic.phases.phase_020_remote_register_qwak_build',
 'qwak.inner.build_logic.run_handlers',
 'qwak.inner.build_logic.tools',
 'qwak.inner.di_configuration',
 'qwak.inner.instance_template',
 'qwak.inner.runtime_di',
 'qwak.inner.tool',
 'qwak.inner.tool.grpc',
 'qwak.inner.tool.run_config',
 'qwak.model',
 'qwak.model.adapters',
 'qwak.model.adapters.input_adapters',
 'qwak.model.adapters.output_adapters',
 'qwak.model.decorators',
 'qwak.model.decorators.impl',
 'qwak.model.tools',
 'qwak.model.tools.adapters',
 'qwak.model.tools.adapters.input_adapters',
 'qwak.model.tools.adapters.output_adapters',
 'qwak.model.utils',
 'qwak.model_loggers',
 'qwak.qwak_client',
 'qwak.qwak_client.batch_jobs',
 'qwak.qwak_client.build_api_helpers',
 'qwak.qwak_client.builds',
 'qwak.qwak_client.builds.filters',
 'qwak.qwak_client.data_versioning',
 'qwak.qwak_client.deployments',
 'qwak.qwak_client.file_versioning',
 'qwak.qwak_client.models',
 'qwak.qwak_client.projects',
 'qwak.testing',
 'qwak.tools',
 'qwak.tools.logger',
 'qwak.utils',
 'qwak.vector_store',
 'qwak.vector_store.utils',
 'qwak_services_mock',
 'qwak_services_mock.mocks',
 'qwak_services_mock.mocks.utils',
 'qwak_services_mock.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML',
 'dependency-injector>=4.0',
 'grpcio>=1.32.0',
 'joblib>=1.3.2,<2.0.0',
 'marshmallow-dataclass>=8.5.8,<9.0.0',
 'python-jose',
 'python-json-logger>=2.0.2',
 'requests',
 'retrying==1.3.4',
 'typeguard>=2,<3']

extras_require = \
{':extra == "feature-store"': ['cloudpickle==2.2.1'],
 ':python_full_version >= "3.7.1" and python_version < "3.10"': ['protobuf>=3.10,<4'],
 ':python_version >= "3.10"': ['protobuf>=4.21.6'],
 'feature-store': ['pyarrow>=6.0.0', 'pyathena>=2.2.0,!=2.18.0']}

setup_kwargs = {
    'name': 'qwak-core',
    'version': '0.2.33',
    'description': 'Qwak Core contains the necessary objects and communication tools for using the Qwak Platform',
    'long_description': '# Qwak Core\n\nQwak is an end-to-end production ML platform designed to allow data scientists to build, deploy, and monitor their models in production with minimal engineering friction.\nQwak Core contains all the objects and tools necessary to use the Qwak Platform\n',
    'author': 'Qwak',
    'author_email': 'info@qwak.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.12',
}


setup(**setup_kwargs)
