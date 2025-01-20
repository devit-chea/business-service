
import ast
import operator

from rest_framework import (serializers, viewsets, filters)
from functools import reduce
from django.db.models import Q
from currency.utils.currency_utils import operator_value
from ..models.abstracts.history import AbstractRootHistory


def filter_revision_if_need(queryset):
    if issubclass(queryset.model, AbstractRootHistory):
        return queryset.filter(active_revision=True)

    return queryset


class FilterFields(filters.BaseFilterBackend):
    """global filter backend with model fields"""

    def filter_queryset(self, request, queryset, view):
        _queryset = queryset
        q_params = request.query_params
        build_in_params = [
            "page",
            "page_size",
            "search",
            "ordering",
            "isSortAsc",
            "sortBy",
            "scopes",
        ]
        new_exp = []

        try:
            if view.model and q_params and isinstance(q_params, dict):
                param_dict = dict(q_params.copy())
                for param_key, param_values in param_dict.items():
                    if param_key in build_in_params:
                        continue

                    if param_values is None:
                        continue

                    self._param_values(
                        param_values, param_key, queryset, new_exp)

                if new_exp:
                    ex = reduce(operator.and_, new_exp)
                    queryset = queryset.filter(ex)

        except Exception:
            return filter_revision_if_need(_queryset)
        return filter_revision_if_need(queryset)

    def _param_values(self, param_values, param_key, queryset, new_exp):
        param_list = param_values if isinstance(
            param_values, list) else [param_values]
        for param_value in param_list:
            try:
                value, expression = operator_value(param_value)

                expr = self._get_search_expression(
                    expression, value, param_key)

                if self._is_filterable(queryset, expr):
                    new_exp.append(expr)

            except Exception:
                pass

    def _is_filterable(self, queryset, exp):
        """ try to filter the expression before load them in to main query"""
        try:
            queryset.filter(exp).first()
            return True
        except Exception:
            return False

    def _get_search_expression(self, expression, value, search_field):
        expr = ""
        match expression:
            case "like":
                expression = "icontains"
                expr = self.get_condition(search_field, expression, value)
            case "equal":
                expr = self.get_condition(
                    search_field, expression, value, False)
            case "lte":
                expr = self.get_condition(
                    search_field, expression, value, False)
            case "gte":
                expr = self.get_condition(
                    search_field, expression, value, False)
            case "lt":
                expr = self.get_condition(
                    search_field, expression, value, False)
            case "gt":
                expr = self.get_condition(
                    search_field, expression, value, False)
            case "not_equal":
                expr = self.get_condition(
                    search_field, expression, value, True)
            case "is_set":
                expression = "isnull"
                expr = self.get_condition(search_field, expression, False)
            case "is_not_set":
                expression = "isnull"
                expr = self.get_condition(search_field, expression, True)
            case "not_like":
                expression = "icontains"
                expr = self.get_condition(
                    search_field, expression, value, is_not=True)
            case "in":
                expression = "in"
                value = ast.literal_eval(value)
                expr = self.get_condition(
                    search_field, expression, value, is_not=False)
            case "not_in":
                expression = "in"
                value = ast.literal_eval(value)
                expr = self.get_condition(
                    search_field, expression, value, is_not=True)
            case _:
                expr = self.get_condition(search_field, "icontains", value)
        return expr

    def get_condition(self, search_field, expression, value, is_not=False):
        new_expression = f"__{expression}"

        if expression == "equal" or expression == "not_equal":
            new_expression = ""

        condition = Q(**{f"{search_field}{new_expression}": value})
        if is_not:
            condition = ~condition
        return condition


class CurrencyApiView(viewsets.ModelViewSet):
    filter_backends = [FilterFields]

    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    # def perform_create(self, serializer):
    #     model = serializer.context.get("view").model
    #     # set current company
    #     if model != User and hasattr(model, "company"):
    #         serializer.validated_data[
    #             "company"
    #         ] = self.request.user.base_company

    #     # set current created user
    #     if hasattr(model, "create_uid"):
    #         serializer.validated_data["create_uid"] = self.request.user.id

    #     # save data
    #     serializer.save()

    # def perform_update(self, serializer):
    #     _employee = get_current_employee(
    #         self.request.user.pk, self.request.user.base_company)
    #     _check_workflow_status(serializer, _employee)

    #     model = serializer.context.get("view").model
    #     # set current updated user
    #     if hasattr(model, "write_uid"):
    #         serializer.validated_data["write_uid"] = self.request.user.id
    #     # save data
    #     serializer.save()
