import codecs
import re

from TestCases.models import *
from TestManagement.local_settings import *

result_file_path = TARGET_DIR + "\\results.txt"


# http://stackoverflow.com/questions/2212643/python-recursive-folder-read
def get_tests_headers_from_java_code():
    # Creating results file - results.txt
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
    result_file = open(result_file_path, 'w+')
    # Searching test classes in java files in java_tests_dir
    for root, subdirs, files in os.walk(JAVA_TESTS_DIR):
        for filename in files:
            # searching test classes
            if filename.endswith("Test.java"):
                file_path = os.path.join(root, filename)
                with open(file_path, "r", encoding="utf-8") as my_file:
                    # placing file content to one string
                    file_text_in_one_sting = my_file.read().replace('\n', '').replace('\t', ' ')
                    # searching test class headers in string
                    search_result = re.findall("@Test(.+?)\(\)", file_text_in_one_sting)
                    if len(search_result) > 0:
                        for res in search_result:
                            # saving to file replacing "unreadable characters"
                            # print(res.replace('\xa3', "f"))
                            result_file.write(res.replace('\xa3', "f"))
                            result_file.write('\n')
    result_file.close()
    print("------------------------------ Result file created-----------------------------")


def create_instances_and_put_to_db():
    my_file = codecs.open(result_file_path, "r", "cp1250")
    data = my_file.readlines()
    progress_bar = init_progress_bar(len(data))
    for class_header in data:
        # creating new instance of TestClass
        new_test_class = TestClass()
        # searching test class name in class headers
        test_class_name_search_result = re.findall("public void (.+?)\\n", class_header)  # TODO Some shit at the end of class name
        for name in test_class_name_search_result:
            new_test_class.test_class_name = name.replace(" ", "").replace('\n', '').replace('\t', ' ')
        # saving TestClass with name only
        new_test_class.save()
        # searching if test class enabled
        enabled_search_result = re.findall("enabled(.+?),", class_header)
        for is_enabled in enabled_search_result:
            enabled = is_enabled.replace(" ", "").replace("=", "")
            if enabled == "false":
                new_test_class.test_class_enabled = False
                comment_search_result = re.findall("//(.+?)description", class_header)
                if len(comment_search_result) > 0:
                    for comment in comment_search_result:
                        new_test_class.test_class_comment = comment
                blocked_by_ticket_search_result = re.findall("#([0-9]+)description", class_header)
                if len(blocked_by_ticket_search_result) > 0:
                    if len(blocked_by_ticket_search_result) == 1:
                        for ticket in blocked_by_ticket_search_result:
                            new_test_class.test_class_blocked_by_ticket = ticket
                    else:
                        blocked_by_ticket = ",".join(blocked_by_ticket_search_result)
                        new_test_class.test_class_blocked_by_ticket = blocked_by_ticket
            new_test_class.save()
        # searching test groups in class headers
        add_test_cases_to_test_class(class_header, new_test_class)
        add_groups_to_test_class(class_header, new_test_class)
        progress_bar.increase()
    progress_bar.clear()
    print(">>>>> All instances created")


def add_groups_to_test_class(class_header, new_test_class):
    groups_search_result = re.findall("groups = \{(.+?)\"\}", class_header)
    if len(groups_search_result) > 0:
        for groups in groups_search_result:
            # removing symbols , and "
            result1 = groups.replace("\"", "").replace(",", "")
            # creating list of groups for this test class
            groups_in_test_list = result1.split()
            for grop_name in groups_in_test_list:
                # saving test group to db if its not saved before
                if not TestGroup.objects.filter(test_group_name=grop_name):
                    new_group = TestGroup()
                    new_group.test_group_name = grop_name
                    new_group.save()
            for grop_name in groups_in_test_list:
                group = TestGroup.objects.get(test_group_name=grop_name)
                new_test_class.test_class_group.add(group)


def add_test_cases_to_test_class(class_header, new_test_class):
    # searching test case names and links in class headers
    test_cases_search_result = re.findall("description(.+?)public", class_header)
    for res in test_cases_search_result:
        # removing symbols
        result4 = res.replace("\"", "") \
                      .replace(",", "") \
                      .replace("=", "") \
                      .replace(";", " ") \
                      .replace("+", "") \
                      .replace(")", "").replace("  ", " ") + " "
        test_case_link_search_result = re.findall(" TC(.+?) ", result4)
        if len(test_case_link_search_result) > 0:
            for link in test_case_link_search_result:
                if not TestCase.objects.filter(test_case_link=TEST_CASE_LINK + link):
                    new_test_case = TestCase()
                    new_test_case.test_case_link = TEST_CASE_LINK + link
                    new_test_case.test_case_name = get_test_case_name_by_link("TC" + link, result4)
                    new_test_case.save()
                test_case = TestCase.objects.get(test_case_link=TEST_CASE_LINK + link)
                test_case.test_case_class = new_test_class
                test_case.save()


def get_test_case_name_by_link(link, search_in_string):
    list1 = search_in_string.split(link)
    test_case_name = list1[0]
    search_result_8 = re.findall("TC_(.+?) ", test_case_name)
    if len(search_result_8) > 0:
        for res in search_result_8:
            test_case_name = test_case_name.split(res)[1]
            search_result_9 = re.findall("TC_(.+?) ", test_case_name)
            if len(search_result_9) == 0:
                break
    return test_case_name
