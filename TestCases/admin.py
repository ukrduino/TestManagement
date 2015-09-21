from django.contrib import admin

from TestCases.models import *

admin.site.register(Job)
admin.site.register(JobBuild)
admin.site.register(TestGroup)
admin.site.register(TestClass)
admin.site.register(TestResult)
