import re

from jenkinsapi.jenkins import Jenkins
from bs4 import BeautifulSoup
from selenium import webdriver
import untangle
from untangle import Element

from TestManagement.local_settings import *
from TestCases.models import *

logger = logging.getLogger(__name__)


def get_server_instance():
    jenkins_url = JENKINS_URL
    server = Jenkins(jenkins_url, username=USER_NAME, password=PASSWORD)
    return server


def get_acceptance_builds_info_from_jenkins():
    get_results_from_jenkins(ACCEPTANCE)


def get_trunk_builds_info_from_jenkins():
    get_results_from_jenkins(TRUNK)


def get_new_trunk_builds_info_from_jenkins():
    get_results_from_jenkins(NEW_TRUNK)


def get_results_from_jenkins(job_jenkins_page):
    print(" > Lets get " + job_jenkins_page + " build results from uncle Jenkins")
    server = get_server_instance()
    for job in Job.objects.filter(job_jenkins_page=job_jenkins_page):
            job_inst = server.get_job(job.job_name)
            # getting builds for job
            builds_dict = job_inst.get_build_dict()
            for build_number, build_link in builds_dict.items():
                process_build_data(job_inst, job, build_number, build_link)


def process_build_data(job_inst, job, build_number, build_link):
    build_inst = job_inst.get_build(build_number)
    build_run_time = str(build_inst.get_duration()).split('.')[0]
    build_date = build_inst.get_timestamp().strftime('%d.%m.%Y %H:%M')
    print(build_date)
    # filtering builds that have artifacts
    artifacts = build_inst.get_artifact_dict()
    for artifact_name, artifact in artifacts.items():
        if artifact_name == BUILD_RESULTS:
            # creating new build with link to QA_Team_Report
            new_build = create_new_build(job,
                                         build_number,
                                         build_link + BUILD_RESULTS_REPORT_LINK,
                                         build_date,
                                         build_run_time)
            print("build_date - " + new_build.build_date)
            save_artifact(artifact)
            process_artifact(new_build)


def save_artifact(artifact):
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
    artifact.save_to_dir(TARGET_DIR)


def process_artifact(new_build):
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
                            " has more then one failed result in build #" + str(new_build.build_number))

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
                            " already is in 'failed' or 'skipped' tests in build #" + str(new_build.build_number))
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


# SAVING JOBS CONFIGS TO JOBS FROM DB

def get_acceptance_job_configs_from_jenkins():
    add_config_data_to_jobs(ACCEPTANCE)


def get_trunk_job_configs_from_jenkins():
    add_config_data_to_jobs(TRUNK)


def get_new_trunk_job_configs_from_jenkins():
    add_config_data_to_jobs(NEW_TRUNK)


def add_config_data_to_jobs(job_jenkins_page):
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
    for job in Job.objects.filter(job_jenkins_page=job_jenkins_page):
        driver.get(job.job_link + CONFIG_FILE)
        config_xml = driver.page_source
        print("Requesting data for job " + job.job_name)
        # getting data from xml
        config_data_dict = get_data_from_job_config(job.job_name, config_xml)
        # adding data to job
        if len(config_data_dict["groups_list"]):
            for group_name in config_data_dict["groups_list"]:
                if not TestGroup.objects.filter(test_group_name=group_name):
                    new_group = TestGroup()
                    new_group.test_group_name = group_name
                    new_group.save()
                    print("Saved group - " + new_group.test_group_name)
                group_from_db = TestGroup.objects.get(test_group_name=group_name)
                group_from_db.job = job
                group_from_db.save()
        # saving shell command
        job.job_hudson_shell_command = config_data_dict["shell_command"]
        job.job_description = config_data_dict["job_description"]
        if len(config_data_dict["up_stream_jobs_names"]):
            for up_stream_job_name in config_data_dict["up_stream_jobs_names"]:
                up_stream_job = Job.objects.get(job_name=up_stream_job_name)
                job.job_up_stream = up_stream_job
        job.save()
        print("Job updated")
        print(job.job_name)
        print(job.job_description)
        print(job.job_link)
        print(job.job_jenkins_page)
        print(job.job_hudson_shell_command)
        print(job.job_up_stream)
        print(job.job_enabled)
        print("---------------")


def get_data_from_job_config(job_name, config_xml):
    config_data_dict = dict()
    config_dict = untangle.parse(config_xml)
    # print(config_xml)
    # getting groups list
    env_inject_builder_tag = config_dict.project.builders.EnvInjectBuilder
    if not isinstance(env_inject_builder_tag, Element):
        # special case for job Check environment and start all tests
        # if env_inject_builder_tag is List
        properties_content_tag_list= env_inject_builder_tag[1].info.propertiesContent.cdata.split("\n")
        for property_content in properties_content_tag_list:
            if property_content.startswith("TEST_GROUPS="):
                config_data_dict["groups_list"] = property_content.replace("TEST_GROUPS=", "").split(",")
    else:
        properties_content_tag_list = config_dict.project.builders.EnvInjectBuilder.info.propertiesContent.cdata.split("\n")
        for property_content in properties_content_tag_list:
            if property_content.startswith("TEST_GROUPS="):
                config_data_dict["groups_list"] = property_content.replace("TEST_GROUPS=", "").split(",")
    # getting shell command
    config_data_dict["shell_command"] = config_dict.project.builders.hudson_tasks_Shell.command.cdata
    # getting job description
    config_data_dict["job_description"] = config_dict.project.description.cdata
    server = get_server_instance()
    job_inst = server.get_job(job_name)
    # getting upstream jobs
    config_data_dict["up_stream_jobs_names"] = job_inst.get_upstream_job_names()
    return config_data_dict


# SAVING JOBS TO DB
def get_acceptance_jobs_from_jenkins():
    get_jobs_from_jenkins(ACCEPTANCE_URL, EXCLUDED_ACCEPTANCE_JOBS, ACCEPTANCE)


def get_trunk_jobs_from_jenkins():
    get_jobs_from_jenkins(TRUNK_URL, EXCLUDED_TRUNK_JOBS, TRUNK)


def get_new_trunk_jobs_from_jenkins():
    get_jobs_from_jenkins(NEW_TRUNK_URL, EXCLUDED_NEW_TRUNK_JOBS, NEW_TRUNK)


def get_jobs_from_jenkins(view_url, excluded_jobs, job_jenkins_page):
    print(" > Lets get " + job_jenkins_page + " jobs from uncle Jenkins")
    server = get_server_instance()
    # opening acceptance view
    view = server.get_view_by_url(view_url)
    # getting all jobs from view
    jobs_dict = view.get_job_dict()
    print(" >> We have - " + str(len(jobs_dict) - len(excluded_jobs)) + " jobs in " + job_jenkins_page)
    for job_title, job_link in jobs_dict.items():
        # filtering jobs
        if job_title not in excluded_jobs:
            job_inst = server.get_job(job_title)
            # creating new job
            create_new_job(job_title, job_link, job_jenkins_page, job_inst.is_enabled())
