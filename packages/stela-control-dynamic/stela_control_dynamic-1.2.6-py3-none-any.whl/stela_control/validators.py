import re, datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from linkzone.context_processors import SiteData
from django.conf import settings
from pytz import country_timezones
from django.forms import formset_factory, inlineformset_factory
from django.http.response import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from accounts.models import UserBase
from .models import (
    Content, Wallet, DataEmail, 
    DynamicBullets, Newsletter, SendMoney, BillingRecipt,
    ItemProducts, ItemServices, ItemDiscount,  
    InvoiceControl, BudgetControl, StelaSelection, 
    StelaItems, Templates, Order, StelaPayments, PathControl, 
    ControlFacturacion, FacturaItems, TemplateSections, StelaColors,
    ModuleItems, ProStelaData, OrderItems, Inventory, Modules, 
    Variants, Sizes, Gallery, Bulletpoints, Sizes, VariantsImage, Customer, 
    Budget, Category, SitePolicy, LegalProvision, SupportResponse, 
    Support, ChatSupport, SiteControl, ItemCloud, FacebookPage, InstagramAccount, FacebookPostPage, FacebookPageComments, FacebookPageCommentsReply, FacebookPageConversations,
    FacebookPageEvent,  FacebookPageLikes, FacebookPageMessages, FacebookPageShares, FacebookPostMedia, IGMediaContent, FacebookPageImpressions,
    IGPost, IGUserTag, FAQ, SetFaq, Poll, Contact,Comments, PaypalClient, Notifications,
    IGPostMetric, IGCarouselMetric, IGReelMetric, IGStoriesMetric, Company, SocialLinks, ProStelaExpert, ProStelaUsage, Reviews,
    Booking, BookingServices
    
)
from .forms import (
    SiteNewsForm, FAQForm, NewsletterForm,
    PolicyForm, UserForm, BillingForm, BillingDiscountForm, 
    ModulesForm,TemplateForm, ProductForm, StylesForm, 
    TempSecForm, ColorsForm, VariantForm, SizeForm, GalleryForm, BulletForm, 
    ServiceForm, VariantImageForm, BillingChargeFormDynamic, BillingChargeFormPOS, 
    BillingFormSuscription, AppstelaForm, LegalProvitionForm, StelaAboutForm, 
    PathForm, MediaForm, FooterContentForm, categForm, 
    BulletSimpleForm, CommentsFormBlog, ReadOnlySupportForm, WalletForm,
    FbPostForm, FacebookEventsForm, IGPostForm, IGMediaForm, RequiredFormSet, CompanyForm, SocialMediaForm,
    SendGridForm,BlogForm, ContentForm, RedirectContentForm, StickerContentForm, ContentDynamicForm,
    SimpleContentForm, SetFaqForm, ImageContentForm, TextContentForm, AboutContentForm, ReviewsForm,
    ConsultingForm, BookingConsultingForm
)

@csrf_exempt
def accountsData(request):
    action = request.POST.get('action')
    print(action)
    
    if action == "checkEmail":
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        email = request.POST.get("user_input")
        if UserBase.objects.filter(email=email).exists():
            response = JsonResponse({'error': _('email not available')})
        elif not pattern.match(email):
            response = JsonResponse({'error': _('Invalid email')})
        else:
            response = JsonResponse({'success': _('email available')})
        return response

    if action == "checkUsername":
        username = request.POST.get("user_input")
        if UserBase.objects.filter(username=username).exists():
            response = JsonResponse({'error': _('username not available')})
            
        elif not re.match(r'^[a-z0-9_]+$', username):
            response = JsonResponse({'error': _('invalid username only lower case, numbers and (_) accepted')})
        
        else:
            response = JsonResponse({'success': _('username available')})
        
        return response
        
    if action == "checkPassword":
        password = request.POST.get("password")
        
        if len(password) < 8:
            response = JsonResponse({'error': _('Password must be at least 8 characters long')})
        
        elif not re.match(r'^[a-zA-Z0-9*.$_]+$', password):
            response = JsonResponse({'error': _('Password must contain only alphanumeric and special characters (a-zA-Z0-9*$_.)')})
        
        elif password.isalpha():
            response = JsonResponse({'error': _('Password must contain at least one number')})
            
        else:
            response = JsonResponse({'success': _('Password is valid')})

        return response

    if action == "matchPassword":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            response = JsonResponse({'error': _('Password dismatch.')})
        else:
            response = JsonResponse({'success': _('Password match')})
        return response

@csrf_exempt
def contentData(request):
    if request.method == 'POST':
        lang=request.LANGUAGE_CODE
        author=request.user
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id, action)
        
        if action == "checkslider_simple":        
            content=Content.objects.filter(author=author, section="slider_simple", lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=SimpleContentForm,
                    extra=0, can_delete=True,
                )
                formset = get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section='slider_simple'))
                obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/slider_simple_form.html', { 
                    'formset': formset   
                })
                response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=SimpleContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/maincontent/forms/slider_simple_form.html', { 
                    'formset': get_formset(prefix='formset') 
                })
                response = JsonResponse({'empty': obj_data})
            return response

        if action == "checkslider_content":        
            content=Content.objects.filter(author=author, section="slider_content", lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=ContentForm,
                    extra=0, can_delete=True,
                )
                formset = get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section='slider_content'))
                obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/slider_content_form.html', { 
                    'formset': formset   
                })
                response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=ContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/maincontent/forms/slider_content_form.html', { 
                    'formset': get_formset(prefix='formset') 
                })
                response = JsonResponse({'empty': obj_data})
            return response
        
        if action == "checkSection":        
            pk=request.POST.get('authorid')
            author=UserBase.objects.get(pk=pk)
            content=Content.objects.filter(author=author, section="Sections Pack", lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=RedirectContentForm,
                    extra=0, can_delete=True,
                )
                obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/sections_form.html', { 
                    'formset': get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section='Sections Pack'))   
                })
                response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=RedirectContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=3 
                )
                obj_data = render_to_string('stela_control/load-data/maincontent/forms/sections_form.html', { 
                    'formset': get_formset(prefix='formset') 
                })
                response = JsonResponse({'empty': obj_data})
            return response
        
        if action == "checkProject":        
            pk=request.POST.get('authorid')
            author=UserBase.objects.get(pk=pk)
            content=Content.objects.filter(author=author, section="Project Carousel", lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=RedirectContentForm,
                    extra=0, can_delete=True,
                )
                obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/projects_form.html', { 
                    'formset': get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section='Project Carousel'))   
                })
                response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=RedirectContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/maincontent/forms/projects_form.html', { 
                    'formset': get_formset(prefix='formset') 
                })
                response = JsonResponse({'empty': obj_data})
            return response

        if action == "checkApp":        
            content=Content.objects.filter(author=author, section="App Carousel", lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=StickerContentForm,
                    extra=0, can_delete=True,
                )
                obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/apps_form.html', { 
                    'formset': get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section='App Carousel'))   
                })
                response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=StickerContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/maincontent/forms/apps_form.html', { 
                    'formset': get_formset(prefix='formset') 
                })
                response = JsonResponse({'empty': obj_data})
            return response

        if action == "checkSetFAQ":
            faq_pk=request.POST.get('faqpk')
            faq=FAQ.objects.get(pk=faq_pk)
            get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0, can_delete=True,
                )
            obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/faq_form.html', { 
                'formset2': get_formset(instance=faq, prefix='formset2')   
            })
            return JsonResponse({'content': obj_data})
            
        if action == "removeContent":
            pk = request.POST.get('id')
            content = Content.objects.get(pk=pk)
            content.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
        
        if form_id == "slider_simple":
            content=Content.objects.filter(author=author, section="slider_simple", lang=lang)
            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=SimpleContentForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=author)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "slider_simple"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/slider_simple_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                get_formset = formset_factory(
                    form=SimpleContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "slider_simple"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/slider_simple_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
        
        if form_id == "slider_content":
            content=Content.objects.filter(author=author, section="slider_content", lang=lang)
            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=ContentForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=author)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "slider_content"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/slider_simple_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                get_formset = formset_factory(
                    form=ContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "slider_content"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/slider_simple_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
        
        if form_id == "section-form":
            content=Content.objects.filter(author=author, section="Sections Pack", lang=lang)
            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=RedirectContentForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=author)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "Sections Pack"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/sections_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                get_formset = inlineformset_factory(
                        UserBase, Content, 
                        form=RedirectContentForm,
                        extra=0,
                        can_delete=False,
                        validate_min=True, 
                        min_num=1 
                    )
                formset=get_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "Sections Pack"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/sections_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
                
        if form_id == "project-form":
            content=Content.objects.filter(author=author, section="Project Carousel", lang=lang)
            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=RedirectContentForm,
                    extra=0, can_delete=False,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=author)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "Project Carousel"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/projects_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                get_formset = inlineformset_factory(
                        UserBase, Content, 
                        form=RedirectContentForm,
                        extra=0,
                        can_delete=False,
                        validate_min=True, 
                        min_num=3
                    )
                formset=get_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "Project Carousel"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/projects_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
        
        if form_id == "apps-form":
            content=Content.objects.filter(author=author, section="App Carousel", lang=lang)
            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=StickerContentForm,
                    extra=0,
                    can_delete=False,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=author)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "App Carousel"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/apps_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                get_formset = inlineformset_factory(
                        UserBase, Content, 
                        form=StickerContentForm,
                        extra=0,
                        can_delete=False,
                        validate_min=True, 
                        min_num=1
                    )
                formset=get_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = "App Carousel"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/apps_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
        
        if form_id == "faq-form":
            content=FAQ.objects.filter(author=author, lang=lang)
            if content:
                get_formset = inlineformset_factory(
                    UserBase, FAQ, 
                    form=FAQForm,
                    extra=0, can_delete=False,
                )
                formset=get_formset(request.POST, prefix='formset', instance=author)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/faq_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
            else:
                get_formset = inlineformset_factory(
                    UserBase, FAQ, 
                    form=FAQForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                get_formset2 = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, prefix='formset')
                formset2=get_formset2(request.POST, prefix='formset2')
                if all[
                    formset.is_valid(),
                    formset2.is_valid()
                    ]:
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.lang = lang
                        data.save()

                    for form2 in formset2:
                        data2 = form2.save(commit=False)
                        data2.faq = data
                        data2.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/faq_form_clean.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
                
        if form_id == "setfaq-form":
            faq_pk=request.POST.get('faqpk')
            faq=FAQ.objects.get(pk=faq_pk)
            get_formset = inlineformset_factory(
                FAQ, SetFaq, 
                form=SetFaqForm,
                extra=0, can_delete=True,
            )
            formset=get_formset(request.POST, prefix='formset2', instance=faq)
            if formset.is_valid():

                for form in formset:
                    data = form.save(commit=False)
                    data.faq = faq
                    data.save()

                return JsonResponse({'success':_('Your content was upload successfully')})
            else:
                print(formset.errors)
                obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/faq_form.html', { 
                    'formset': formset,
                    'errors': formset.errors,
                })
                return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})

@csrf_exempt    
def docsData(request): 
    if request.method == 'POST':
        lang=request.LANGUAGE_CODE
        author=request.user
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id, action)
        
        if action == "checkAbout":
            content=Content.objects.filter(author=author, section="About Values", lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=AboutContentForm,
                    extra=0, can_delete=True,
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/update_forms/aboutform.html', { 
                    'formset': get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section='About Values')), 
                    'pk': author.pk
                })
                response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=AboutContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/forms/aboutform.html', { 
                    'formset': get_formset(prefix='formset') 
                })
                response = JsonResponse({'empty': obj_data})
            return response
        
        if action == "checkCardContent":        
            content=Content.objects.filter(author=author, section="Card Content", lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=ContentForm,
                    extra=0, can_delete=True,
                )
                formset = get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section='Card Content'))
                obj_data = render_to_string('stela_control/load-data/contentdocs/update_forms/cardform.html', { 
                    'formset': formset,
                    'pk': author.pk   
                })
                response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=ContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/forms/cardform.html', { 
                    'formset': get_formset(prefix='formset') 
                })
                response = JsonResponse({'empty': obj_data})
            return response
        
        if action == "checkImageBullet":  
            uk=request.POST.get('uk')
            if uk:      
                content=Content.objects.get(pk=uk)
                form=ImageContentForm(instance=content)
                get_formset = inlineformset_factory(
                    Content, DynamicBullets, 
                    form=BulletSimpleForm,
                    extra=0, can_delete=False,
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/update_forms/imagebulletform.html', { 
                    'form': form,
                    'formset': get_formset(instance=content, prefix='formset'),
                    'pk': content.pk
                        
                })
                response = JsonResponse({'content': obj_data})
            else:
                form=ImageContentForm()
                get_formset = formset_factory(
                    form=BulletSimpleForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/forms/imagebulletform.html', { 
                    'form': form,
                    'formset': get_formset(prefix='formset')
                })
                response = JsonResponse({'empty': obj_data})
            return response
        
        if action == "checkBoxIconBulllets":        
            content=Content.objects.filter(author=author, section="Icon Box", lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=TextContentForm,
                    extra=0, can_delete=True,
                )
                formset = get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section='Icon Box'))
                obj_data = render_to_string('stela_control/load-data/contentdocs/update_forms/box-info.html', { 
                    'formset': formset,
                    'pk': author.pk   
                })
                response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=TextContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/forms/box-info.html', { 
                    'formset': get_formset(prefix='formset') 
                })
                response = JsonResponse({'empty': obj_data})
            return response

        if action == "checkDocs":
            pk=request.POST.get('pk')
            if pk:
                obj=SitePolicy.objects.get(pk=pk)
                form=PolicyForm(instance=obj)
                get_formset = inlineformset_factory(
                SitePolicy, LegalProvision, 
                form=LegalProvitionForm,
                extra=0, can_delete=True,
                )
                formset=get_formset(instance=obj, prefix='terms')

                obj_data = render_to_string('stela_control/load-data/contentdocs/update_forms/terms.html', {
                                'form': form, 
                                'formset': formset,   
                                'obj': obj  
                    })

                response = JsonResponse({'content': obj_data})
            else:
                form=PolicyForm()
                get_formset = inlineformset_factory(
                    SitePolicy, LegalProvision, 
                    form=LegalProvitionForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(prefix='terms')

                obj_data = render_to_string('stela_control/load-data/contentdocs/forms/terms.html', {
                                'form': form, 
                                'formset': formset,   
                    })
                response = JsonResponse({'empty': obj_data})
            return response

        if action == "checkFAQ": 
            pk=request.POST.get('pk')
            if pk:   
                print(pk)
                content=FAQ.objects.get(pk=pk)
                form=FAQForm(instance=content)
                get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0, can_delete=False,
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/update_forms/faq_form.html', { 
                    'formset': get_formset(instance=content, prefix='formset')   
                })
                response = JsonResponse({'content': obj_data})
            else:
                form=FAQForm()
                get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/forms/faq_form.html', { 
                    'form': form,
                    'formset': get_formset(prefix='formset')
                })
                response = JsonResponse({'empty': obj_data})
            return response
        
        if action == "removeDoc":
            doc_id=request.POST.get('id')
            doc=SitePolicy.objects.get(pk=doc_id)
            doc.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})

        if action == "removeContent":
            content_id=request.POST.get('id')
            content=Content.objects.get(pk=content_id)
            content.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})

        if action == "removeFAQ":
            content_id=request.POST.get('id')
            content=FAQ.objects.get(pk=content_id)
            content.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})

        if form_id == "doc-form":
            update_form = request.POST.get('form-update')
            if update_form:
                form=PolicyForm(request.POST, instance=update_form)
                get_formset = inlineformset_factory(
                    SitePolicy, LegalProvision, 
                    form=LegalProvitionForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, prefix='terms', instance=update_form)
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    policy = form.save(commit=False)
                    policy.owner = author
                    policy.lang = lang
                    policy.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.policy = policy
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_forms/terms.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'clause_cke':'content'})
            else:
                form=PolicyForm(request.POST)
                get_formset = inlineformset_factory(
                    SitePolicy, LegalProvision, 
                    form=LegalProvitionForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, prefix='terms')
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    policy = form.save(commit=False)
                    policy.owner = author
                    policy.lang = lang
                    policy.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.policy = policy
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_empty_forms/terms.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'clause_cke':'content'})
        
        if form_id == "about-form":
            pk = request.POST.get('form-update')
            if pk:
                instance=UserBase.objects.get(pk=pk)
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=AboutContentForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=instance)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.path = "Services"
                        data.section = "About Values"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_forms/aboutform.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'about_cke':'content'})
            else:
                get_formset = formset_factory(
                    form=AboutContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.path = "Services"
                        data.section = "About Values"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_empty_forms/aboutform.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'about_cke':'content'})
        
        if form_id == "card-form":
            pk = request.POST.get('form-update')
            if pk:
                instance=UserBase.objects.get(pk=pk)
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=ContentForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=instance)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.path = "Services"
                        data.section = "Card Content"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_forms/cardform.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'about_cke':'content'})
            else:
                get_formset = formset_factory(
                    form=ContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.path = "Services"
                        data.section = "Card Content"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_empty_forms/cardform.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'about_cke':'content'})

        if form_id == "imagebullet-form":
            pk = request.POST.get('form-update')
            if pk:
                content=Content.objects.get(pk=pk)
                form=ImageContentForm(request.POST, request.FILES, instance=content)
                get_formset = inlineformset_factory(
                    Content, DynamicBullets, 
                    form=BulletSimpleForm,
                    extra=0, can_delete=False,
                )
                formset=get_formset(request.POST, prefix='formset', instance=content)
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.author = author
                    parent.path = "Services"
                    parent.section = "Image Bullet"
                    parent.lang = lang
                    parent.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.parent = parent
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_forms/terms.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                form=ImageContentForm(request.POST, request.FILES)
                get_formset = formset_factory(
                    form=BulletSimpleForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1
                )
                formset=get_formset(request.POST, prefix='formset')
                print(form.is_valid(),
                        formset.is_valid())
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.author = author
                    parent.path = "Services"
                    parent.section = "Image Bullet"
                    parent.lang = lang
                    parent.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.parent = parent
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_empty_forms/terms.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
    
        if form_id == "boxicon-form":
            pk = request.POST.get('form-update')
            if pk:
                instance=UserBase.objects.get(pk=pk)
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=TextContentForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=instance)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.path = "Services"
                        data.section = "Icon Box"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_forms/box-info.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                get_formset = formset_factory(
                    form=TextContentForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.path = "Services"
                        data.section = "Icon Box"
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_empty_forms/box-info.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

        if form_id == "faq-form":
            pk = request.POST.get('form-update')
            if pk:
                content=FAQ.objects.get(pk=pk)
                form=FAQForm(request.POST, instance=content)
                get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0, can_delete=False,
                )
                formset=get_formset(request.POST, prefix='formset', instance=content)
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.author = author
                    parent.lang = lang
                    parent.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.faq = parent
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_forms/faq_form.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'clause_faq':'content'})
            else:
                form=FAQForm(request.POST)
                get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, prefix='formset')
                print(form.is_valid(),
                        formset.is_valid())
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.author = author
                    parent.lang = lang
                    parent.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.faq = parent
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/contentdocs/error_empty_forms/faq_form.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'clause_faq':'content'})

@csrf_exempt 
def stelaStoryData(request):
    if request.method == 'POST':
        lang=request.LANGUAGE_CODE
        author=request.user
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id, action)

        if action == "checkBlog":       
            form = BlogForm()
            obj_data = render_to_string('stela_control/load-data/maincontent/forms/blog_form.html', { 
                    'form': form
                })
            return JsonResponse({'empty': obj_data})
        
        if action == "postData":   
            postpk=request.POST.get('obj')    
            post = Content.objects.get(pk=postpk)
            obj_data = render_to_string('stela_control/load-data/stela_story/feed-item.html', { 
                    'post': post,
                    'usertz': get_timezone,
                })
            return JsonResponse({'content': obj_data})
        
        if action == "filter":   
            filter=request.POST.get('get_value')   
            feed=Content.objects.filter(author=author, lang=lang).order_by('-id')
            if filter in [_('News'), _('Tutorials'), _('Tips and Tricks'), _('Guides and Manuals'), _('Inspiration'), _('Events and Conferences'), _('Interviews')]:   
                filter_feed=feed.filter(category=filter)
                obj_data = render_to_string('stela_control/load-data/stela_story/table-blog-filter.html', { 
                        'feed': filter_feed,
                        'usertz': get_timezone,
                    })
                response = JsonResponse({'filter_data': obj_data})

            elif filter in ['today', '15', '29']:
                if filter == 'today':
                    start_date = datetime.datetime.now().date()
                    end_date = start_date
                elif filter == '15':
                    end_date = datetime.datetime.now().date()
                    start_date = end_date - timedelta(days=15)
                elif filter == '29':
                    end_date = datetime.datetime.now().date()
                    start_date = end_date - timedelta(days=29)

                filter_feed=feed.filter(created__range=[start_date, end_date])
                obj_data = render_to_string('stela_control/load-data/stela_story/table-blog-filter.html', { 
                        'feed': filter_feed,
                        'usertz': get_timezone,
                    })
                response = JsonResponse({'filter_data': obj_data})

            elif filter == '':
                obj_data = render_to_string('stela_control/load-data/stela_story/table-blog-filter.html', { 
                        'feed': feed,
                        'usertz': get_timezone,
                    })
                response = JsonResponse({'filter_data': obj_data})
            return response
        
        if action == "updateFeed":   
            pk = request.POST.get('feed_id')    
            post=Content.objects.get(pk=pk)
            form = BlogForm(instance=post)
            if post.is_schedule:
                obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/blog_form.html', { 
                        'form': form,
                    })
                response = JsonResponse({
                        'content': obj_data,
                        'getDate': post.schedule
                    })
            else:
                obj_data = render_to_string('stela_control/load-data/maincontent/update_forms/blog_form.html', { 
                        'form': form,
                    })
                response = JsonResponse({'content': obj_data})
                
            return response
        
        if action == "removeObj":
            item_ids = request.POST.getlist('id[]')
            for id in item_ids:
                obj = Content.objects.get(pk=id)
                obj.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
        
        if action == "loadPages":
            lang=request.LANGUAGE_CODE
            country_id = str(lang).split('-')
            get_timezone = country_timezones(country_id[1])[0] 
            starts = int(request.POST.get('start'))
            ends = int(request.POST.get('ends'))
            print(starts)
            print(ends)
            new_posts = Content.objects.filter(author=author, lang=lang).order_by('-id')[starts:ends]
            new_pages = render_to_string('stela_control/load-data/blog-feed.html', {
                    'feed': new_posts,
                    'usertz': get_timezone,
                    })
            return JsonResponse({'response': new_pages})
        
        if form_id == "blog-form":
            form = BlogForm(request.POST, request.FILES)
            website = request.POST.get('website')
            schedule = request.POST.get('schedule')
            if form.is_valid():
                data = form.save(commit=False)
                data.author = author
                data.section = "Blog Post"
                data.site = website
                data.lang = lang
                data.save()

                if schedule:
                    Content.objects.filter(pk=data.id).update(schedule=schedule, is_schedule=True)

                return JsonResponse({'success':_('Your post was upload successfully')})
            else:
                print(form.errors)
                obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/blog_form.html', { 
                    'form': form,
                    'errors': form.errors,
                })
                return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
        
        if form_id == "blog-update":
            pk = request.POST.get('obj-id')    
            post=Content.objects.get(pk=pk)
            form = BlogForm(request.POST, request.FILES, instance=post)
            website = request.POST.get('website')
            schedule = request.POST.get('schedule')
            if form.is_valid():
                data = form.save(commit=False)
                data.author = author
                data.section = "Blog Post"
                data.site = website
                data.lang = lang
                data.save()

                if schedule:
                    Content.objects.filter(pk=data.id).update(schedule=schedule, is_schedule=True)

                return JsonResponse({'success':_('Your post was upload successfully')})
            else:
                print(form.errors)
                obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/blog_form.html', { 
                    'form': form,
                    'errors': form.errors,
                })
                return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})

@csrf_exempt  
def inventoryData(request):
    if request.method == 'POST':
        owner=UserBase.objects.get(is_superuser=True)
        category=Category.objects.get(type="Consulting")
        lang=request.LANGUAGE_CODE
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id)
        print(action)

        if action == "checkConsultingServices":
            content=Inventory.objects.filter(owner=owner, category=category, lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Inventory, 
                    form=ConsultingForm,
                    extra=0, can_delete=True,
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/update_forms/aboutform.html', { 
                    'formset': get_formset(instance=owner, prefix='formset', queryset=Inventory.objects.filter(owner=owner, category=category, lang=lang)), 
                    'pk': owner.pk
                })
                response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=ConsultingForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/contentdocs/forms/aboutform.html', { 
                    'formset': get_formset(prefix='formset') 
                })
                response = JsonResponse({'empty': obj_data})
            return response

        if action == "data":
            obj_id=request.POST.get('objid')
            obj=Inventory.objects.get(pk=obj_id)
            form=ServiceForm(instance=obj, prefix="update")
            get_formset = inlineformset_factory(
            Inventory, Modules, 
            form=ModulesForm,
            extra=0, can_delete=True,
            )
            formset=get_formset(instance=obj, prefix='update')

            obj_data = render_to_string('stela_control/load-data/formset-base-services.html', {
                            'form': form, 
                            'formset': formset,   
                            'pk': obj_id, 
                })

            response = JsonResponse({'response': obj_data})
            return response

        if action == "deleteObj":
            item_ids = request.POST.getlist('id[]')
            for id in item_ids:
                obj = Inventory.objects.get(pk=id)
                obj.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
        
        if action == "categoryData":
            pk=request.POST.get('pk')
            if pk:
                obj=Category.objects.get(pk=pk)
                form = categForm(instance=obj)
                obj_data = render_to_string('stela_control/load-data/products/new/category-form.html', {
                                'form': form,  
                                'obj': pk, 
                    })
            else:
                get_formset = formset_factory(
                    categForm, 
                    formset=RequiredFormSet, 
                    extra=1,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/products/update/category-form.html', {
                                'formset': formset,   
                    })

            response = JsonResponse({'response': obj_data})
            return response
        
        if action == "newProductData":
            pk=request.POST.get('pk')
            if pk:
                obj=Inventory.objects.get(pk=pk)
                form = ProductForm(instance=obj)
                get_formset = inlineformset_factory(
                    Inventory, Bulletpoints, 
                    form=BulletForm,
                    extra=1, can_delete=False,
                )
                formset=get_formset(instance=obj, prefix='update')
                obj_data = render_to_string('stela_control/load-data/products/new/product-form.html', {
                            'form': form, 
                            'formset': formset,   
                            'obj': pk, 
                })
            else:
                form = ProductForm()
                get_formset = inlineformset_factory(
                    Inventory, Bulletpoints, 
                    form=BulletForm,
                    extra=1, 
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 

                )
                formset=get_formset()
                obj_data = render_to_string('stela_control/load-data/products/update/product-form.html', {
                                'form': form, 
                                'formset': formset,   
                    })

            response = JsonResponse({'response': obj_data})
            return response
            
        if action == "variantData":
            pk=request.POST.get('pk')
            if pk:
                obj_id=request.POST.get('variantid')
                obj=Variants.objects.get(pk=pk)
                form=VariantForm(instance=obj)
                obj_data = render_to_string('stela_control/load-data/products/new/variant-form.html', {
                                'form': form,  
                                'obj': pk  
                    })
            else:
                get_formset = formset_factory(
                    VariantForm, 
                    formset=RequiredFormSet, 
                    extra=1,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/products/update/variant-form.html', {
                                'formset': get_formset()
                    })

            response = JsonResponse({'response': obj_data})
            return response
        
        if action == "sizeData":
            pk=request.POST.get('pk')
            if pk:
                obj=Sizes.objects.get(pk=pk)
                form=SizeForm(instance=obj)

                obj_data = render_to_string('stela_control/load-data/products/new/size-form.html', {
                                'form': form,  
                                'obj': pk  
                    })
            else:
                get_formset = formset_factory(
                    SizeForm, 
                    formset=RequiredFormSet, 
                    extra=1,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/products/update/size-form.html', {
                                'form': form,    
                    })

            response = JsonResponse({'response': obj_data})
            return response
        
        if action == "colorData":
            pk=request.POST.get('pk')
            if pk:
                obj=StelaColors.objects.get(pk=pk)
                form=ColorsForm(instance=obj)

                obj_data = render_to_string('stela_control/load-data/products/new/color-form.html', {
                                'form': form,  
                                'obj': pk  
                    })
            else:
                get_formset = formset_factory(
                    ColorsForm, 
                    formset=RequiredFormSet, 
                    extra=1,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/products/update/color-form.html', {
                                'form': get_formset(),    
                    })

            response = JsonResponse({'response': obj_data})
            return response
        
        if action == "catalogData":
            pk=request.POST.get('pk')
            if pk:
                obj=VariantsImage.objects.get(pk=obj_id)
                form=VariantImageForm(instance=obj, prefix="update")
        
                get_formset = inlineformset_factory(
                    VariantsImage, Gallery, 
                    form=GalleryForm,
                    extra=0, can_delete=True,
                    )
                formset2=get_formset(instance=obj, prefix='update')
                obj_data = render_to_string('stela_control/load-data/products/new/catalog-form.html', {
                                'form': form,  
                                'formset2': formset2,  
                                'catalog': obj  
                    })
            else:
                form=VariantImageForm()
                get_formset = inlineformset_factory(
                    VariantsImage, Gallery, 
                    form=GalleryForm,
                    extra=0, 
                    can_delete=True,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/products/update/catalog-form.html', {
                                'form': form,  
                                'formset': get_formset(),   
                    })
            response = JsonResponse({'response': obj_data})
            return response

        if action == "deleteObj":
            item_ids = request.POST.getlist('id[]')
            for id in item_ids:
                obj = Inventory.objects.get(pk=id)
                obj.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
        
        if form_id == "newService":
            update_form = request.POST.get('form-update')
            if update_form:
                service=Inventory.objects.get(pk=update_form)
                set_formset = inlineformset_factory(
                    Inventory, Modules, 
                    form=ModulesForm,
                    extra=0, can_delete=True,
                    )
                form = ServiceForm(request.POST, request.FILES, instance=service, prefix="update")
                formset = set_formset(request.POST, request.FILES, prefix='update', instance=service)  
                if all([form.is_valid(),
                        formset.is_valid(),
                        ]):
                        parent = form.save(commit=False)
                        parent.save()
                            
                        instances = formset.save(commit=False)
                                
                        for obj in formset.deleted_objects:
                                obj.delete()
                                
                        for instance in instances:
                            instance.parent = parent
                            instance.save()

                        return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/formset-base-services.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
            else:
                form = ServiceForm(request.POST, request.FILES)
                formset = get_formset(request.POST, request.FILES, prefix='form')
                    
                if all([form.is_valid(), 
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.owner = request.user
                    parent.type = "Service"
                    parent.lang = lang
                    parent.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.parent = parent
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/formset-base-services', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
        
        if form_id == "newProductForm":
            products=Inventory.objects.filter(type='Product')
            sku_count=products.count() + 1 
            form = ProductForm(request.POST, request.FILES)
            formset2 = get_formset2(request.POST, prefix='bullet')
            if all([form.is_valid(), 
                    formset2.is_valid(),
                    ]):
                    cat_id = form.cleaned_data['category']
                    category=Category.objects.get(pk=cat_id.pk)
                    get_code = str(category.type+'-'+category.slug+'-'+str(sku_count))
                    parent = form.save(commit=False)
                    parent.category = category
                    parent.sku = get_code
                    parent.owner = request.user
                    parent.type = "Product"
                    parent.lang = lang
                    parent.save()

                    for form in formset2:
                        child2 = form.save(commit=False)
                        child2.product = parent
                        child2.save()
                    
                    messages.success(request, _("Changes made successfully"))
                    return redirect('/inventory-control/products')

            else:
                print (formset.errors)
                return render(request, 'stela_control/inventory/products/index-products.html', {
                    'stock': stock,
                    'sizes': sizes,
                    'form': form,
                    'form2': form2,
                    'formset': formset, 
                    'formset2': formset2,
                    'errors': formset.errors,
                    'errors2': formset2.errors,
            })

        if form_id == "newSize":
            formset3 = get_formset3(request.POST, prefix='sizes')
            if formset3.is_valid():
                
                for form in formset3:
                        form.save()

                messages.success(request, _("Changes made successfully"))
                return redirect('/inventory-control/products')
            else:
                print (formset3.errors)

        if form_id == "newVariant":
            formset4 = get_formset4(request.POST, request.FILES, prefix='variant')
            if formset4.is_valid():
                
                for form in formset4:
                        form.save()

                messages.success(request, _("Changes made successfully"))
                return redirect('/inventory-control/products')
            else:
                print (formset4.errors)

        if form_id == "newCatalog":
            form2 = VariantImageForm(request.POST)
            formset=get_formset(request.POST, request.FILES, prefix='gallery')
            if all([form2.is_valid(), 
                    formset.is_valid(),
                    ]):
                
                    catalogue = form2.save(commit=False)
                    catalogue.save()

                    for form in formset:
                        child2 = form.save(commit=False)
                        child2.catalogue = catalogue
                        child2.save()
                    
                    messages.success(request, _("Changes made successfully"))
                    return redirect('/inventory-control/products')
            else:
                print (formset4.errors)

        if form_id == "Update":
            pk=request.POST.get('obj-id')
            variant=Variants.objects.get(pk=pk)

            form=VariantForm(request.POST, request.FILES, instance=variant)
            if form.is_valid():
                form.save()
                messages.success(request, _("Changes made successfully"))
                return redirect('/inventory-control/products')
            else:
                print(formset.errors)
        
        if form_id == "sizeUpdate":
            pk=request.POST.get('size-id')
            size=Sizes.objects.get(pk=pk)

            form=SizeForm(request.POST, instance=size)
            if form.is_valid():
                form.save()
                messages.success(request, _("Changes made successfully"))
                return redirect('/inventory-control/products')
            else:
                print(formset.errors)

        if form_id == "catalogUpdate":
            pk=request.POST.get('catalog-id')
            catalog=VariantsImage.objects.get(pk=pk)
            form=VariantImageForm(instance=catalog, prefix="update")
    
            get_formset = inlineformset_factory(
                VariantsImage, Gallery, 
                form=GalleryForm,
                extra=0, can_delete=True,
                )
           
            form = VariantImageForm(request.POST, instance=catalog, prefix="update")
            formset2 = get_formset(request.POST, request.FILES, prefix='update-gallery', instance=catalog)  
            if all([form.is_valid(),
                    formset2.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.save()
                        
                    instances2 = formset2.save(commit=False)
                            
                    for obj in formset2.deleted_objects:
                            obj.delete()
                            
                    for instance in instances2:
                        instance.catalogue = parent
                        instance.save()
                    
                    messages.success(request, _("Changes made successfully"))
                    return redirect('/inventory-control/products')
            else:
                print(
                    form.errors,
                    formset.errors,
                    formset2.errors,
                )
                return render(request, 'stela_control/inventory/products/index-products.html', {
                    'stock': stock,
                    'sizes': sizes,
                    'form': form,
                    'form2': form2,
                    'formset': formset, 
                    'formset2': formset2,
                    'formset3': formset3,
                    'formset4': formset4,
                    'errors': formset.errors,
                    'errors2': formset2.errors,
            })

        if form_id == 'colorForm':
                formset=colorform(request.POST, prefix='color')
                if formset.is_valid():

                    for loop in formset:
                        color=loop.save(commit=False)
                        color.owner=request.user
                        color.save()

                    messages.success(request, _("Changes made successfully"))
                    return redirect('stela:products')
                else:
                    print(formset.errors)

        if form_id == 'colorUpdate':
            obj_id=request.POST.get('obj-id')
            data=StelaColors.objects.get(pk=obj_id)
            form=ColorsForm(request.POST, instance=data)
            if form.is_valid():
                form.save()

                messages.success(request, _("Changes made successfully"))
                return redirect('/inventory-control/products')
            else:
                print(form.errors)
                
        if form_id == 'categForm':
                formset=categform(request.POST, prefix='categ')
                if formset.is_valid():

                    for loop in formset:
                        category=loop.save(commit=False)
                        category.owner=request.user
                        category.save()
            
                    messages.success(request, _("Changes made successfully"))
                    return redirect('/inventory-control/products')
                else:
                    print(formset.errors)   

        if form_id == 'categUpdate':
            obj_id=request.POST.get('obj-id')
            data=Category.objects.get(pk=obj_id)
            form=categForm(request.POST, instance=data)
            if form.is_valid():
                form.save()

                messages.success(request, _("Changes made successfully"))
                return redirect('/inventory-control/products')
            else:
                print(form.errors)

        if form_id == "consulting_service":
            content=Inventory.objects.filter(owner=owner, category=category, lang=lang)
            if content:
                get_formset = inlineformset_factory(
                    UserBase, Inventory, 
                    form=ConsultingForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, instance=owner, prefix='formset', queryset=Inventory.objects.filter(owner=owner, category=category, lang=lang))
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.owner = owner
                        data.category = category
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/slider_simple_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                get_formset = formset_factory(
                    form=ConsultingForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.owner = owner
                        data.category = category
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/slider_simple_form.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

@csrf_exempt               
def sendgridData(request, id, ig):
    ig_account=InstagramAccount.objects.get(asset_id=ig)
    if request.method == 'POST':
        action = request.POST.get('form-id')
        lang=request.LANGUAGE_CODE
        call = request.POST.get('action')
        print(action)
        print(call)

        if action == "sendgrid-form":
            site_cookie=SiteData(request)
            form = SendGridForm(request.POST)
            if form.is_valid():
                html_content = render_to_string('stela_control/emails-template/marketing/content-planner-email.html', {
                    'client':form.cleaned_data['client'],
                    'report':form.cleaned_data['message'],
                    'id_page':id,
                    'lang': lang,
                    'id_instagram':ig,
                    'date': timezone.now(),
                    'company': site_cookie.company_public()
                })

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                            form.cleaned_data['subject'],
                            text_content,
                            settings.STELA_EMAIL,
                            [form.cleaned_data['email']]
                                            
                        )
                email.attach_alternative(html_content, "text/html")
                email.send()
                return JsonResponse({'success':_('Your content grid was sent successfully')})
            else:
                print(form.errors)
                errors = form.errors.as_json()
                return JsonResponse({'alert': errors})
        
        if action == "sendmetric-form":
            site_cookie=SiteData(request)
            form = SendGridForm(request.POST)
            if form.is_valid():
                html_content = render_to_string('stela_control/emails-template/marketing/content-planner-email.html', {
                    'client':form.cleaned_data['client'],
                    'report':form.cleaned_data['message'],
                    'id_page':id,
                    'lang': lang,
                    'id_instagram':ig,
                    'company': site_cookie.company_public()
                })

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                            form.cleaned_data['subject'],
                            text_content,
                            settings.STELA_EMAIL,
                            [form.cleaned_data['email']]
                                            
                        )
                email.attach_alternative(html_content, "text/html")
                email.send()
                return JsonResponse({'success':_('Your IG Analyzer was sent successfully')})
            else:
                print(form.errors)
                errors = form.errors.as_json()
                return JsonResponse({'alert': errors})
        
        if call == "loadPages":
            get_timezone = request.POST.get('zone') 
            starts = int(request.POST.get('start'))
            ends = int(request.POST.get('ends'))
            new_posts = IGPost.objects.filter(parent=ig_account).order_by('-schedule')[starts:ends]
            new_pages = render_to_string('stela_control/load-data/meta/ig-new-pages.html', {
                    'newposts': new_posts,
                    'instagram': ig_account,
                    'usertz': get_timezone,
                    })
            return JsonResponse({'response': new_pages})

@csrf_exempt
def bookingData(request):
    if request.method == 'POST':
        owner=UserBase.objects.get(is_superuser=True)
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id, action)

        if action == "consulting_appointment":
            form=BookingConsultingForm(request.POST)
            if form.is_valid():
                booking_list = Booking.objects.filter(owner=owner, date=form.cleaned_data['schedule'])
                if booking_list.count() > 10:
                    return JsonResponse({'alert':_('There is no availability for the selected day, please choose another.')})  
                else:
                    data = Booking()
                    data.owner = owner
                    data.name = form.cleaned_data['name']
                    data.address = form.cleaned_data['address']
                    data.email = form.cleaned_data['email']
                    data.type = form.cleaned_data['type']
                    data.date = form.cleaned_data['schedule']
                    data.dateConfirm = True
                    data.save()
                    services = request.POST.getlist('services[]')
                    for service in services:
                        BookingServices.objects.create(
                            parent=data,
                            service=service
                        )
                    return JsonResponse({'success':_('Your appointment has been successfully scheduled.')})  

@csrf_exempt               
def inputsData(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        field_value = request.POST.get('field_value')
        field_name = request.POST.get('field_name')
        regex_patterns = {
            'name': r'^[a-zA-Z\s]+$',
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'address': r'.+', 
        }

        if action == "validateBillingData":
            
            pattern = regex_patterns.get(field_name)

            if pattern and re.fullmatch(pattern, field_value):

                response = JsonResponse ({'status': 'success'})
            else:
                response = JsonResponse ({
                    'status': 'error',
                    'field': field_name,
                    'message':_('The value entered in the field is not valid.')
                })

            return response


