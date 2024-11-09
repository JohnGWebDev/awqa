from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta

from django.views import View

from .models import Aquarium
import pandas as pd
import plotly.express as pe
import plotly.graph_objects as go
from decimal import Decimal

class ChartFactory(View):

    def get(self, request, **kwargs):
        try:
            query = kwargs.get('days')
        except:
            query = 30
        now = timezone.now()
        start_date = now - timedelta(days=query)
        pk = kwargs.get('pk')
        aquarium = Aquarium.objects.get(pk=pk)
        queryset = aquarium.freshwaterparameterlogentry_set.filter(date_created__range=(start_date, now))

        if queryset:
            # Only show private entries if the current user is the owner.
            if aquarium.user != self.request.user:
                queryset.filter(is_private=False)
            # Use pandas to turn object into dataframe
            data = list(queryset.values())
            data_frame = pd.DataFrame(data)
            
            chart = go.Figure()
            data_frame['ph'] = data_frame['ph'].apply(Decimal)
            chart.add_trace(go.Scatter(x=data_frame['date_created'], y=data_frame['ph'], name="Ph", mode="lines+markers"))
            data_frame['high_range_ph'] = data_frame['high_range_ph'].apply(Decimal)
            chart.add_trace(go.Scatter(x=data_frame['date_created'], y=data_frame['high_range_ph'], name="High Range Ph", mode="lines+markers"))
            data_frame['ammonia'] = data_frame['ammonia'].apply(Decimal)
            chart.add_trace(go.Scatter(x=data_frame['date_created'], y=data_frame['ammonia'], name="Ammonia| ppm", mode="lines+markers"))
            data_frame['nitrate'] = data_frame['nitrate'].apply(Decimal)
            chart.add_trace(go.Scatter(x=data_frame['date_created'], y=data_frame['nitrate'], name="Nitrates| ppm", mode="lines+markers"))
            data_frame['nitrite'] = data_frame['nitrite'].apply(Decimal)
            chart.add_trace(go.Scatter(x=data_frame['date_created'], y=data_frame['nitrite'], name="Nitrites| ppm", mode="lines+markers"))
            chart.update_layout(
                autosize=True,
                xaxis_title='Date Created',
                title=dict(text='Water Quality Chart', font=dict(size=50), x=0.5, y=0.9, yanchor="top", yref='container'),
                margin=dict(l=10, r=10, t=100, b=10),
                title_font=dict(
                    family="Fredoka",
                    size=30,),
                legend=dict(
                    title=dict(text="Parameters", side="top center", font=dict(size=18)),
                    orientation="h",
                    yanchor="bottom",
                    xanchor='center',
                    x=0.5,
                    xref="container",
                    yref="container",
                    bordercolor="grey",
                    borderwidth=2,
                    entrywidth=0.5,
                    entrywidthmode="fraction",)
            )
            chart_contents = '<script src="https://cdn.plot.ly/plotly-2.32.0.min.js" charset="utf-8"></script>' + chart.to_html(full_html=False)
        else:
            chart_contents = '<p>There is currently no data to be displayed.</p>'
        return HttpResponse(chart_contents)