from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, UserProfileForm, CropForm, KnowledgeForm, KnowledgeRuleForm, KnowledgeFuzzyValueForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Crop, Knowledge, KnowledgeRule, KnowledgeFuzzyValue, KnowledgeRuleDetail, RecommendationResult
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from math import log10
from django.conf import settings

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data['user_type']
            security_key = form.cleaned_data['security_key']

            if user_type == 'admin':
                if security_key != settings.SECURITY_KEY:
                    form.add_error('security_key', 'Invalid security key for admin account.')
                    return render(request, 'recommendation/register.html', {'form': form})
                user.is_superuser = True
                user.is_staff = True
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'recommendation/register.html', {'form': form})

def home(request):
    return HttpResponse("Welcome to the Crop Recommendation System")

def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        else:
            return redirect('crop_recommendation')
    return render(request, 'recommendation/index.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'recommendation/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'recommendation/profile.html', {'form': form})

@login_required
def crop_list(request):
    crops = Crop.objects.all()
    return render(request, 'recommendation/crop_list.html', {'crops': crops})

@login_required
def crop_create(request):
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crop_list')
    else:
        form = CropForm()
    return render(request, 'recommendation/crop_form.html', {'form': form})

@login_required
def crop_update(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    if request.method == 'POST':
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            return redirect('crop_list')
    else:
        form = CropForm(instance=crop)
    return render(request, 'recommendation/crop_form.html', {'form': form})

@login_required
def crop_delete(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    if request.method == 'POST':
        crop.delete()
        return redirect('crop_list')
    return render(request, 'recommendation/crop_confirm_delete.html', {'crop': crop})

@staff_member_required
def knowledge_list(request):
    knowledges = Knowledge.objects.all()
    return render(request, 'recommendation/knowledge_list.html', {'knowledges': knowledges})

@staff_member_required
def knowledge_create(request):
    if request.method == 'POST':
        form = KnowledgeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('knowledge_list')
    else:
        form = KnowledgeForm()
    return render(request, 'recommendation/knowledge_form.html', {'form': form})

@staff_member_required
def knowledge_update(request, pk):
    knowledge = get_object_or_404(Knowledge, pk=pk)
    if request.method == 'POST':
        form = KnowledgeForm(request.POST, instance=knowledge)
        if form.is_valid():
            form.save()
            return redirect('knowledge_list')
    else:
        form = KnowledgeForm(instance=knowledge)
    return render(request, 'recommendation/knowledge_form.html', {'form': form})

@staff_member_required
def knowledge_delete(request, pk):
    knowledge = get_object_or_404(Knowledge, pk=pk)
    if request.method == 'POST':
        knowledge.delete()
        return redirect('knowledge_list')
    return render(request, 'recommendation/knowledge_confirm_delete.html', {'knowledge': knowledge})

@staff_member_required
def knowledge_rule_list(request):
    knowledge_rules = KnowledgeRule.objects.all()
    return render(request, 'recommendation/knowledge_rule_list.html', {'knowledge_rules': knowledge_rules})

@staff_member_required
def knowledge_rule_create(request):
    if request.method == 'POST':
        form = KnowledgeRuleForm(request.POST)
        if form.is_valid():
            knowledge_rule = form.save()
            # Create KnowledgeRuleDetail for each selected knowledge
            for knowledge in form.cleaned_data['knowledges']:
                KnowledgeRuleDetail.objects.create(
                    knowledge_rule=knowledge_rule,
                    knowledge=knowledge,
                    value=0.0  # Set a default value or handle it accordingly
                )
            return redirect('knowledge_rule_list')  # Change to your desired redirect page
    else:
        form = KnowledgeRuleForm()
    return render(request, 'recommendation/knowledge_rule_form.html', {'form': form})

@staff_member_required
def knowledge_rule_update(request, pk):
    knowledge_rule = get_object_or_404(KnowledgeRule, pk=pk)
    if request.method == 'POST':
        form = KnowledgeRuleForm(request.POST, instance=knowledge_rule)
        if form.is_valid():
            knowledge_rule = form.save()
            # Update KnowledgeRuleDetail
            knowledge_rule.details.all().delete()  # Clear existing details
            for knowledge in form.cleaned_data['knowledges']:
                KnowledgeRuleDetail.objects.create(
                    knowledge_rule=knowledge_rule,
                    knowledge=knowledge,
                    value=0.0  # Set a default value or handle it accordingly
                )
            return redirect('knowledge_rule_list')  # Change to your desired redirect page
    else:
        form = KnowledgeRuleForm(instance=knowledge_rule)
    return render(request, 'recommendation/knowledge_rule_form.html', {'form': form})

@staff_member_required
def knowledge_rule_delete(request, pk):
    knowledge_rule = get_object_or_404(KnowledgeRule, pk=pk)
    if request.method == 'POST':
        knowledge_rule.delete()
        return redirect('knowledge_rule_list')
    return render(request, 'recommendation/knowledge_rule_confirm_delete.html', {'knowledge_rule': knowledge_rule})

@staff_member_required
def knowledge_fuzzy_value_list(request):
    knowledge_fuzzy_values = KnowledgeFuzzyValue.objects.all()
    return render(request, 'recommendation/knowledge_fuzzy_value_list.html', {'knowledge_fuzzy_values': knowledge_fuzzy_values})

@staff_member_required
def knowledge_fuzzy_value_create(request):
    if request.method == 'POST':
        form = KnowledgeFuzzyValueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('knowledge_fuzzy_value_list')  # Change to your list view
    else:
        form = KnowledgeFuzzyValueForm()
    return render(request, 'recommendation/knowledge_fuzzy_value_form.html', {'form': form})

@staff_member_required
def knowledge_fuzzy_value_update(request, pk):
    knowledge_fuzzy_value = get_object_or_404(KnowledgeFuzzyValue, pk=pk)
    if request.method == 'POST':
        form = KnowledgeFuzzyValueForm(request.POST, instance=knowledge_fuzzy_value)
        if form.is_valid():
            form.save()
            return redirect('knowledge_fuzzy_value_list')
    else:
        form = KnowledgeFuzzyValueForm(instance=knowledge_fuzzy_value)
    return render(request, 'recommendation/knowledge_fuzzy_value_form.html', {'form': form})

@staff_member_required
def knowledge_fuzzy_value_delete(request, pk):
    knowledge_fuzzy_value = get_object_or_404(KnowledgeFuzzyValue, pk=pk)
    if request.method == 'POST':
        knowledge_fuzzy_value.delete()
        return redirect('knowledge_fuzzy_value_list')
    return render(request, 'recommendation/knowledge_fuzzy_value_confirm_delete.html', {'knowledge_fuzzy_value': knowledge_fuzzy_value})

@login_required
def crop_recommendation(request):
    if request.method == 'POST':
        knowledge_values = {}
        knowledges_entered = {}
        
        # Collecte des valeurs renseignées par l'utilisateur
        for knowledge in Knowledge.objects.all():
            value = request.POST.get(knowledge.name, None)
            if value:
                knowledge_values[knowledge.name] = float(value)
                knowledges_entered[knowledge.name] = True  # Connaissance renseignée
            else:
                knowledge_values[knowledge.name] = None  # Connaissance non renseignée
                knowledges_entered[knowledge.name] = False

        fuzzy_scores = {}
        # Calcul des scores flous pour chaque culture
        for fuzzy_value in KnowledgeFuzzyValue.objects.all():
            knowledge_name = fuzzy_value.knowledge.name
            crop_name = fuzzy_value.crop.name
            knowledge_value = knowledge_values.get(knowledge_name, None)

            if knowledge_value is None:
                percentage = 1  # Valeur par défaut si non renseignée
            else:
                percentage = fuzzy_value.get_fuzzy_value(knowledge_value)

            if crop_name not in fuzzy_scores:
                fuzzy_scores[crop_name] = []
            fuzzy_scores[crop_name].append((percentage, knowledge_name))

        recommendation_scores = {}
        for crop, scores in fuzzy_scores.items():
            combined_score = 1
            num_knowledges_used = 0
            for score, knowledge_name in scores:
                combined_score *= score
                if knowledges_entered[knowledge_name]:  # Vérifier si la connaissance a été renseignée
                    num_knowledges_used += 1

            # Si aucune connaissance n'a été renseignée pour cette culture, le score doit être 0
            if num_knowledges_used == 0:
                combined_score = 0
            else:
                combined_score **= (1 / num_knowledges_used)

            recommendation_scores[crop] = combined_score

        # Vérification des règles de connaissance
        for crop in Crop.objects.all():
            if crop.name not in recommendation_scores:
                recommendation_scores[crop.name] = 0
            else:
                knowledge_rule = KnowledgeRule.objects.filter(crop=crop).first()
                if knowledge_rule:
                    rule_knowledges = knowledge_rule.details.values_list('knowledge__name', flat=True)
                    if not any(knowledge_values.get(knowledge_name, None) is not None for knowledge_name in rule_knowledges):
                        recommendation_scores[crop.name] = 0

        sorted_recommendations = sorted(recommendation_scores.items(), key=lambda x: x[1], reverse=True)
        top_recommendations = sorted_recommendations[:5]
        recommended_crop, recommended_score = top_recommendations[0] if top_recommendations else (None, None)

        # Supprimer les anciens résultats de recommandation de l'utilisateur
        RecommendationResult.objects.filter(user=request.user).delete()

        # Stocker le nouveau résultat de recommandation
        if recommended_crop:
            RecommendationResult.objects.create(user=request.user, crop=Crop.objects.get(name=recommended_crop))

        return render(request, 'recommendation/recommendation_result.html', {
            'recommended_crop': recommended_crop,
            'recommended_score': recommended_score,
            'top_recommendations': top_recommendations
        })
    else:
        knowledges = Knowledge.objects.exclude(name='Default Knowledge')
        return render(request, 'recommendation/crop_recommendation_form.html', {'knowledges': knowledges})


def is_admin(user):
    return user.is_superuser

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('index')

    crops = Crop.objects.all()
    knowledges = Knowledge.objects.all()
    knowledge_rules = KnowledgeRule.objects.all()
    knowledge_fuzzy_values = KnowledgeFuzzyValue.objects.all()

    context = {
        'crops': crops,
        'knowledges': knowledges,
        'knowledge_rules': knowledge_rules,
        'knowledge_fuzzy_values': knowledge_fuzzy_values,
        'crop_form': CropForm(),
        'knowledge_form': KnowledgeForm(),
        'knowledge_rule_form': KnowledgeRuleForm(),
        'knowledge_fuzzy_value_form': KnowledgeFuzzyValueForm(),
    }
    return render(request, 'recommendation/admin_dashboard.html', context)