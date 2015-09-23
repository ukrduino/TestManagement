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
    # set to avoid methods be at the same time in 'failed', 'skipped', and 'passed' groups
    unique_test_classes = set()

    failed_test_methods = soup.find_all(id="failedTest")
    if len(failed_test_methods) > 0:
        print(" >>>>> Saving FAILED TESTS ")
        for failed_test_method in failed_test_methods:
            failed_test_class_name = failed_test_method.contents[1].get_text().split(".")[1]
            if failed_test_class_name not in unique_test_classes:
                create_new_test_result(new_build, failed_test_class_name, "failed")
                unique_test_classes.add(failed_test_class_name)
            else:
                logger.info(" >>>>>> TEST RESULTS ERROR - Test class " + failed_test_class_name +
                            " has more then one failed result in build #" + str(build_number))


    skipped_test_methods = soup.find_all(id="skippedTest")
    if len(skipped_test_methods) > 0:
        print(" >>>>> Saving SKIPPED TESTS ")
        for skipped_test_method in skipped_test_methods:
            skipped_test_class_name = skipped_test_method.contents[1].get_text().split(".")[1]
            if skipped_test_class_name not in unique_test_classes:
                create_new_test_result(new_build, skipped_test_class_name, "skipped")
                unique_test_classes.add(skipped_test_class_name)


    passed_test_methods = soup.find_all(id="passedTest")
    if len(passed_test_methods) > 0:
        print(" >>>>> Saving PASSED TESTS ")
        for passed_test_method in passed_test_methods:
            passed_test_class_name = passed_test_method.contents[1].get_text().split(".")[1]
            if passed_test_class_name not in unique_test_classes:
                create_new_test_result(new_build, passed_test_class_name, "passed")
                unique_test_classes.add(passed_test_class_name)
            else:
                logger.info(" >>>>>> TEST RESULTS ERROR - Test class " + passed_test_class_name +
                            " already is in 'failed' or 'skipped' tests in build #" + str(build_number))

    html.close()
    os.remove(TARGET_DIR + "\\" + artifact_name)




