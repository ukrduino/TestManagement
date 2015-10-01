import re

from jenkinsapi.jenkins import Jenkins
from bs4 import BeautifulSoup
from selenium import webdriver
import untangle

from TestManagement.local_settings import *
from TestCases.models import *

logger = logging.getLogger(__name__)


def get_server_instance():
    jenkins_url = JENKINS_URL
    server = Jenkins(jenkins_url, username=USER_NAME, password=PASSWORD)
    return server


def get_acceptance_results_from_jenkins():
    get_results_from_jenkins(ACCEPTANCE_URL, EXCLUDED_ACCEPTANCE_JOBS, True)


def get_trunk_results_from_jenkins():
    get_results_from_jenkins(TRUNK_URL, EXCLUDED_TRUNK_JOBS, False)


def get_results_from_jenkins(view_url, excluded_jobs, is_acceptance):
    print(" > cleaning DB")
    Job.objects.all().delete()
    JobBuild.objects.all().delete()
    TestResult.objects.all().delete()
    print(" > Lets get build results from uncle Jenkins")
    server = get_server_instance()
    # opening acceptance view
    view = server.get_view_by_url(view_url)
    # getting all jobs from view
    jobs_dict = view.get_job_dict()
    print(" >> We have - " + str(len(jobs_dict) - len(excluded_jobs)) + " jobs in " + view_url)
    for job_title, job_link in jobs_dict.items():
        # filtering jobs
        if job_title not in excluded_jobs:
            job_inst = server.get_job(job_title)
            # creating new job
            new_job = create_new_job(job_title, job_link, is_acceptance)
            # getting builds for job
            builds_dict = job_inst.get_build_dict()
            for build_number, build_link in builds_dict.items():
                process_build_data(job_inst, new_job, build_number, build_link)


def process_build_data(job_inst, new_job, build_number, build_link):
    build_inst = job_inst.get_build(build_number)
    build_run_time = str(build_inst.get_duration()).split('.')[0]
    build_date = build_inst.get_timestamp().strftime('%d.%m.%Y %H:%M')
    # filtering builds that have artifacts
    artifacts = build_inst.get_artifact_dict()
    for artifact_name, artifact in artifacts.items():
        if artifact_name == BUILD_RESULTS:
            save_artifact(artifact)
            process_artifact(new_job, build_number, build_link, build_date, build_run_time)


def save_artifact(artifact):
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
    artifact.save_to_dir(TARGET_DIR)


def process_artifact(new_job, build_number, build_link, build_date, build_run_time):
    # creating new build with link to QA_Team_Report
    new_build = create_new_build(new_job,
                                 build_number,
                                 build_link + BUILD_RESULTS_REPORT_LINK,
                                 build_date,
                                 build_run_time)
    html_report_file = open(BUILD_RESULTS_FILE_PATH)
    html_report_soup = BeautifulSoup(html_report_file, 'html.parser')
    # unique_test_classes_set used to avoid methods be at the same time in 'failed', 'skipped', and 'passed' groups
    unique_test_classes_set = set()
    failed_test_methods = html_report_soup.find_all(id="failedTest")
    successful_build = True
    if len(failed_test_methods) > 0:
        print(" >>>>> Saving FAILED TESTS ")
        successful_build = False
        for failed_test_method in failed_test_methods:
            failed_test_class_name = failed_test_method.contents[1].get_text().split(".")[1]
            failed_test_class_stack_trace = failed_test_method.find('textarea').getText()
            if failed_test_class_name not in unique_test_classes_set:
                create_new_test_result(new_build, failed_test_class_name, "failed", failed_test_class_stack_trace)
                unique_test_classes_set.add(failed_test_class_name)
            else:
                logger.info(" >>>>>> TEST RESULTS ERROR - Test class " + failed_test_class_name +
                            " has more then one failed result in build #" + str(build_number))

    skipped_test_methods = html_report_soup.find_all(id="skippedTest")
    if len(skipped_test_methods) > 0:
        print(" >>>>> Saving SKIPPED TESTS ")
        successful_build = False
        for skipped_test_method in skipped_test_methods:
            skipped_test_class_name = skipped_test_method.contents[1].get_text().split(".")[1]
            if skipped_test_class_name not in unique_test_classes_set:
                create_new_test_result(new_build, skipped_test_class_name, "skipped", "")
                unique_test_classes_set.add(skipped_test_class_name)

    passed_test_methods = html_report_soup.find_all(id="passedTest")
    if len(passed_test_methods) > 0:
        print(" >>>>> Saving PASSED TESTS ")
        for passed_test_method in passed_test_methods:
            passed_test_class_name = passed_test_method.contents[1].get_text().split(".")[1]
            if passed_test_class_name not in unique_test_classes_set:
                create_new_test_result(new_build, passed_test_class_name, "passed", "")
                unique_test_classes_set.add(passed_test_class_name)
            else:
                logger.info(" >>>>>> TEST RESULTS ERROR - Test class " + passed_test_class_name +
                            " already is in 'failed' or 'skipped' tests in build #" + str(build_number))
    # saving successful_build if its successful
    if successful_build and len(unique_test_classes_set) > 0:
        new_build.build_successful = True
    pre_text = html_report_soup.find('pre').getText().replace("\n", "")
    # saving app_version
    app_version_search_result = re.findall("Application Version : (.+?)Locale", pre_text)
    for app_version in app_version_search_result:
        new_build.build_app_ver = app_version.split()[0][2:]
    new_build.save()
    html_report_file.close()
    os.remove(BUILD_RESULTS_FILE_PATH)


def add_acceptance_groups_to_jobs():
    add_groups_to_jobs(ACCEPTANCE_URL, EXCLUDED_ACCEPTANCE_JOBS)


def add_trunk_groups_to_jobs():
    add_groups_to_jobs(TRUNK_URL, EXCLUDED_TRUNK_JOBS)


def add_groups_to_jobs(view_url, excluded_jobs):
    config_links_dict = get_jenkins_jobs_configs_links_dict(view_url, excluded_jobs)
    # setting webdriver to parse Jenkins
    firefox_profile = webdriver.FirefoxProfile(LOCAL_FIREFOX_PROFILE)
    driver = webdriver.Firefox(firefox_profile)
    driver.implicitly_wait(10)
    # logging to Jenkins
    driver.get(JENKINS_LOGIN_URL)
    driver.find_element_by_name("j_username").send_keys(USER_NAME)
    driver.find_element_by_name("j_password").send_keys(PASSWORD)
    driver.find_element_by_name("Submit").click()
    # getting config files
    for job_name, config_link in config_links_dict.items():
        # getting xml data for job
        driver.get(config_link)
        config_xml = driver.page_source
        groups_list = get_groups_list_from_job_config(job_name, config_xml)
        # adding groups to job
        job_from_db = Job.objects.get(job_name=job_name)
        print(job_from_db.job_name)
        for group_name in groups_list:
            if not TestGroup.objects.filter(test_group_name=group_name):
                new_group = TestGroup()
                new_group.test_group_name = group_name
                new_group.save()
                print("Saved group - " + new_group.test_group_name)
            group_from_db = TestGroup.objects.get(test_group_name=group_name)
            group_from_db.job = job_from_db
            group_from_db.save()


def get_jenkins_jobs_configs_links_dict(view_url, excluded_jobs):
    config_links_dict = dict()
    print(" > Lets get jobs configs from uncle Jenkins")
    server = get_server_instance()
    # opening acceptance view
    view = server.get_view_by_url(view_url)
    # getting all jobs from view
    jobs_dict = view.get_job_dict()
    print(" >> We have - " + str(len(jobs_dict) - len(excluded_jobs)) + " jobs in " + view_url)
    for job_title, job_link in jobs_dict.items():
        if job_title not in excluded_jobs:
            config_links_dict[job_title] = job_link + CONFIG_FILE
    return config_links_dict


def get_groups_list_from_job_config(job_name, config_xml):
    groups_data = ""
    config_dict = untangle.parse(config_xml)
    groups_data = config_dict.project.builders.EnvInjectBuilder.info.propertiesContent.cdata
    if groups_data.startswith("TEST_GROUPS="):
        return groups_data.replace("TEST_GROUPS=", "").split(",")
    else:
        logger.info("TEST_GROUPS ABSENT IN JOB CONFIGS - (" + groups_data + ") for job (" + job_name + ")")
