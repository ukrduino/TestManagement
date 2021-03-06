import json

from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, redirect, render

from TestCases.Parser import JavaTestsParser, JenkinsAPI
from TestCases.forms import *
from TestCases.models import *
from TestManagement.local_settings import *

logger = logging.getLogger(__name__)


def home(request):
    args = dict()
    args["test_cases_number"] = TestCase.objects.all().count()
    args["test_classes_number"] = TestClass.objects.all().count()
    args["jobs_number"] = Job.objects.all().count()
    args["groups_number"] = TestGroup.objects.all().count()
    args["builds_number"] = JobBuild.objects.all().count()
    return render(request, "HomePage.html", args)


# Data section
def data_collection_page(request):
    return render(request, "DataCollectionPage.html")


def delete(request):
    if request.method == 'POST':
        object_to_delete = request.POST['object_to_delete']
        if object_to_delete == "all tests":
            DataCollectionTimeStamps.objects.all().delete()
            init_data_collection_time_stamps()
            logger.info(" > cleaning DB (deleting Test classes and Test cases)")
            TestClass.objects.all().delete()
            TestCase.objects.all().delete()
        if object_to_delete == "all groups":
            logger.info(" > cleaning DB (deleting Groups)")
            TestGroup.objects.all().delete()
        if object_to_delete == "all jobs":
            logger.info(" > cleaning DB (deleting Jobs)")
            Job.objects.all().delete()
        if object_to_delete == "all builds and results":
            logger.info(" > cleaning DB (deleting JobBuilds, TestResult)")
            time_stamp = init_data_collection_time_stamps()
            JobBuild.objects.all().delete()
            TestResult.objects.all().delete()
            time_stamp.get_builds_and_save_results_acceptance = "no data"
            time_stamp.get_builds_and_save_results_new_trunk = "no data"
            time_stamp.save()
    return render(request, "DataCollectionPage.html")


# def super_update(request):
#     print(1)
#     logger.info(" > cleaning DB (deleting Test classes and Test cases)")
#     TestClass.objects.all().delete()
#     TestCase.objects.all().delete()
#     logger.info(" > cleaning DB (deleting Groups)")
#     TestGroup.objects.all().delete()
#     logger.info(" > cleaning DB (deleting Jobs)")
#     Job.objects.all().delete()
#     logger.info(" > cleaning DB (deleting JobBuilds, TestResult)")
#     JobBuild.objects.all().delete()
#     TestResult.objects.all().delete()
#     DataCollectionTimeStamps.objects.all().delete()
#     time_stamp = init_data_collection_time_stamps()
#     time_stamp.save()
#     print(2)
#     parse_java_code(request)
#     print(3)
#     save_instances_to_db(request)
#     print(4)
#     JenkinsAPI.get_jobs_from_jenkins(ACCEPTANCE_URL, EXCLUDED_ACCEPTANCE_JOBS, ACCEPTANCE)
#     time_stamp.get_jobs_acceptance = timezone.now().strftime("%d %b %H:%M")
#     time_stamp.save()
#     JenkinsAPI.get_jobs_from_jenkins(NEW_TRUNK_URL, EXCLUDED_NEW_TRUNK_JOBS, NEW_TRUNK)
#     time_stamp.get_jobs_new_trunk = timezone.now().strftime("%d %b %H:%M")
#     time_stamp.save()
#     JenkinsAPI.get_jobs_from_jenkins(ALL_OTHER_URL, EXCLUDED_ALL_OTHER_JOBS, ALL_OTHER)
#     time_stamp.get_jobs_all_other = timezone.now().strftime("%d %b %H:%M")
#     time_stamp.save()
#     JenkinsAPI.add_config_data_to_jobs(ACCEPTANCE)
#     time_stamp.get_jobs_configs_acceptance = timezone.now().strftime("%d %b %H:%M")
#     time_stamp.save()
#     JenkinsAPI.add_config_data_to_jobs(NEW_TRUNK)
#     time_stamp.get_jobs_configs_new_trunk = timezone.now().strftime("%d %b %H:%M")
#     time_stamp.save()
#     # JenkinsAPI.add_config_data_to_jobs(ALL_OTHER)
#     # time_stamp.get_jobs_configs_all_other = timezone.now().strftime("%d %b %H:%M")
#     # time_stamp.save()
#     JenkinsAPI.get_build_results_from_jenkins(ACCEPTANCE)
#     time_stamp.get_builds_and_save_results_acceptance = timezone.now().strftime("%d %b %H:%M")
#     time_stamp.save()
#     JenkinsAPI.get_build_results_from_jenkins(NEW_TRUNK)
#     time_stamp.get_builds_and_save_results_new_trunk = timezone.now().strftime("%d %b %H:%M")
#     time_stamp.save()
#     return render(request, "DataCollectionPage.html")


def parse_java_code(request):
    DataCollectionTimeStamps.objects.all().delete()
    time_stamp = init_data_collection_time_stamps()
    JavaTestsParser.get_tests_headers_from_java_code()
    time_stamp.parse_java_code = timezone.now().strftime("%d %b %H:%M")
    time_stamp.save()
    return render(request, "DataCollectionPage.html")


def save_instances_to_db(request):
    time_stamp = init_data_collection_time_stamps()
    JavaTestsParser.create_instances_and_put_to_db()
    time_stamp.save_instances_to_db = timezone.now().strftime("%d %b %H:%M")
    time_stamp.save()
    return render(request, "DataCollectionPage.html")


def get_jobs_from_jenkins(request):
    time_stamp = init_data_collection_time_stamps()
    if request.method == 'POST':
        jenkins_page = request.POST['jenkins_page']
        if jenkins_page == ACCEPTANCE:
            JenkinsAPI.get_jobs_from_jenkins(ACCEPTANCE_URL, EXCLUDED_ACCEPTANCE_JOBS, ACCEPTANCE)
            time_stamp.get_jobs_acceptance = timezone.now().strftime("%d %b %H:%M")
        if jenkins_page == NEW_TRUNK:
            JenkinsAPI.get_jobs_from_jenkins(NEW_TRUNK_URL, EXCLUDED_NEW_TRUNK_JOBS, NEW_TRUNK)
            time_stamp.get_jobs_new_trunk = timezone.now().strftime("%d %b %H:%M")
        if jenkins_page == ALL_OTHER:
            JenkinsAPI.get_jobs_from_jenkins(ALL_OTHER_URL, EXCLUDED_ALL_OTHER_JOBS, ALL_OTHER)
            time_stamp.get_jobs_all_other = timezone.now().strftime("%d %b %H:%M")
        time_stamp.save()
    return render(request, "DataCollectionPage.html")


def get_jobs_configs_from_jenkins(request):
    if request.method == 'POST':
        time_stamp = init_data_collection_time_stamps()
        jenkins_page = request.POST['jenkins_page']
        if jenkins_page == ACCEPTANCE:
            JenkinsAPI.add_config_data_to_jobs(ACCEPTANCE)
            time_stamp.get_jobs_configs_acceptance = timezone.now().strftime("%d %b %H:%M")
        if jenkins_page == NEW_TRUNK:
            JenkinsAPI.add_config_data_to_jobs(NEW_TRUNK)
            time_stamp.get_jobs_configs_new_trunk = timezone.now().strftime("%d %b %H:%M")
        if jenkins_page == ALL_OTHER:
            JenkinsAPI.add_config_data_to_jobs(ALL_OTHER)
            time_stamp.get_jobs_configs_all_other = timezone.now().strftime("%d %b %H:%M")
        time_stamp.save()
    return render(request, "DataCollectionPage.html")


def get_builds_and_save_results(request):
    if request.method == 'POST':
        time_stamp = init_data_collection_time_stamps()
        jenkins_page = request.POST['jenkins_page']
        if jenkins_page == ACCEPTANCE:
            JenkinsAPI.get_build_results_from_jenkins(ACCEPTANCE)
            time_stamp.get_builds_and_save_results_acceptance = timezone.now().strftime("%d %b %H:%M")
        if jenkins_page == NEW_TRUNK:
            JenkinsAPI.get_build_results_from_jenkins(NEW_TRUNK)
            time_stamp.get_builds_and_save_results_new_trunk = timezone.now().strftime("%d %b %H:%M")
        time_stamp.save()
    return render(request, "DataCollectionPage.html")


def search_jobs_page(request):
    return render(request, "JOBS_SEARCH_PAGE/SearchJobsPage.html")


def search_jobs_by_group_name(request):
    args = dict()
    args['found_jobs_list'] = search_jobs(request, BY_GROUP_NAME)
    return render(request, "JOBS_SEARCH_PAGE/JobsForSearchJobsPage.html", args)


def search_jobs_by_job_name(request):
    args = dict()
    args['found_jobs_list'] = search_jobs(request, BY_JOB_NAME)
    return render(request, "JOBS_SEARCH_PAGE/JobsForSearchJobsPage.html", args)


def search_jobs(request, by):
    if request.method == 'POST':
        if by == BY_GROUP_NAME:
            jobs_set = set()
            group_names = request.POST['search_text']
            group_names_list = group_names.replace(" ", "").split(",")
            if len(group_names_list) > 0:
                for group_name in group_names_list:
                    jobs = Job.objects.filter(testgroup__test_group_name=group_name)
                    jobs_set.update(jobs)
                return jobs_set
        if by == BY_JOB_NAME:
            jobs_set = set()
            job_names = request.POST['search_text']
            if len(job_names) > 0:
                jobs = Job.objects.filter(job_name__contains=job_names)
                jobs_set.update(jobs)
                return jobs_set


def search_group(request):
    args = dict()
    groups_set = set()
    if request.method == 'POST':
        group_name = request.POST['search_text']
        if len(group_name) > 0:
            groups = TestGroup.objects.filter(test_group_name__contains=group_name)
            groups_set.update(groups)
            args['found_groups_list'] = groups_set
    return render(request, "JOBS_SEARCH_PAGE/GroupsForSearchJobsPage.html", args)


# JOBS RESULTS PAGE
def jobs_results_page(request):
    return render(request, "JOBS_PAGE/JobsPage.html")


def show_jobs_results(request):
    args = dict()
    jobs_with_builds = dict()
    if request.method == 'POST':
        jenkins_page = request.POST['jenkins_page']
        for job in Job.objects.filter(job_jenkins_page=jenkins_page):
            jobs_with_builds[job] = JobBuild.objects.filter(job__id=job.id).order_by('build_number')
    args['jobs_with_builds'] = jobs_with_builds
    return render(request, "JOBS_PAGE/JobsForJobsPage.html", args)


def show_test_for_jobs(request):
    args = dict()
    if request.method == 'POST':
        job_id = request.POST['job_id']
        builds = JobBuild.objects.filter(job__id=job_id).order_by('build_number')
        # set of tests for Job
        tests_for_job_set = find_tests_for_job_from_builds(builds)
        tests_with_results = list()
        # get results for each test
        for test in tests_for_job_set:
            results_for_test = list()
            for build in builds:
                result = TestResult.objects.filter(build__id=build.id)
                result_present = False
                for res in result:
                    if res.test_class.id == test.id:
                        results_for_test.append(res)
                        result_present = True
                        break
                # if test has no result for this build we creating blank result
                if not result_present:
                    new_test_result = TestResult(test_class=test,
                                                 build=build,
                                                 test_passed="absent",
                                                 test_stack_trace="")
                    results_for_test.append(new_test_result)
            tests_with_results.append({"test": test,
                                       "test_cases": TestCase.objects.filter(test_case_class=test),
                                       "test_name": test.test_class_name,
                                       "test_results": results_for_test})
        args['tests_with_results'] = tests_with_results
    return render(request, "JOBS_PAGE/TestsForJobsPage.html", args)


def find_tests_for_job_from_builds(builds):
    tests_for_job_set = set()
    for build in builds:
        results_for_build = TestResult.objects.filter(build__id=build.id)
        for result in results_for_build:
            test = TestClass.objects.get(id=result.test_class.id)
            tests_for_job_set.add(test)
    return tests_for_job_set


# JOBS CONFIGS PAGE
def jobs_configs_page(request):
    return render(request, "JOBS_CONFIGS_PAGE/JobsConfigsPage.html")


# # GROUPS INFO PAGE
def groups_page(request):
    args = dict()
    args['acceptance_groups'] = [group.test_group_name for group in TestGroup.objects.filter(job__job_jenkins_page=ACCEPTANCE)]
    args['new_trunk_groups'] = [group.test_group_name for group in TestGroup.objects.filter(job__job_jenkins_page=NEW_TRUNK)]
    all_other_groups = [group.test_group_name for group in TestGroup.objects.filter(job__job_jenkins_page=ALL_OTHER)]
    args['all_other_groups'] = list()
    for group_name in all_other_groups:
        if group_name not in args['acceptance_groups']:
            if group_name not in args['new_trunk_groups']:
                args['all_other_groups'].append(group_name)
    no_jobs_groups = [group.test_group_name for group in TestGroup.objects.filter(job=None)]
    args['no_jobs_groups'] = list()
    for group_name in no_jobs_groups:
        if group_name not in args['acceptance_groups']:
            if group_name not in args['new_trunk_groups']:
                if group_name not in args['all_other_groups']:
                    args['no_jobs_groups'].append(group_name)

    return render(request, "GroupsPage.html", args)


def show_jobs_configs(request):
    args = dict()
    if request.method == 'POST':
        jenkins_page = request.POST['jenkins_page']
        args["jobs"] = Job.objects.filter(job_jenkins_page=jenkins_page)
    return render(request, "JOBS_CONFIGS_PAGE/JobForJobsConfigsPage.html", args)


# TODO REFACTORING
def show_all_disabled_test_cases(request):
    args = dict()
    test_case_with_test_class = dict()
    for test_case in TestCase.objects.all()[555:600]:
        test_class = TestClass.objects.get(testcase__id=test_case.id)
        groups = TestGroup.objects.filter(testclass__id=test_class.id)
        test_class_with_groups = dict()
        test_class_with_groups[test_class] = groups
        test_case_with_test_class[test_case] = test_class_with_groups
    args["test_case_with_test_class"] = test_case_with_test_class
    return render(request, "TEST_CLASSES_PAGE/TestClassesPage.html", args)


# http://stackoverflow.com/a/32466453
def update_progress_bar(request):
    if request.method == 'POST':
        progress_bar = ProgressBar.objects.last()
        resp = {'current_val': progress_bar.progress_bar_current_val,
                'max_val': progress_bar.progress_bar_max_val,
                }
        return HttpResponse(json.dumps(resp))


# http://stackoverflow.com/a/9942455
def update_time_stamps(request):
    resp = dict()
    time_stamp_fields_dict = DataCollectionTimeStamps.objects.last().__dict__
    for field, stored_data in time_stamp_fields_dict.items():
        if field != "_state" and field != "id":
            resp[field] = stored_data
    return HttpResponse(json.dumps(resp))


def todo_page(request):
    args = dict()
    args['form'] = CreateToDoNoteForm
    args["to_do_notes"] = ToDoNote.objects.all().order_by('-id')
    return render(request, "TODO_PAGE/ToDoPage.html", args)


def new_todo(request):
    if request.method == 'POST':
        form = CreateToDoNoteForm(request.POST)
        if form.is_valid():
            add = form.save(commit=False)
            add.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def edit_todo_page(request, todo_id):
    args = dict()
    to_do_note = ToDoNote.objects.get(id=todo_id)
    args['form'] = EditToDoNoteForm(instance=to_do_note)
    args["to_do_note"] = to_do_note
    return render(request, "TODO_PAGE/EditToDoPage.html", args)


def edit_todo_save(request, todo_id):
    instance = ToDoNote.objects.get(id=todo_id)
    form = EditToDoNoteForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('todo_page')
    return edit_todo_page(request, todo_id)
