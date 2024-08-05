from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User

class User(AbstractUser):
    is_farmer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        related_name='recommendation_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='recommendation_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

class Crop(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Knowledge(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class KnowledgeRule(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)

    def __str__(self):
        return f'Knowledge Rule for {self.crop.name}'

class KnowledgeRuleDetail(models.Model):
    knowledge_rule = models.ForeignKey(KnowledgeRule, related_name='details', on_delete=models.CASCADE)
    knowledge = models.ForeignKey(Knowledge, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return f'{self.knowledge.name} - {self.value}'

class KnowledgeFuzzyValue(models.Model):
    FUZZY_SET_TYPE_CHOICES = [
        ('Triangular', 'Triangular'),
        ('Trapezoidal', 'Trapezoidal'),
        ('Left Shoulder', 'Left Shoulder'),
        ('Right Shoulder', 'Right Shoulder')
    ]
    
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, default=1)
    knowledge = models.ForeignKey(Knowledge, on_delete=models.CASCADE, default=1)
    fuzzy_set_type = models.CharField(max_length=100, choices=FUZZY_SET_TYPE_CHOICES)
    x1 = models.FloatField()
    x2 = models.FloatField(null=True, blank=True)
    x3 = models.FloatField(null=True, blank=True)
    x4 = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.crop.name} - {self.knowledge} - {self.fuzzy_set_type}'
    
    def get_fuzzy_value(self, input_value):
        if self.fuzzy_set_type == 'Triangular':
            if self.x1 <= input_value <= self.x2:
                return (input_value - self.x1) / (self.x2 - self.x1)
            elif self.x2 <= input_value <= self.x3:
                return (self.x3 - input_value) / (self.x3 - self.x2)
        elif self.fuzzy_set_type == 'Trapezoidal':
            if self.x1 <= input_value <= self.x2:
                return (input_value - self.x1) / (self.x2 - self.x1)
            elif self.x2 <= input_value <= self.x3:
                return 1
            elif self.x3 <= input_value <= self.x4:
                return (self.x4 - input_value) / (self.x4 - self.x3)
        elif self.fuzzy_set_type == 'Left Shoulder':
            if input_value <= self.x1:
                return 0
            elif self.x1 < input_value <= self.x2:
                return (input_value - self.x1) / (self.x2 - self.x1)
            elif input_value > self.x2:
                return 1
        elif self.fuzzy_set_type == 'Right Shoulder':
            if input_value >= self.x2:
                return 0
            elif self.x1 <= input_value < self.x2:
                return (self.x2 - input_value) / (self.x2 - self.x1)
            elif input_value < self.x1:
                return 1
        return 0

    
class RecommendationResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    recommended_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Recommendation for {self.user.username} - {self.crop.name}'