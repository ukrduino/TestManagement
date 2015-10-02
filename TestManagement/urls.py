from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^data_collection/save_instances/$', 'TestCases.views.save_instances_to_db', name="save_instances_to_db"),
    url(r'^data_collection/parse_java_code/$', 'TestCases.views.parse_java_code', name="parse_java_code"),
    url(r'^acceptance_jobs/$', 'TestCases.views.show_acceptance_jobs', name="show_acceptance_jobs"),
    url(r'^acceptance_jobs/load_data/$', 'TestCases.views.show_test_for_jobs', name="load_data"),
    url(r'^search_jobs/$', 'TestCases.views.search_jobs_page', name="search_jobs"),
    url(r'^search_jobs/by_groups/$', 'TestCases.views.search_jobs_by_groups'),
    url(r'^search_jobs/search_group/$', 'TestCases.views.search_group'),
    url(r'^all_test_cases/$', 'TestCases.views.show_all_test_cases', name="show_all_test_cases"),
    url(r'^data_collection/$', 'TestCases.views.data_collection_page', name="data_collection"),
    url(r'^data_collection/get_builds_info_from_jenkins/$', 'TestCases.views.get_builds_info_from_jenkins'),
    url(r'^data_collection/get_acceptance_job_configs_from_jenkins/$', 'TestCases.views.'
                                                                       'get_acceptance_job_configs_from_jenkins'),
    url(r'^data_collection/get_trunk_job_configs_from_jenkins/$', 'TestCases.views.get_trunk_job_configs_from_jenkins'),
    url(r'^jobs_configs/$', 'TestCases.views.jobs_configs_page', name='jobs_configs'),
    url(r'^jobs_configs/show_jobs_configs/$', 'TestCases.views.show_jobs_configs'),
    url(r'^$', 'TestCases.views.home', name="home"),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
        import debug_toolbar
        urlpatterns += patterns('',
                                url(r'^__debug__/', include(debug_toolbar.urls)),
                                )
