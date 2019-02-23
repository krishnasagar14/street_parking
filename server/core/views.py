from django.shortcuts import render

# Create your views here.

class AppResponse(object):
    def get_data(self, data):
        return {
            'data': data
        }