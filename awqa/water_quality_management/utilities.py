from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
import datetime

from django.views import View
import pytz
from tz_detect.utils import offset_to_timezone
from django.utils.timezone import now

from .models import Aquarium, FreshWaterParameterLogEntry
import pandas as pd
import plotly.graph_objects as go
from decimal import Decimal
from django.conf import settings
from openai import OpenAI

OPENAI_API_KEY = settings.OPENAI_API_KEY


class ChartFactory(View):

    def get(self, request, **kwargs):

        # Get query parameters with default values
        query = kwargs.get('days', 15)
        pk = kwargs.get('pk')

        start_date = now() - timedelta(days=int(query))
        aquarium = get_object_or_404(Aquarium, pk=pk)

        # Filter log entries
        queryset = aquarium.freshwaterparameterlogentry_set.filter(date_created__range=(start_date, now()))
        if queryset.count() <= 1:
            return HttpResponse(
                '''
                <sl-alert open variant="warning" style="margin: 1em;">
                    <sl-icon slot="icon" name="info-circle"></sl-icon>
                    <b><p>At least two log entries are required to generate a chart.</p></b>
                </sl-alert>
                '''
            )

        # Convert queryset to DataFrame
        data = list(queryset.values())
        tz = request.session.get("detected_tz", "UTC")
        new_tz = pytz.timezone(tz)

        data_frame = pd.DataFrame(data)
        data_frame['date_created'] = pd.to_datetime(data_frame['date_created']).dt.tz_convert(new_tz)
        
        # Process columns and remove invalid entries
        numeric_columns = ['ph', 'high_range_ph', 'ammonia', 'nitrite', 'nitrate']
        for column in numeric_columns:
            data_frame[column] = pd.to_numeric(data_frame[column], errors='coerce')

        # Helper function to add chart traces
        def add_trace(df, column, name, unit=""):
            if column in df.columns and df[column].notna().sum() > 0:
                chart.add_trace(
                    go.Scatter(
                        x=df['date_created'], 
                        y=df[column], 
                        name=f"{name} {unit}".strip(),
                        mode="lines+markers",
                        hovertemplate=(
                            "<b>%{x|%b %d, %Y}</b><br><b>%{x|%I:%M %p}</b><br><br>"
                            f"<b>{name}: </b>%{{y}} {unit}".strip()
                        )
                    )
                )

        chart = go.Figure()

        # Add traces for each parameter
        add_trace(data_frame, 'ph', "pH")
        add_trace(data_frame, 'high_range_ph', "High Range pH")
        add_trace(data_frame, 'ammonia', "Ammonia", "ppm")
        add_trace(data_frame, 'nitrite', "Nitrite", "ppm")
        add_trace(data_frame, 'nitrate', "Nitrate", "ppm")

        chart.update_layout(
            autosize=True,
            xaxis_title='Date Created',
            hoverlabel=dict(bgcolor="lightgray", font_size=15),
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
        return HttpResponse(chart_contents)


client = OpenAI(api_key=OPENAI_API_KEY)

class OpenAITankCareSuggestionsFactory(View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        log_entry = FreshWaterParameterLogEntry.objects.get(pk=pk)

        ph = f"pH: {log_entry.ph}" if log_entry.ph != 'N/A' else "pH data is unavailable"
        high_range_ph = f"high range pH: {log_entry.high_range_ph}" if log_entry.high_range_ph != 'N/A' else "high range pH data is unavailable"
        ammonia = f"ammonia: {log_entry.ammonia}" if log_entry.ammonia != 'N/A' else "ammonia data is unavailable"
        nitrite = f"nitrite: {log_entry.nitrite}" if log_entry.nitrite != 'N/A' else "nitrite data is unavailable"
        nitrate = f"nitrate: {log_entry.nitrate}" if log_entry.nitrate != 'N/A' else "nitrate data is unavailable"
        notes = f"notes: {log_entry.notes}" if log_entry.notes else "notes are unavailable"

        prompt = f"""
            Provide care suggestions for an aquarium with the following details:
            {ph},
            {high_range_ph},
            {ammonia}ppm,
            {nitrite}ppm,
            {nitrate}ppm,
            {notes}.
            Only provide a short paragraph of immediate actions that can be taken. Do not make it in list format, and the response ready to be submitted to a textarea.
            If paramaters look normal provide loger term care suggestions instead of immediate actions.
            If no parameters are given, only suggest to record them in the future.
        """

        openai_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                    {"role": "system", "content": "You are an expert aquarium care assistant."},
                    {"role": "user", "content": prompt}
                ],
            temperature=0.7,
            max_tokens=200
        )

        suggestions = openai_response.choices[0].message.content.strip()
        log_entry.ai_suggestions = suggestions
        log_entry.openai_token_available = False
        log_entry.date_ai_suggestion_created = timezone.now()
        log_entry.save(update_fields=['ai_suggestions', 'openai_token_available', 'date_ai_suggestion_created'])

        response = f"<p style='text-indent: 25px;'>{log_entry.ai_suggestions}</p>"
        return HttpResponse(response)