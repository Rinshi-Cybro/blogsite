from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import View,CreateView,FormView,TemplateView,UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from account.models import UserProfile
from django.contrib import messages
from .forms import UserProfForm,PassForm,BlogForm,CommentForm
from .models import BlogModel,Comments



# Create your views here.
# decorators
# to check is_authenticated using decorators(method_decorators)

def sign_required(fn):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            return redirect('log')
    return wrapper
####--------------------------------------------------------------------###   



@method_decorator(sign_required,name='dispatch')
class UserHome(CreateView):
    # def get(self,request):
    #     user=request.user
    #     return render(request,"userhome.html",{'user_data':user})
    template_name="userhome.html"
    form_class=BlogForm
    model=BlogModel
    success_url=reverse_lazy('uhome')
    def form_valid(self,form):
        form.instance.author=self.request.user
        self.object=form.save()
        messages.success(self.request,"Blog Added Successfully !!")
        return super().form_valid(form)
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        blog=self.model.objects.all().order_by('-date')
        context['blog']=blog
        cmnt=CommentForm()
        context['comment']=cmnt
        context['cmnts']=Comments.objects.all()
        return context
    
def add_comment(request,*args,**kwargs):
    if request.method=='POST':
        cmnt=request.POST.get('comment')
        user=request.user
        b_id=kwargs.get('id')
        blog=BlogModel.objects.get(id=b_id)
        Comments.objects.create(comment=cmnt,user=user,blog=blog)
        messages.success(request,"Comment Added")
        return redirect('uhome')
    
def add_like(request,*args,**kwargs):
    blog_id=kwargs.get('bid')
    user=request.user
    blog=BlogModel.objects.get(id=blog_id)
    blog.liked_by.add(user)
    blog.save()
    return redirect('uhome')    
        


@method_decorator(sign_required,name='dispatch')    
class ViewProfile(TemplateView):
    # def get(self,request,*args,**kwargs):
    #         user=request.user
    #         return render(request,"profile.html",{'user_data':user})
    template_name="profile.html"
    
    
    
class UserProfView(CreateView):
    model=UserProfile
    form_class=UserProfForm
    template_name="bio.html"
    success_url=reverse_lazy('profile')
    # def post(self,request,*args,**kwargs):
    #     form_data=self.form_class(request.POST,request.FILES)
    #     if form_data.is_valid():
    #         form_data.instance.user=request.user
    #         form_data.save()
    #         return redirect('profile')
    #     else:
    #         return redirect('addbio')
    def form_valid(self,form):
        form.instance.user=self.request.user
        self.object=form.save()
        messages.success(self.request,"Bio Added Successfully")
        return super().form_valid(form)
    
    
class ChangePasswordView(FormView):
    template_name='resetpass.html'
    form_class=PassForm
    
    def post(self,request,*args,**kwargs):
        form_data=self.form_class(request.POST)
        if form_data.is_valid():
            old=form_data.cleaned_data.get('old_password')
            new_p=form_data.cleaned_data.get('new_password') 
            c_p=form_data.cleaned_data.get('confirm_password')
            user=authenticate(request,username=request.user.username,password=old)
            if user:
                if new_p==c_p:
                    user.set_password(c_p)
                    user.save()
                    messages.success(request,"Password Changed!!")
                    return redirect('log')
                else:
                    messages.error(request,"New Password and Confirm Password Mismathes!!!")
                    return redirect('change-password')
            else:
                messages.error(request,"Old Password Mismathes!!!")
                return redirect('change-password')
        else:
            messages.error(request,form_data.errors)
            return redirect('change-password')
        
        
class UpdateBioView(UpdateView):
    template_name='update-bio.html'
    form_class=UserProfForm
    model=UserProfile
    success_url=reverse_lazy('profile')
    pk_url_kwarg='user_id'
    def form_valid(self,form):
        self.object=form.save()
        messages.success(self.request,'Bio Updated!!!')
        return super().form_valid(form)


class MyBlogs(TemplateView):
    template_name='blogs.html'
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(**kwargs)
        blog=BlogModel.objects.filter(author=self.request.user)
        context['data']=blog
        context['cmnts']=Comments.objects.all()
        return context          



        

                
