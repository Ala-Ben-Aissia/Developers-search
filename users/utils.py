from django.db.models import Q
from .models import Profile, Skill
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def searchProfiles(request):
    search_query = ''
    if request.GET.get('search_query'): # request.GET --> dict(k, v) where k='search_query' 
        # and v is the value typed in the search bar(v is the search query variable)  
        search_query = request.GET.get('search_query')
    skills = Skill.objects.filter(name__icontains=search_query)   
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
    )
    # profiles -> parent, skills -> child
    return profiles, search_query

def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)  # profiles = <page {{page}} of {{paginator.num_pages}}>
        print(profiles)
    left_index = int(page) - 4        # 5 > 4 : we always subtract 1 from the right_index, range(1, 5) -> 1, 2, 3 ,4
    if left_index < 1:
        left_index = 1
    right_index = int(page) + 5
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
    custom_range = range(left_index, right_index)
    return profiles, custom_range