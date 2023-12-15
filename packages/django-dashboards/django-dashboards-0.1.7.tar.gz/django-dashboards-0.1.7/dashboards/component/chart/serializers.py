import json
from typing import Any, Dict, List, Optional, Type

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model
from django.template.loader import render_to_string

import asset_definitions
import pandas as pd
import plotly.graph_objs as go

from dashboards.meta import ClassWithMeta


class ModelDataMixin:
    """
    gets data from a django model and converts to a pandas dataframe
    """

    class Meta:
        fields: Optional[List[str]] = None
        model: Optional[Model] = None

    _meta: Type["ModelDataMixin.Meta"]

    def get_fields(self) -> Optional[List[str]]:
        # TODO: for some reason mypy complains about this one line
        return self._meta.fields  # type: ignore

    def convert_to_df(self, data: Any, columns: Optional[List] = None) -> pd.DataFrame:
        return pd.DataFrame(data, columns=columns)

    def get_data(self, *args, **kwargs) -> pd.DataFrame:
        fields = self.get_fields()
        queryset = self.get_queryset(*args, **kwargs)
        if fields:
            queryset = queryset.values(*fields)

        try:
            df = self.convert_to_df(queryset.iterator(), fields)
        except KeyError:
            return pd.DataFrame()
        return df

    def get_queryset(self, *args, **kwargs):
        if self._meta.model is not None:
            queryset = self._meta.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(self)s is missing a QuerySet. Define "
                "%(self)s.model or override "
                "%(self)s.get_queryset()." % {"self": self.__class__.__name__}
            )

        return queryset


class PlotlyChartSerializerMixin:
    template_name: str = "dashboards/components/chart/plotly.html"
    meta_layout_attrs = ["title", "width", "height"]
    layout: Optional[Dict[str, Any]] = None

    _meta: Type[Any]

    class Meta:
        displayModeBar: Optional[bool] = True
        staticPlot: Optional[bool] = False
        responsive: Optional[bool] = True

    def empty_chart(self) -> str:
        return json.dumps(
            {
                "layout": {
                    "xaxis": {"visible": False},
                    "yaxis": {"visible": False},
                    "annotations": [
                        {
                            "text": f"{self._meta.verbose_name} - No data",
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                            "font": {"size": 28},
                        }
                    ],
                }
            }
        )

    def apply_layout(self, fig: go.Figure, dark=False) -> go.Figure:
        layout = self.layout or {}

        for attr in self.meta_layout_attrs:
            layout.setdefault(attr, getattr(self._meta, attr))

        if dark:
            fig = fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0.05)",
                paper_bgcolor="rgba(0,0,0,0.05)",
            )

        return fig.update_layout(**layout)

    def get_data(self, *args, **kwargs) -> pd.DataFrame:
        raise NotImplementedError

    def to_fig(self, data: Any) -> go.Figure:
        raise NotImplementedError

    @classmethod
    def serialize(cls, **kwargs) -> str:
        self = cls()
        request = kwargs.get("request")
        df = self.get_data(**kwargs)

        if isinstance(df, pd.DataFrame) and df.empty:
            return self.empty_chart()

        fig = self.to_fig(df)
        fig = self.apply_layout(
            fig, dark=request and request.COOKIES.get("appearanceMode") == "dark"
        )

        return fig.to_json()

    @classmethod
    def render(cls, template_id, **kwargs) -> str:
        self = cls()
        value = cls.serialize(**kwargs)
        context = {
            "template_id": template_id,
            "value": value,
            "displayModeBar": self._meta.displayModeBar,
            "staticPlot": self._meta.staticPlot,
            "responsive": self._meta.responsive,
        }
        return render_to_string(cls.template_name, context)


class BaseChartSerializer(ClassWithMeta, asset_definitions.MediaDefiningClass):
    _meta: Type[Any]

    class Meta:
        title: Optional[str] = None
        width: Optional[int] = None
        height: Optional[int] = None

    @classmethod
    def preprocess_meta(cls, current_class_meta):
        title = getattr(current_class_meta, "title", None)

        if title and not hasattr(current_class_meta, "name"):
            current_class_meta.name = title

        if title and not hasattr(current_class_meta, "verbose_name"):
            current_class_meta.verbose_name = title

        return current_class_meta

    @classmethod
    def postprocess_meta(cls, current_class_meta, resolved_meta_class):
        if not hasattr(resolved_meta_class, "title"):
            resolved_meta_class.title = resolved_meta_class.verbose_name

        return resolved_meta_class

    @classmethod
    def serialize(cls, **kwargs) -> str:
        raise NotImplementedError


class PlotlyChartSerializer(PlotlyChartSerializerMixin, BaseChartSerializer):
    """
    Serializer to convert data into a plotly js format
    """

    class Meta(PlotlyChartSerializerMixin.Meta, BaseChartSerializer.Meta):
        pass

    class Media:
        js = ("dashboards/vendor/js/plotly.min.js",)


class ChartSerializer(ModelDataMixin, PlotlyChartSerializer):
    """
    Default chart serializer to read data from a django model
    and serialize it to something plotly js can render
    """

    class Meta(ModelDataMixin.Meta, PlotlyChartSerializer.Meta):
        pass

    _meta: Type["ChartSerializer.Meta"]
