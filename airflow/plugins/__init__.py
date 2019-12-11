# from __future__ import division, absolute_import, print_function

from airflow.plugins_manager import AirflowPlugin

import operators

import helpers


class ETLPlugin(AirflowPlugin):
    name = "etl_plugin"
    operators = [
        operators.StageToRedshiftOperator,
        operators.LoadTableOperator,
        operators.DataQualityOperator,
    ]
    helpers = [helpers.SqlQueries, helpers.DataValidationQueries]
