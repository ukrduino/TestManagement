from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^data_collection/$', 'TestCases.views.data_collection_page', name="data_collection"),
    url(r'^data_collection/parse_java_code/$', 'TestCases.views.parse_java_code', name="parse_java_code"),
    url(r'^data_collection/save_instances/$', 'TestCases.views.save_instances_to_db', name="save_instances_to_db"),
    url(r'^data_collection/get_jobs/$', 'TestCases.views.get_jobs_from_jenkins'),
    url(r'^data_collection/get_jobs_configs/$', 'TestCases.views.get_jobs_configs_from_jenkins'),
    url(r'^data_collection/get_builds_and_save_results/$', 'TestCases.views.get_builds_and_save_results'),
    url(r'^data_collection/delete/$', 'TestCases.views.delete'),
    url(r'^data_collection/update_progress_bar/$', 'TestCases.views.update_progress_bar'),
    url(r'^data_collection/update_time_stamps/$', 'TestCases.views.update_time_stamps'),


    url(r'^search_jobs/$', 'TestCases.views.search_jobs_page', name="search_jobs"),
    url(r'^search_jobs/by_groups/$', 'TestCases.views.search_jobs_by_group_name'),
    url(r'^search_jobs/by_job_name/$', 'TestCases.views.search_jobs_by_job_name'),
    url(r'^search_jobs/search_group/$', 'TestCases.views.search_group'),

    url(r'^jobs_configs/$', 'TestCases.views.jobs_configs_page', name='jobs_configs'),
    url(r'^jobs_configs/show_jobs_configs/$', 'TestCases.views.show_jobs_configs'),

    url(r'^$', 'TestCases.views.home', name="home"),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^jobs_results/$', 'TestCases.views.jobs_results_page', name="jobs_results_page"),
    url(r'^jobs_results/show_jobs_results/$', 'TestCases.views.show_jobs_results'),
    url(r'^jobs_results/load_data/$', 'TestCases.views.show_test_for_jobs'),

    url(r'^all_test_cases/$', 'TestCases.views.show_all_test_cases', name="show_all_test_cases"),
    url(r'^groups/$', 'TestCases.views.groups_page', name="groups_page"),
    url(r'^todo/$', 'TestCases.views.todo_page', name="todo_page"),
    url(r'new_todo/$', 'TestCases.views.new_todo', name='new_todo'),
    url(r'edit_todo/(?P<todo_id>\d+)$', 'TestCases.views.edit_todo_page', name='edit_todo_page'),
    url(r'edit_todo_save/(?P<todo_id>\d+)$', 'TestCases.views.edit_todo_save', name='edit_todo_save'),
]
