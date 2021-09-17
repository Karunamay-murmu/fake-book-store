from category.models import Category

def categories(request):
    return {
        'categories': Category.objects.select_related('parent').filter(is_active=True)
    }