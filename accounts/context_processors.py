# Author : Parham Golmohammadi

def user_role(request):
    if request.user.is_authenticated:
        prof = getattr(request.user, 'profile', None)
        role = prof.role if prof else 'Anonymous'
    else:
        role = None
    return {
        'user_role': role,
        'voting_roles': ['Engineer', 'Team Leader'],
        'trends_roles': ['Team Leader', 'Department Leader', 'Senior Manager'],
    }
