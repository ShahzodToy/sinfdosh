import datetime

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from hitcount.utils import get_hitcount_model

from friend.models import Friend_Request
from users.forms import EditUserForm
from .forms import EditPostForm, CreatePostForm, CheckPostForm, CommentForm
from .models import Post, Comment
from users.models import CustomUser
from hitcount.views import HitCountMixin, HitCountDetailView


def home(request):
    posts = Post.published.all()
    context = {'posts':posts}
    return render(request,'posts.html',context)





def detail_view(request,slug):
    post = get_object_or_404(Post,slug=slug)
    total_like = post.total_likes()
    comments = post.comment_set.all()
    form = CommentForm(data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            Comment.objects.create(
                post_name=post,
                user=request.user,
                comment = form.cleaned_data['comment'],
            )
            return redirect(reverse('detail_view',kwargs={'slug':post.slug}))

    context = {'post': post,'total_like':total_like,'comments':comments,"form":form,
               'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3]}

    hit_count = get_hitcount_model().objects.get_for_object(post)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_messsage'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    return render(request, 'detail_view.html', context)

class FriendFeedView(View):
    def get(self,request):
        friend_list = CustomUser.objects.exclude(username = request.user)
        alluser = CustomUser.objects.exclude(username=request.user)
        fr = Friend_Request.objects.filter(to_user=request.user)
        return render(request,'post/friend_feed.html',{'friend_list':friend_list,'alluser':alluser,'fr':fr})


class EditPostView(View):
    def get(self,request,id):
        post = Post.objects.get(id=id)
        form = EditPostForm(instance=post)
        return render(request,'post/edit_post.html',{'form':form})
    def post(self,request,id):
        post = Post.objects.get(id=id)
        form = EditPostForm(instance=post,data=request.POST,files = request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'post/edit_post.html', {'form': form})

class DeletePostView(View):
    def post(self,request,id):
        post = Post.objects.get(id=id)
        post.delete()
        messages.info(request,'Post deleted successfully')
        return redirect('home')


class CreateNewPost(View):
    def get(self,request):
        form = CreatePostForm()
        return render(request,'create_post.html',{'form':form})

    def post(self,request):
        form = CreatePostForm(data=request.POST,files = request.FILES)

        if form.is_valid():
            Post.objects.create(
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                picture_content=form.cleaned_data['picture_content'],
                post_tag=form.cleaned_data['post_tag'],
                creator=  request.user,
                section_topic=form.cleaned_data['section_topic'],
            )
            return redirect(reverse('home'))
        return render(request, 'create_post.html', {'form': form})

def LikeView(request,id):
    post=get_object_or_404(Post,id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return redirect(reverse('detail_view', kwargs={'slug': post.slug}))


def ListUnPublishedPost(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request,'post/list_published.html',context)

class Published_check_post(View):
    def get(self,request,id):
        post = Post.objects.get(id=id)
        form = CheckPostForm(instance=post)
        return render(request,'post/published.html',{'form':form,'post':post})


    def post(self,request,id):
        post = Post.objects.get(id=id)
        form = CheckPostForm(instance=post,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('detail_view', kwargs={'slug': post.slug}))
        return render(request,'post/published.html',{'form':form,'post':post})

def trending_weekly(request):
    last_week = datetime.datetime.now() - datetime.timedelta(days=7)
    top = Post.objects.filter(created_at__gte=last_week).order_by('-hit_count_generic__hits')[:3]
    return render(request,'post/weekly_posts.html',{"top_week":top})

def trending_monthly(request):
    last_week = datetime.datetime.now() - datetime.timedelta(days=30)
    top = Post.objects.filter(created_at__gte=last_week).order_by('-hit_count_generic__hits')[:3]
    return render(request,'post/monthly_posts.html',{"top_month":top})



