#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from ibm_watson_machine_learning.foundation_models.inference import ModelInference
from ibm_watsonx_ai.utils.change_methods_docstring import change_docstrings


@change_docstrings
class ModelInference(ModelInference):
    """Instantiate the model interface.

    .. hint::
        To use the ModelInference class with LangChain, use the :func:`WatsonxLLM <ibm_watsonx_ai.foundation_models.extensions.langchain.WatsonxLLM>` wrapper.

    :param model_id: the type of model to use
    :type model_id: str, optional

    :param deployment_id: ID of tuned model's deployment
    :type deployment_id: str, optional

    :param credentials: credentials to Watson Machine Learning instance
    :type credentials: dict, optional

    :param params: parameters to use during generate requests
    :type params: dict, optional

    :param project_id: ID of the Watson Studio project
    :type project_id: str, optional

    :param space_id: ID of the Watson Studio space
    :type space_id: str, optional

    :param verify: user can pass as verify one of following:

        - the path to a CA_BUNDLE file
        - the path of directory with certificates of trusted CAs
        - `True` - default path to truststore will be taken
        - `False` - no verification will be made
    :type verify: bool or str, optional

    :param api_client: Initialized APIClient object with set project or space ID. If passed, ``credentials`` and ``project_id``/``space_id`` are not required.
    :type api_client: APIClient, optional

    .. note::
        One of these parameters is required: [``model_id``, ``deployment_id``]

    .. note::
        One of these parameters is required: [``project_id``, ``space_id``] when ``credentials`` parameter passed.

    .. hint::
        You can copy the project_id from Project's Manage tab (Project -> Manage -> General -> Details).

    **Example**

    .. code-block:: python

        from ibm_watsonx_ai.foundation_models import ModelInference
        from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
        from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes, DecodingMethods

        # To display example params enter
        GenParams().get_example_values()

        generate_params = {
            GenParams.MAX_NEW_TOKENS: 25
        }

        model_inference = ModelInference(
            model_id=ModelTypes.FLAN_UL2,
            params=generate_params,
            credentials={
                "apikey": "***",
                "url": "https://us-south.ml.cloud.ibm.com"
            },
            project_id="*****"
            )

    .. code-block:: python

        from ibm_watsonx_ai.foundation_models import ModelInference

        deployment_inference = ModelInference(
            deployment_id="<ID of deployed model>",
            credentials={
                "apikey": "***",
                "url": "https://us-south.ml.cloud.ibm.com"
            },
            project_id="*****"
            )

    """
    pass
