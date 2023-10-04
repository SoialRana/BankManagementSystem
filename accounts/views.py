from django.shortcuts import render,redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login,logout
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView,LogoutView
 
# Create your views here.
# jodi amra app er moddhe template create kori taile settings e template add korte hobe na otherwise lagbe 
class UserRegistrationView(FormView): #django class based view google search
    template_name='accounts/user_registration.html' 
    form_class=UserRegistrationForm
    success_url=reverse_lazy('profile') #     amader user jokhon registration complete korbe tokhon amra take kothai(profile) pathay dibo 
    # reverse lazy er kaj hocche amader website jate age thekei load hoye na thake tie use kora hoi 
    # jodi age thekei load hoye thake taile website slow kaj kore tie reverse_lazy use kora 
    def form_valid(self,form): # form_valid ekta build in functon ..django amader form valid er moddhe
        # form take pass kore dibe 
        print(form.cleaned_data)
        user=form.save()
        login(self.request, user) # form.save in korar pore amra user k login koray diye thaki ekhane
        # self.request na dile form ta se khuje pabe na ..mane login er jonno amader request kortei hobe
        print(user)
        return super().form_valid(form) # form valid function call hobe jodi shob thik thake
    # er porer kaj hocche user_registration.html form er.. 
    
    
class UserLoginView(LoginView):
    template_name='accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
class UserLogoutView(LogoutView): # Logout/Login view niye porasona korte hobe 
    def get_success_url(self):
        if self.request.user.is_authenticated: # user login ki na seta amader check korte hobe age 
            logout(self.request)
        return reverse_lazy('home')
    
    


class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
    