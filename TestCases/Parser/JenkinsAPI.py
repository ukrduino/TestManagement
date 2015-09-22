import os

from jenkinsapi.jenkins import Jenkins

from bs4 import BeautifulSoup

from TestCases.models import *
from TestManagement.local_settings import *

logger = logging.getLogger(__name__)


def get_server_instance():
    jenkins_url = JENKINS_URL
    server = Jenkins(jenkins_url, username=USER_NAME, password=PASSWORD)
    return server


def get_results_from_jenkins():
    # cleaning DB
    Job.objects.all().delete()
    JobBuild.objects.all().delete()
    TestResult.objects.all().delete()
    print(" > Lets Get info from uncle Jenkins")
    server = get_server_instance()
    # opening acceptance view
    job_from_view = server.get_view_by_url(JENKINS_URL + ACCEPTANCE_URL)
    # getting all jobs from view
    jobs = job_from_view.get_job_dict()
    print(" >> We have - " + str(len(jobs) - len(EXCLUDED_ACCEPTANCE_JOBS)) + " jobs in Acceptance")
    for job_title, job_link in jobs.items():
        # filtering jobs
        if job_title not in EXCLUDED_ACCEPTANCE_JOBS:
            job_inst = server.get_job(job_title)
            # creating new job
            new_job = create_new_job(job_title)
            # getting builds for job
            builds = job_inst.get_build_dict()
            for build_number, build_link in builds.items():
                process_build_data(job_inst, new_job, build_number)


def process_build_data(job_inst, new_job, build_number):
    build_inst = job_inst.get_build(build_number)
    # filtering builds that have artifacts
    artifacts = build_inst.get_artifact_dict()
    for artifact_name, artifact in artifacts.items():
        if artifact_name == "custom-report.html":
            save_artifact(artifact)
            process_artifact(new_job, build_number, artifact_name)


def save_artifact(artifact):
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
    artifact.save_to_dir(TARGET_DIR)


def process_artifact(new_job, build_number, artifact_name):
    # creating new build
    new_build = create_new_build(new_job, build_number)
    html = open(TARGET_DIR + "\\" + artifact_name)
    soup = BeautifulSoup(html, 'html.parser')
    test_methods = soup.find_all(id="failedTest")
    test_classes = set()
    if len(test_methods) > 0:
        print(" >>>>> Saving FAILED TESTS ")
        for method in test_methods:
            test_class_name = method.contents[1].get_text().split(".")[1]
            create_new_test_result(new_build, test_class_name, "failed")
            test_classes.add(test_class_name)
    test_methods = soup.find_all(id="skippedTest")
    if len(test_methods) > 0:
        print(" >>>>> Saving SKIPPED TESTS ")
        for method in test_methods:
            test_class_name = method.contents[1].get_text().split(".")[1]
            if test_class_name not in test_classes:
                create_new_test_result(new_build, test_class_name, "skipped")
                test_classes.add(test_class_name)
            else:
                logger.info(" >>>>>> ERROR - Test class " + test_class_name + "found in 'Failed' tests")
    test_methods = soup.find_all(id="passedTest")
    if len(test_methods) > 0:
        print(" >>>>> Saving PASSED TESTS ")
        for method in test_methods:
            test_class_name = method.contents[1].get_text().split(".")[1]
            if test_class_name not in test_classes:
                create_new_test_result(new_build, test_class_name, "passed")
            else:
                logger.info(" >>>>>> ERROR - Test class " + test_class_name + "found in 'Failed' or 'Skipped' tests")
    html.close()
    os.remove(TARGET_DIR + "\\" + artifact_name)




