from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import PhotoForm, MyPasswordChangeForm, UserUpdateForm, ContactForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Photo, Category, Like, Follow
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.shortcuts import redirect, resolve_url
from django.views import generic
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'app/user_detail.html'


class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'app/user_form.html'

    def get_success_url(self):
        return resolve_url('app:user_detail', pk=self.kwargs['pk'])

class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('app:password_change_done')
    template_name = 'app/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'app/password_change_done.html'




def paginate_queryset(request, queryset, count):

    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj



def index(request):
    photos = Photo.objects.all().order_by('-created_at')
    photo_filter = Photo.objects.all().order_by('-created_at')
    page_obj = paginate_queryset(request, photos, 6)
    keyword = request.GET.get('keyword')
    if keyword:
        page_obj = photos.filter(
            Q(title__icontains=keyword) | Q(comment__icontains=keyword)
        )
    context = {
        # 'photos': page_obj.object_list,
        'photos': page_obj,
        'page_obj': page_obj,
        'keyword': photo_filter,
    }
    return render(request, 'app/index.html', context)


def users_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    #photo_filter = Photo.objects.all().order_by('-created_at', 'user').filter(user=pk)
    photo_filter = Photo.objects.all().order_by('-created_at')
    photos = user.photo_set.all().order_by('-created_at')
    page_obj = paginate_queryset(request, photos, 6)
    keyword = request.GET.get('keyword')
    if keyword:
        photos = photos.filter(
            Q(title__icontains=keyword) | Q(comment__icontains=keyword)
        )
        """elseの中をいかにしたらできた。要はページングと被ってる"""
    else:
        photos = page_obj
    context = {
        'user': user,
        'photos': photos,
        'page_obj': page_obj,
        'keyword': photo_filter,
    }
    return render(request, 'app/users_detail.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # ユーザーインスタンスを作成
        if form.is_valid():
            new_user = form.save() # ユーザーインスタンスを保存
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password1']
            # フォームの入力値で認証できればユーザーオブジェクト、できなければNoneを返す
            new_user = authenticate(username=input_username, password=input_password)
            # 認証成功時のみ、ユーザーをログインさせる
            if new_user is not None:
                # loginメソッドは、認証ができてなくてもログインさせることができる。→上のauthenticateで認証を実行する
                login(request, new_user)
                return redirect('app:users_detail', pk=new_user.pk)
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

@login_required
def photos_new(request):
    keyword = request.GET.get('keyword')

    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, "投稿が完了しました！") # 追加
        return redirect('app:users_detail', pk=request.user.pk)
    else:
        form = PhotoForm()
    return render(request, 'app/photos_new.html', {'form': form})

def photos_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'app/photos_detail.html', {'photo': photo})

@require_POST
def photos_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    photo.delete()
    return redirect('app:users_detail', request.user.id)


def photos_category(request, category):
    # titleがURLの文字列と一致するCategoryインスタンスを取得
    category = Category.objects.get(title=category)
    # 取得したCategoryに属するPhoto一覧を取得
    photos = Photo.objects.filter(category=category).order_by('-created_at')
    return render(request, 'app/index.html', {'photos': photos, 'category':category})

def contact(request):
    keyword = request.GET.get('keyword')

    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            cantact = form.save(commit=False)
            #cantact.user = request.user
            cantact.save()
            mail(request)
            messages.success(request, "お問い合わせが完了しました！") # 追加
        return redirect('app:index', )
    else:
        form = ContactForm()
    return render(request, 'app/contact.html', {'form': form})

def mail(request):

    if request.method == "POST":

        subject = request.POST.get('title')
        message = request.POST.get('content')
        from_email = request.POST.get('email')
        recipient_list = [
            "hirogram@co.jp"
        ]

        send_mail(subject, message, from_email, recipient_list)

@login_required
def like(request, pk):
    photos = get_object_or_404(Photo, pk=pk)
    is_like = Like.objects.filter(user=request.user).filter(photos=photos).count()
    if is_like > 0:
        liking = Like.objects.get(user=request.user, photos_id=pk)
        liking.delete()
        photos.like_num -= 1
        photos.save()
        messages.warning(request, 'いいねを取り消しました')
        return redirect('app:photos_detail', photos.id)
    else:
        photos.like_num += 1
        photos.save()
        like = Like()
        like.user = request.user
        like.photos = photos
        like.save()
        messages.success(request, 'いいね！しました')
        return redirect('app:photos_detail', photos.id)

def user_list(request, pk):
    users = User.objects.all()
    follow = Follow.objects.all()
    request_user = get_object_or_404(User, pk=pk)
    # users = get_object_or_404(User)
    return render(request, 'app/user_list.html', {'users': users, 'request_user': request_user, 'follow': follow})

@login_required
def follow(request, pk):
    follower = User.objects.get(username=request.user)
    following = User.objects.get(pk=pk)
    if follower == following:
        messages.warning(request, '自分自身はフォローできません')
    else:
        if not Follow.objects.filter(follower=follower, following=following).exists():
            Follow(follower=follower, following=following).save()
            messages.warning(request, 'フォローしました')
        else:
            Follow.objects.filter(follower=follower, following=following).delete()
            messages.warning(request, 'フォローを外しました')
    return redirect('app:user_list', request.user.id)








