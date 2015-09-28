from django.shortcuts import render_to_response
from django.template import RequestContext

from TestCases.Parser import JavaTestsParser, JenkinsAPI
from TestCases.models import *

logger = logging.getLogger(__name__)


# Site section
def show_acceptance_jobs(request):

    args = dict()
    jobs_with_builds = dict()
    for job in Job.objects.all():
        jobs_with_builds[job] = JobBuild.objects.filter(job__id=job.id).order_by('build_number')
    args['jobs_with_builds'] = jobs_with_builds
    return render_to_response("AcceptanceJobsPage.html", args, context_instance=RequestContext(request))


def show_test_for_jobs(request):  # TODO pass data in ajax dictionary
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
    return render_to_response("TestsForAcceptanceJobsPage.html", args, context_instance=RequestContext(request))


def find_tests_for_job_from_builds(builds):
    tests_for_job = set()
    for build in builds:
        results_for_build = TestResult.objects.filter(build__id=build.id)
        for result in results_for_build:
            test = TestClass.objects.get(id=result.test_class.id)
            tests_for_job.add(test)
    return tests_for_job

    # jobs_with_groups_tests_results = dict()
    # for jenkins_job in Job.objects.all():
    #     build_with_tests = dict()
    #     for buid in JobBuild.objects.filter(job__id=jenkins_job.id):
    #         tests_with_results = dict()
    #         for test in TestClass.objects.filter(test_case_group__id=group.id):
    #             results = TestResult.objects.filter(test_case__id=test.id)
    #             results_for_template = list()
    #             for build in jobs_with_builds[jenkins_job]:
    #                 not_run = True
    #                 for res in results:
    #                     if build.id == res.build.id:
    #                         if res.test_passed:
    #                             results_for_template.append("pass")
    #                             not_run = False
    #                             break
    #                         else:
    #                             results_for_template.append("fail")
    #                             not_run = False
    #                             break
    #                 if not_run:
    #                     results_for_template.append("N/R")
    #             tests_with_results[test] = results_for_template
    #         groups_with_tests[group] = tests_with_results
    #     jobs_with_groups_tests_results[jenkins_job] = groups_with_tests
    # args['jobs_with_groups_tests_results'] = jobs_with_groups_tests_results


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
    return render_to_response("TestCases.html", args, context_instance=RequestContext(request))


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
    JenkinsAPI.get_acceptance_results_from_jenkins()
    return render_to_response("HomePage.html", context_instance=RequestContext(request))


def get_job_configs_from_jenkins(request):
    JenkinsAPI.add_acceptance_groups_to_jobs()
    return render_to_response("HomePage.html", context_instance=RequestContext(request))


def search_jobs_page(request):
    return render_to_response("JobsPage.html", context_instance=RequestContext(request))


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
            args['found_jobs_list'] = list(jobs_set)
    return render_to_response("JobsForJobsPage.html", args, context_instance=RequestContext(request))
