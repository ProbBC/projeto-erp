from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView, FormView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponseRedirect
import threading

from .forms import CadastroForm, ConfirmaEmailForm
from .tokens import account_activation_token

User = get_user_model()


class CustomLoginView(LoginView):
    redirect_authenticated_user = True

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.get_user()
            if user.is_email_activated or user.is_superuser:
                request.session['loja'] = user.loja_set.get(loja_principal=True).pk
                return self.form_valid(form)
            return HttpResponseRedirect(reverse('confirmar_cadastro'))
        return self.form_invalid(form)


class CadastroView(CreateView):
    form_class = CadastroForm
    success_url = reverse_lazy('confirmar_cadastro')
    template_name = 'cadastro.html'

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        self.object = None
        form = self.get_form()
        if form.is_valid():  # is_valid chama o form.save()
            user = form.save(commit=True)
            current_site = get_current_site(request)
            mail_subject = "Ative sua conta."
            message = render_to_string('active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email_sender = threading.Thread(target=email.send)
            email_sender.start()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ConfirmarCadastro(FormView):
    form_class = ConfirmaEmailForm
    success_url = reverse_lazy('login')
    template_name = 'confirmar_cadastro.html'

    def get(self, request, *args, **kwargs):
        if request.GET:
            get_data = request.GET
            if get_data['codigo']:
                uid, token = get_data['codigo'].split('@', 1)
                uid = force_text(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=uid)
                if account_activation_token.check_token(user, token):
                    user.is_email_activated = True
                    user.save()
                    return self.form_valid(self.get_form())
                else:
                    return self.form_invalid(self.get_form())
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())
