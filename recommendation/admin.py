from django.contrib import admin
from .models import Crop, RecommendationResult

admin.site.register(Crop)
admin.site.register(RecommendationResult)