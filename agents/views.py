import random

from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic

from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin
from leads.models import Agent


class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    context_object_name = "agents"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    

class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:list")
    
    def form_valid(self, form):
        # TODO send email
        password = f"{random.randint(0, 1000000)}"
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(password)
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be an agent",
            message=f"You were added as an agent on DJCRM. Please come login with password {password} to start working.",
            from_email="admin@test.com",
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    model = Agent
    template_name = "agents/agent_detail.html"


class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    form_class = AgentModelForm
    template_name = "agents/agent_update.html"
    
    def get_success_url(self):
        return reverse("agents:detail", args=[self.get_object().id])

    def get_object(self, queryset=None):
        # Mendapatkan agent berdasarkan filter
        agent = Agent.objects.get(id=self.kwargs["pk"])
        # Mengembalikan user terkait agent
        return agent.user
    
    def get_context_data(self, **kwargs):
        context = super(AgentUpdateView, self).get_context_data(**kwargs)
        context.update({
            "agent": Agent.objects.get(id=self.kwargs["pk"])
        })
        return context
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    
    def get_success_url(self):
        return reverse("agents:list")
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)