from django.shortcuts import render_to_response
from django.template import RequestContext

from TestCases.Parser import JavaTestsParser, JenkinsAPI
from TestCases.models import *

logger = logging.getLogger(__name__)





def show_all_test_cases(request):
    args = dict()
    test_case_with_test_class = dict()
    for test_case in TestCase.objects.all()[555:600]:
        test_class = TestClass.objects.get(testcase__id=test_case.id)
        groups = TestGroup.objects.filter(testclass__id=test_class.id)
        test_class_with_groups = dict()
        test_class_with_groups[test_class] = groups
        test_case_with_test_class[test_case] = test_class_with_groups
    args["test_case_with_test_class"] = test_case_with_test_class
    return render_to_response("TEST_CLASSES_PAGE/TestClassesPage.html", args, context_instance=RequestContext(request))


def home(request):
    args = dict()
    args["test_cases_number"] = TestCase.objects.all().count()
    args["test_classes_number"] = TestClass.objects.all().count()
    args["jobs_number"] = Job.objects.all().count()
    args["builds_number"] = JobBuild.objects.all().count()
    return render_to_response("HomePage.html", args, context_instance=RequestContext(request))


# Data section
def parse_java_code(request):
    JavaTestsParser.get_tests_headers_from_java_code()
    return render_to_response("HomePage.html", context_instance=RequestContext(request))


def save_instances_to_db(request):
    JavaTestsParser.create_instances_and_put_to_db()
    return render_to_response("HomePage.html", context_instance=RequestContext(request))


def get_builds_info_from_jenkins(request):
    JenkinsAPI.get_builds_info_from_jenkins()
    return render_to_response("HomePage.html", context_instance=RequestContext(request))


def get_acceptance_job_configs_from_jenkins(request):
    JenkinsAPI.get_acceptance_job_configs_from_jenkins()
    return render_to_response("HomePage.html", context_instance=RequestContext(request))


def get_trunk_job_configs_from_jenkins(request):
    JenkinsAPI.get_trunk_job_configs_from_jenkins()
    return render_to_response("HomePage.html", context_instance=RequestContext(request))


def search_jobs_page(request):
    return render_to_response("JOBS_SEARCH_PAGE/SearchJobsPage.html", context_instance=RequestContext(request))


def search_jobs_by_groups(request):
    args = dict()
    jobs_set = set()
    if request.method == 'POST':
        group_names = request.POST['search_text']
        group_names_list = group_names.replace(" ", "").split(",")
        if len(group_names_list) > 0:
            for group_name in group_names_list:
                jobs = Job.objects.filter(testgroup__test_group_name=group_name)
                jobs_set.update(jobs)
            args['found_jobs_list'] = jobs_set
    return render_to_response("JOBS_SEARCH_PAGE/JobsForSearchJobsPage.html", args, context_instance=RequestContext(request))


def search_group(request):
    args = dict()
    groups_set = set()
    if request.method == 'POST':
        group_name = request.POST['search_text']
        print(group_name)
        if len(group_name) > 0:
            groups = TestGroup.objects.filter(test_group_name__contains=group_name)
            # print(groups)
            groups_set.update(groups)
            args['found_groups_list'] = groups_set
            print(args['found_groups_list'])
    return render_to_response("JOBS_SEARCH_PAGE/GroupsForSearchJobsPage.html", args, context_instance=RequestContext(request))


def data_collection_page(request):
    return render_to_response("DataCollectionPage.html", context_instance=RequestContext(request))


# JOBS PAGE

# JOBS CONFIGS PAGE
def jobs_jobs_page(request):
    return render_to_response("Jo.html", context_instance=RequestContext(request))

def show_acceptance_jobs(request):
    args = dict()
    jobs_with_builds = dict()
    for job in Job.objects.all():
        jobs_with_builds[job] = JobBuild.objects.filter(job__id=job.id).order_by('build_number')
    args['jobs_with_builds'] = jobs_with_builds
    return render_to_response("JOBS_PAGE/JobsPage.html", args, context_instance=RequestContext(request))


def show_test_for_jobs(request):
    args = dict()
    if request.method == 'POST':
        job_id = request.POST['job_id']
        builds = JobBuild.objects.filter(job__id=job_id).order_by('build_number')
        tests_for_job = find_tests_for_job_from_builds(builds)
        tests_with_results = dict()
        for test in tests_for_job:
            results_for_test = list()
            for build in builds:
                result = TestResult.objects.filter(build__id=build.id)
                for res in result:
                    if res.test_class.id == test.id:
                        results_for_test.append(res)
            tests_with_results[test] = results_for_test
        args['tests_with_results'] = tests_with_results
    return render_to_response("JOBS_PAGE/TestsForJobsPage.html", args, context_instance=RequestContext(request))


def find_tests_for_job_from_builds(builds):
    tests_for_job = set()
    for build in builds:
        results_for_build = TestResult.objects.filter(build__id=build.id)
        for result in results_for_build:
            test = TestClass.objects.get(id=result.test_class.id)
            tests_for_job.add(test)
    return tests_for_job


# JOBS CONFIGS PAGE
def jobs_configs_page(request):
    return render_to_response("JOBS_CONFIGS_PAGE/JobsConfigsPage.html", context_instance=RequestContext(request))


def show_jobs_configs(request):
    args = dict()
    if request.method == 'POST':
        jenkins_page = request.POST['jenkins_page']
        args["jobs"] = Job.objects.filter(job_jenkins_page=jenkins_page)
    return render_to_response("JOBS_CONFIGS_PAGE/JobForJobsConfigsPage.html", args, context_instance=RequestContext(request))
