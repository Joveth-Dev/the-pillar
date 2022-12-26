# class MiddleInitialFilter(admin.SimpleListFilter):
#     """- a custom filter for 'middle_initial' field"""
#     title = 'middle Initial'
#     parameter_name = 'middle_initial'

#     def lookups(self, request, model_admin):
#         return [
#             ('A-E', 'A-E'),
#             ('F-J', 'F-J'),
#             ('K-O', 'K-O'),
#             ('P-T', 'P-T'),
#             ('U-Z', 'U-Z')
#         ]

#     def queryset(self, request, queryset):
#         if self.value() == 'A-E':
#             return queryset.filter(middle_initial__in='ABCDE')
#         elif self.value() == 'F-J':
#             return queryset.filter(middle_initial__in='FGHIJ')
#         elif self.value() == 'K-O':
#             return queryset.filter(middle_initial__in='KLMNO')
#         elif self.value() == 'P-T':
#             return queryset.filter(middle_initial__in='PQRST')
#         elif self.value() == 'U-Z':
#             return queryset.filter(middle_initial__in='UVWXYZ')

# class UserDetail(RetrieveUpdateDestroyAPIView):
#     # needed: constrain so that they can only view, delete,
#     # and update their own account profile, so as edit it.
#     verified_cur_user = True
#     queryset = User.objects.filter(is_active=True)
#     serializer_class = UserSerializer

#     def get_queryset(self):
#         if self.request.user.id == self.kwargs['pk']:
#             return super().get_queryset()
#         else:
#             self.verified_cur_user = False
#             return self.http_method_not_allowed

#     def get_serializer_context(self):
#         return {'request': self.request}

#     def put(self, request, *args, **kwargs):
#         self.get_queryset()
#         if self.verified_cur_user == False:
#             return Response({'error': "Action denied. Please keep away from anyone else's account🙇."},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         return super().put(request, *args, **kwargs)

#     def patch(self, request, *args, **kwargs):
#         self.get_queryset()
#         if self.verified_cur_user == False:
#             return Response({'error': "Action denied. Please keep away from anyone else's account🙇."},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         return super().patch(request, *args, **kwargs)

#     def delete(self, request, pk):
#         self.get_queryset()
#         # not deleting the user
#         if self.verified_cur_user == False:
#             return Response({'error': "Action denied. Please keep away from anyone else's account🙇."},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         else:
#             user = get_object_or_404(User, pk=pk)
#             user.is_active = False  # update is_active to False
#             user.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)


# class StudentInline(admin.StackedInline):
#     autocomplete_fields = ['college', 'degree_program']
#     model = Student
#     verbose_name = 'Student Information'


# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     fieldsets = (
#         (None, {"fields": ("username", "password")}),
#         (("Personal info"), {"fields": ("first_name",
#          "last_name", 'middle_initial', 'is_student', "email", 'profile_image', 'thumbnail', 'birth_date', 'sex')}),
#         (
#             ("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     # "groups",
#                     "user_permissions",
#                 ),
#             },
#         ),
#         (("Important dates"), {"fields": ("last_login", "date_joined")}),
#     )
#     inlines = [StudentInline]
#     list_display = ['profile', "username", "first_name", "last_name", 'MI', 'SEX',
#                     "email", "is_staff", 'is_student', 'date_joined', 'date_updated', "is_active"]
#     list_filter = ["is_staff", "is_active", MiddleInitialFilter,
#                    'date_joined', 'date_updated']
#     list_per_page = 10
#     ordering = ['date_joined']
#     readonly_fields = ['thumbnail']
#     search_fields = ("username__istartswith", "first_name__istartswith",
#                      "last_name__istartswith", "email__istartswith", "middle_initial__iexact")

#     @admin.display(ordering='middle_initial')
#     def MI(self, user):
#         return user.middle_initial

#     @admin.display(ordering='sex')
#     def SEX(self, user):
#         if user.sex == 'M':
#             return 'M'
#         else:
#             return 'F'

#     def thumbnail(self, instance):
#         if instance.profile_image.name != '':
#             return format_html(f'<img src="{instance.profile_image.url}" class="thumbnail"/>')
#         return 'No Profile Yet'

#     def profile(self, instance):
#         if instance.profile_image.name != '':
#             return format_html(f'<img src="{instance.profile_image.url}" class="profile"/>')
#         return 'No Profile Yet'

#     def get_queryset(self, request):
#         return super().get_queryset(request)

#     class Media:
#         css = {
#             'all': ['publication/styles.css']
#         }

# def save_formset(self, request, form, formset, change):
#     formset.save()
#     if form.instance.is_approved:
#         for obj in formset.forms:
#             article = obj.instance
#             article.is_approved = True
#             article.date_updated = datetime.now()
#             return super().save_formset(request, form, formset, change)
#     elif not form.instance.is_approved:
#         for obj in formset.forms:
#             article = obj.instance
#             article.is_approved = False
#             article.date_updated = datetime.now()
#             return super().save_formset(request, form, formset, change)


#  @admin.action(description='Approve selected issues')
# def approve(self, request, queryset):
#     updated_issue_count = queryset.update(is_approved=True)
#     updated_article_count = 0
#     for obj in queryset:
#         updated_article_count += models.Article.objects.filter(
#             issue_id=obj.id).update(is_approved=True, date_updated=datetime.now())
#     self.message_user(
#         request,
#         f'{updated_issue_count} issues and {updated_article_count} articles were successfully updated.'
#     )

# class Account(models.Model):
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, primary_key=True)
#     # birth_date = models.DateField(null=True)
#     # sex = models.CharField(max_length=1, choices=SEX_CHOICES)
#     date_updated = models.DateTimeField(auto_now=True)

#     def __str__(self) -> str:
#         return str(self.user.get_full_name())

# EDITOR_IN_CHIEF = 'EIC'
# ASSOCIATE_EDITOR = 'AE'
# MANAGING_EDITOR = 'ME'
# NEWS_EDITOR = 'NE'
# FEATURE_EDITOR = 'FE'
# CULTURE_EDITOR = 'CE'
# STAFF_WRITTERS = 'SW'
# CARTOONIST = 'CT'
# PHOTOJOURNALIST = 'PJ'
# LAYOUT_ARTIST = 'LA'
# FINANCIAL_MANAGER = 'FM'
# ASSISTANT_FINANCIAL_MANAGER = 'AFM'
# FINANCIAL_ADVISER = 'FA'
# TECHNICAL_ADVISER = 'TA'

# POSITION_CHOICES = [
#     (EDITOR_IN_CHIEF, 'Editor-in-chief'),
#     (ASSOCIATE_EDITOR, 'Associate Editor'),
#     (MANAGING_EDITOR, 'Managing Editor'),
#     (NEWS_EDITOR, 'News Editor'),
#     (FEATURE_EDITOR, 'Feature Editor'),
#     (CULTURE_EDITOR, 'Culture Editor'),
#     (STAFF_WRITTERS, 'Staff Writter'),
#     (CARTOONIST, 'Cartoonist'),
#     (PHOTOJOURNALIST, 'Photojournalist'),
#     (LAYOUT_ARTIST, 'Layout Artist'),
#     (FINANCIAL_MANAGER, 'Financial Manager'),
#     (ASSISTANT_FINANCIAL_MANAGER, 'Assistant Financial Manager'),
#     (FINANCIAL_ADVISER, 'Financial Adviser'),
#     (TECHNICAL_ADVISER, 'Technical Adviser')
# ]

# class PositionFilter(admin.SimpleListFilter):
#     title = 'Position'
#     parameter_name = 'position'

#     def lookups(self, request, model_admin):
#         return [
#             ('EIC', 'Editor-in-Chief'),
#             ('AE', 'Associate Editor'),
#             ('ME', 'Managing Editor'),
#             ('NE', 'News Editor'),
#             ('FE', 'Feature Editor'),
#             ('CE', 'Culture Editor'),
#             ('SW', 'Staff Writter'),
#             ('CT', 'Cartoonist'),
#             ('PJ', 'Photojournalist'),
#             ('LA', 'Layout Artist'),
#             ('FM', 'Financial Manager'),
#             ('AFM', 'Assistant Financial Manager'),
#             ('FA', 'Financial Adviser'),
#             ('TA', 'Technical Adviser'),
#         ]

#     def queryset(self, request, queryset):
#         if self.value() == 'EIC':
#             return queryset.filter(memberposition__position__title='Editor-in-Chief')
#         elif self.value() == 'AE':
#             return queryset.filter(memberposition__position__title='Associate Editor')
#         elif self.value() == 'ME':
#             return queryset.filter(memberposition__position__title='Managing Editor')
#         elif self.value() == 'NE':
#             return queryset.gfilteret(memberposition__position__title='News Editor')
#         elif self.value() == 'FE':
#             return queryset.filter(memberposition__position__title='Feature Editor')
#         elif self.value() == 'CE':
#             return queryset.filter(memberposition__position__title='Culture Editor')
#         elif self.value() == 'SW':
#             return queryset.filter(memberposition__position__title='Staff Writter')
#         elif self.value() == 'CT':
#             return queryset.filter(memberposition__position__title='Cartoonist')
#         elif self.value() == 'PJ':
#             return queryset.filter(memberposition__position__title='Photojournalist')
#         elif self.value() == 'LA':
#             return queryset.filter(memberposition__position__title='Layout Artist')
#         elif self.value() == 'FM':
#             return queryset.filter(memberposition__position__title='Financial Manager')
#         elif self.value() == 'AFM':
#             return queryset.filter(memberposition__position__title='Assistant Financial Manager')
#         elif self.value() == 'FA':
#             return queryset.filter(memberposition__position__title='Financial Adviser')
#         elif self.value() == 'TA':
#             return queryset.filter(memberposition__position__title='Technical Adviser')


# class Log(models.Model):
#     AC = 'AC'
#     ArC = 'ArC'
#     IC = 'IC'
#     MC = 'MC'
#     AU = 'AU'
#     ArU = 'ArU'
#     IU = 'IU'
#     MU = 'MU'
#     DECRIPTION_CHOICES = [
#         (AC, 'Account Created'),
#         (ArC, 'Article Created'),
#         (IC, 'Issue Created'),
#         (MC, 'Member Created'),
#         (AU, 'Account Updated'),
#         (ArU, 'Article Updated'),
#         (IU, 'Issue Updated'),
#         (MU, 'Member Updated'),
#     ]

#     user = models.ForeignKey(
#         Account, on_delete=models.PROTECT)
#     datetime = models.DateTimeField(auto_now_add=True)
#     description = models.CharField(max_length=3, choices=DECRIPTION_CHOICES)
