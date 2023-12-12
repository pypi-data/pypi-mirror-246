"""DI Choice String Parameter Type."""
import collections
from typing import Optional, Any

from cmem_plugin_base.dataintegration.context import PluginContext
from cmem_plugin_base.dataintegration.types import StringParameterType, Autocompletion


class ChoiceParameterType(StringParameterType):
    """Choice parameter type."""

    allow_only_autocompleted_values: bool = True

    autocomplete_value_with_labels: bool = True

    choice_list: collections.OrderedDict[str, str]

    def __init__(self, choice_list: collections.OrderedDict[str, str]):
        self.choice_list = choice_list

    def label(
        self, value: str, depend_on_parameter_values: list[Any], context: PluginContext
    ) -> Optional[str]:
        """Returns the label for the given choice value."""
        return self.choice_list[value]

    def autocomplete(
        self,
        query_terms: list[str],
        depend_on_parameter_values: list[Any],
        context: PluginContext,
    ) -> list[Autocompletion]:
        result = []
        for identifier in self.choice_list:
            label = self.choice_list[identifier]
            if len(query_terms) == 0:
                # add any choices to list if no search terms are given
                result.append(Autocompletion(value=identifier, label=label))
            for term in query_terms:
                if term.lower() in label.lower():
                    result.append(Autocompletion(value=identifier, label=label))
        result.sort(key=lambda x: x.label)  # type: ignore
        return list(set(result))
