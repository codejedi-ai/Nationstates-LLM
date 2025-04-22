from django.db import models
import requests
import os


class Gptnation(models.Model):
    NATION = models.CharField(max_length=255)
    X_PASSWORD = models.CharField(max_length=255)
    USERAGENT = models.CharField(max_length=255, default='GPT_USERAGENT')  # Added default value

    def __str__(self):
        return self.NATION

    def get_nation_issues(self):
        url = "https://www.nationstates.net/cgi-bin/api.cgi"
        headers = {
            "X-Password": self.X_PASSWORD,
            "User-Agent": "GreatDictatorAI"  # Corrected User-Agent value
        }
        params = {
            "nation": self.NATION,
            "q": "issues"
        }
        response = requests.get(url, headers=headers, params=params)
        return response.text

    class Meta:
        app_label = 'GreatDictatorAI'  # Change 'GreatDictatorAI' to the name of your Django app
