from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from profileapp.forms import ProfileCreationForm
from profileapp.models import Profile
from django.utils.decorators import method_decorator
from profileapp.decorators import profile_ownership_required

class ProfileCreateView(CreateView):
    model = Profile
    context_object_name = "target_profile"
    form_class = ProfileCreationForm
    # success_url = reverse_lazy('accountapp:detail') 동적으로 연결 불가
    template_name = 'profileapp/create.html'

    def form_valid(self, form):
        temp_profile = form.save(commit=False)  # 실제db에 저장하진 x (임시 저장)
        temp_profile.user = self.request.user
        temp_profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accountapp:detail', kwargs={'pk': self.object.user.pk})  # self.object=Profile

@method_decorator(profile_ownership_required, 'get')
@method_decorator(profile_ownership_required, 'post')
class ProfileUpdateView(UpdateView):
    model = Profile
    context_object_name = 'target_profile'
    form_class = ProfileCreationForm
    success_url = reverse_lazy('accountapp:detail')
    template_name = 'profileapp/update.html'

    def get_success_url(self):
        return reverse_lazy('accountapp:detail', kwargs={'pk': self.object.user.pk})
