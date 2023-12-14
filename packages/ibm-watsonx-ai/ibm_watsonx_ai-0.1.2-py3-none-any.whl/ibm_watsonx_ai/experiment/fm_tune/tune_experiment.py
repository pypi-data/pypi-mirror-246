#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------


from ibm_watson_machine_learning.experiment.fm_tune.tune_experiment import TuneExperiment
from ibm_watsonx_ai.utils.change_methods_docstring import change_docstrings


@change_docstrings
class TuneExperiment(TuneExperiment):
    """TuneExperiment class for tuning models with prompts.

    :param credentials: credentials to Watson Machine Learning instance
    :type credentials: dict

    :param project_id: ID of the Watson Studio project
    :type project_id: str, optional

    :param space_id: ID of the Watson Studio Space
    :type space_id: str, optional

    :param verify: user can pass as verify one of following:
        - the path to a CA_BUNDLE file
        - the path of directory with certificates of trusted CAs
        - `True` - default path to truststore will be taken
        - `False` - no verification will be made
    :type verify: bool or str, optional

    **Example**
    .. code-block:: python
        from ibm_watsonx_ai.experiment import TuneExperiment
        experiment = TuneExperiment(
            credentials={
                "apikey": "...",
                "iam_apikey_description": "...",
                "iam_apikey_name": "...",
                "iam_role_crn": "...",
                "iam_serviceid_crn": "...",
                "instance_id": "...",
                "url": "https://us-south.ml.cloud.ibm.com"
            },
            project_id="...",
            space_id="...")
    """
    pass
