from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from .forms import CommentCreateForm
from .models import Post, Comment


class IndexView(generic.ListView):
    model = Post
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.order_by('-created_at')  # 降順
        keyword = self.request.GET.get('keyword')  # 検索入力キーワード
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(content__icontains=keyword)
            )  # icontains: 部分一致、大小文字区別なし
        return queryset


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
    paginate_by = 5

    def get_queryset(self):
        category_pk = self.kwargs['category_pk']
        queryset = Post.objects.order_by('-created_at').filter(category__pk=category_pk)
        return queryset


class CommentView(generic.CreateView):
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):
        post_pk = self.kwargs['post_pk']
        comment = form.save(commit=False)
        comment.post = get_object_or_404(Post, pk=post_pk)
        comment.save()  # DBに保存
        return redirect('app:detail', pk=post_pk)
