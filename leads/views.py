from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .forms import (
    LeadForm, 
    LeadModelForm, 
    CustomUserCreationForm, 
    AssignAgentForm, 
    LeadCategoryUpdateForm,
    CategoryModelForm
)
from .models import Lead, Agent, Category
from agents.mixins import OrganisorAndLoginRequiredMixin


class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landingpage.html"


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        # initial query set of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, 
                agent__isnull=False
            )
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        if self.request.user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=self.request.user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset
            })
        return context


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"

    def get_queryset(self):
        user = self.request.user
        # initial query set of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(agent__user=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:list")
    
    def form_valid(self, form):
        # TODO send email
        agent = form.save(commit=False)
        agent.organisation = self.request.user.userprofile
        agent.save()
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@djcrm.com",
            recipient_list=["test@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    form_class = LeadModelForm
    template_name = "leads/lead_update.html"
    
    def get_success_url(self):
        return reverse("leads:detail", args=[self.get_object().id])
    
    def get_queryset(self):
        user = self.request.user
        # initial query set of leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)


class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    
    def get_success_url(self):
        return reverse("leads:list")
    
    def get_queryset(self):
        user = self.request.user
        # initial query set of leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)
    

class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
    
    def get_success_url(self):
        return reverse("leads:list")
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CategoryListView, self).get_context_data(**kwargs)
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation,
            )
        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial query set of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile,
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation,
            )
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DeleteView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # initial query set of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile,
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation,
            )
        return queryset


class CategoryCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/category_create.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category")

    def form_valid(self, form):
        # TODO send email
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/category_update.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category")

    def get_queryset(self):
        user = self.request.user
        # initial query set of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)

        return queryset


class CategoryDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/category_delete.html"

    def get_success_url(self):
        return reverse("leads:category")

    def get_queryset(self):
        user = self.request.user
        # initial query set of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)

        return queryset


class LeadCategoryUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    form_class = LeadCategoryUpdateForm
    template_name = "leads/lead_category_update.html"
    
    def get_success_url(self):
        return reverse("leads:detail", args=[self.get_object().id])
    
    def get_queryset(self):
        user = self.request.user
        # initial query set of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(agent__user=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


# def landing_page(request):
    # return render(request, "landingpage.html")


# def lead_list(request):
#     leads = Lead.objects.all()
#     context = {
#         "leads": leads,
#     }
#     return render(request, "leads/lead_list.html", context)


# def lead_detail(request, pk):
#     lead = get_object_or_404(Lead, pk=pk)
#     context = {
#         "lead": lead
#     }
#     return render(request, "leads/lead_detail.html", context)


# def lead_create(request):
#     form = LeadModelForm()
    
#     if request.method == "POST":
#         # form = LeadForm(request.POST)
#         form = LeadModelForm(request.POST)
        
#         if form.is_valid():
#             # first_name = form.cleaned_data['first_name']
#             # last_name = form.cleaned_data['last_name']
#             # age = form.cleaned_data['age']
#             # agent = Agent.objects.first()
#             # Lead.objects.create(
#             #     first_name=first_name,
#             #     last_name=last_name,
#             #     age=age,
#             #     agent=agent,
#             # )
#             form.save()
#             return HttpResponseRedirect(reverse("leads:list"))

#     context = {
#         "form": form
#     }
#     return render(request, "leads/lead_create.html", context)


# def lead_update(request, pk):
#     lead = get_object_or_404(Lead, pk=pk)
#     form = LeadModelForm(instance=lead)
    
#     if request.method == "POST":
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("leads:list"))

#     context = {
#         "form": form,
#         "lead": lead,
#     }
#     return render(request, "leads/lead_update.html", context)


# def lead_delete(request, pk):
#     get_object_or_404(Lead, pk=pk).delete()
#     return HttpResponseRedirect(reverse("leads:list"))
