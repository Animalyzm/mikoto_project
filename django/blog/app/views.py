from django.views import generic

from .models import Post


class IndexView(generic.ListView):
    model = Post


class DetailView(generic.DetailView):
    model = Post
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.page_views += 1
        self.object.save() 
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
    
class CategoryView(generic.ListView):
    model = Post
    