from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from .models import Post, User, Friends, Reaction, Comment, REACTION_CHOICES
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('profile')
        return super(SignupView, self).get(*args, **kwargs)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return redirect('login')


def logut_user(request):
    logout(request)
    return redirect('login')


def _get_user_reactions(posts, user):
    reactions = Reaction.objects.filter(post__in=posts, user=user)
    return {r.post_id: r.reaction_type for r in reactions}


@method_decorator(login_required(login_url='login'), name='dispatch')
class Profile(ListView):
    model = Post
    template_name = 'profile.html'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_reactions'] = _get_user_reactions(context['object_list'], self.request.user)
        context['show_user'] = False
        context['reaction_choices'] = REACTION_CHOICES
        context['is_own_profile'] = True
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class AccountSettingsView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'profile_pic', 'bio']
    template_name = 'account_settings.html'
    success_url = '/profile/'

    def get_object(self, queryset=None):
        return self.request.user


@method_decorator(login_required(login_url='login'), name='dispatch')
class CreatePost(CreateView):
    model = Post
    fields = ['caption', 'image']
    template_name = 'new_post.html'
    success_url = '/profile/'

    def form_valid(self, form):
        if not form.instance.caption and not self.request.FILES.get('image'):
            form.add_error(None, 'Please add a caption or an image.')
            return self.form_invalid(form)
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class FriendProfile(ListView):
    model = Post
    template_name = 'friend-profile.html'
    paginate_by = 4

    def get(self, *args, **kwargs):
        friend_username = self.kwargs['username']
        if friend_username == self.request.user.username:
            return redirect('profile')
        return super(FriendProfile, self).get(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        friend_username = self.kwargs['username']
        friend = User.objects.get(username=friend_username)
        context['friend'] = friend
        context['is_following'] = self.request.user.is_following(friend)
        context['user_reactions'] = _get_user_reactions(context['object_list'], self.request.user)
        context['show_user'] = False
        context['reaction_choices'] = REACTION_CHOICES
        context['profile_user'] = friend
        context['is_own_profile'] = False
        return context

    def get_queryset(self):
        friend_username = self.kwargs['username']
        friend = User.objects.get(username=friend_username)
        return Post.objects.filter(user=friend).order_by('-date_created')


@method_decorator(login_required(login_url='login'), name='dispatch')
class SearchResults(ListView):
    model = User
    template_name = 'search-results.html'
    paginate_by = 4

    def get_queryset(self):
        search_term = self.request.GET.get('search-term', '')
        return User.objects.filter(username__icontains=search_term).order_by('username')


@login_required(login_url='login')
def follow_user(request, id):
    user_B = get_object_or_404(User, id=id)
    Friends.objects.get_or_create(user_A=request.user, user_B=user_B)
    return redirect('/user/' + user_B.username)


@login_required(login_url='login')
def unfollow_user(request, id):
    user_B = get_object_or_404(User, id=id)
    Friends.objects.filter(user_A=request.user, user_B=user_B).delete()
    return redirect('/user/' + user_B.username)


@method_decorator(login_required(login_url='login'), name='dispatch')
class HomePage(ListView):
    model = Post
    template_name = 'homepage.html'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.all().order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_reactions'] = _get_user_reactions(context['object_list'], self.request.user)
        context['show_user'] = True
        context['reaction_choices'] = REACTION_CHOICES
        context['is_own_profile'] = False
        return context


@login_required(login_url='login')
def react_to_post(request, post_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    post = get_object_or_404(Post, id=post_id)
    reaction_type = request.POST.get('reaction_type')

    valid_types = ['like', 'love', 'haha', 'wow', 'sad']
    if reaction_type not in valid_types:
        return JsonResponse({'error': 'Invalid reaction'}, status=400)

    existing = Reaction.objects.filter(post=post, user=request.user).first()
    if existing:
        if existing.reaction_type == reaction_type:
            existing.delete()
            user_reaction = None
        else:
            existing.reaction_type = reaction_type
            existing.save()
            user_reaction = reaction_type
    else:
        Reaction.objects.create(post=post, user=request.user, reaction_type=reaction_type)
        user_reaction = reaction_type

    counts = {}
    for r in Reaction.objects.filter(post=post):
        counts[r.reaction_type] = counts.get(r.reaction_type, 0) + 1

    emoji_map = {'like': '👍', 'love': '❤️', 'haha': '😂', 'wow': '😮', 'sad': '😢'}
    top_reactions = [emoji_map[r] for r, _ in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:3]]

    return JsonResponse({
        'success': True,
        'counts': counts,
        'user_reaction': user_reaction,
        'total': sum(counts.values()),
        'top_reactions': top_reactions,
    })


@login_required(login_url='login')
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        text = request.POST.get('text', '').strip()
        parent_id = request.POST.get('parent_id')
        if text:
            parent = None
            if parent_id:
                parent = Comment.objects.filter(id=parent_id, post=post).first()
            Comment.objects.create(post=post, user=request.user, text=text, parent=parent)
    return redirect(request.META.get('HTTP_REFERER', '/home/'))


@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user or comment.post.user == request.user:
        comment.delete()
    return redirect(request.META.get('HTTP_REFERER', '/home/'))


