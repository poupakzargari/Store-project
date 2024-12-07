from .models import Category

def categories_context(request):
    # Fetch all categories from the database
    categories = Category.objects.all()
    return {'categories': categories}
