#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------
import inspect
import sys

import ibm_watson_machine_learning.foundation_models.utils.utils as utils
from ibm_watson_machine_learning.foundation_models.utils.utils import PromptTuningParams, TemplateFormatter

from ibm_watsonx_ai.utils.change_methods_docstring import change_docstrings, copy_func


@change_docstrings
class PromptTuningParams(PromptTuningParams):
    pass

@change_docstrings
class TemplateFormatter(TemplateFormatter):
    pass

attributes = dir(utils)

for attribute in attributes:
    attr = getattr(utils, attribute)
    if callable(attr) and not inspect.isclass(attr)\
          and hasattr(attr, '__globals__'):
        setattr(sys.modules[__name__], attribute, copy_func(getattr(utils, attribute)))