import logging

from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class Job(models.Model):
    class Meta:
        db_table = 'jobs'
        verbose_name = 'Jenkins job'
        verbose_name_plural = 'Jenkins jobs'

    job_name = models.CharField(verbose_name="Job name", max_length=200, unique=True)
    job_env = models.CharField(verbose_name="Job environment", max_length=200, null=True)  # TODO get from Job's XML
    job_description = models.TextField(verbose_name="Job description", null=True)
    job_assigned_node = models.CharField(verbose_name="Job assigned node", max_length=200,
                                         null=True)  # TODO get from Job's XML
    job_link = models.CharField(verbose_name="Job link", max_length=200, null=True)
    job_jenkins_page = models.CharField(verbose_name="Jenkins page", max_length=200, null=True)
    job_hudson_shell_command = models.TextField(verbose_name="Job hudson shell command settings", null=True)
    job_up_stream = models.ForeignKey("self", null=True)
    job_enabled = models.BooleanField(verbose_name="Is job enabled", default=True)
    job_successful = models.BooleanField(verbose_name="Is job successful", default=True)

    def __str__(self):
        return self.job_name

    def __unicode__(self):
        return self.job_name


def create_new_job(name, link, job_jenkins_page, is_enabled):  # TODO move to class constructor
    # creating new job
    new_job = Job(job_name=name, job_link=link, job_jenkins_page=job_jenkins_page, job_enabled=is_enabled)
    new_job.save()
    return new_job


class JobBuild(models.Model):
    class Meta:
        db_table = 'job_builds'
        verbose_name = 'Job build'
        verbose_name_plural = 'Job builds'

    job = models.ForeignKey(Job)
    build_number = models.IntegerField(verbose_name="Build number")
    build_app_ver = models.CharField(verbose_name="Version of App", max_length=200, blank=True)
    build_date = models.CharField(verbose_name="Date of build", max_length=200, blank=True)
    build_link = models.CharField(verbose_name="Build link", max_length=200, blank=True)
    build_console_link = models.CharField(verbose_name="Build console link", max_length=200, blank=True)
    build_run_time = models.CharField(verbose_name="Build run time", max_length=200, blank=True)
    build_successful = models.BooleanField(verbose_name="Was build successful", default=False)
    build_number_of_failed_tests = models.IntegerField(verbose_name="Number of failed tests in build", default=0)

    def __str__(self):
        return "Build #" + str(self.build_number) + " of " + self.job.job_name

    def __unicode__(self):
        return "Build #" + str(self.build_number) + " of " + self.job.job_name


def create_new_build(new_job, build_number, build_link, build_console_link, build_date,
                     build_run_time):  # TODO move to class constructor
    # creating new build
    new_build = JobBuild(job=new_job,
                         build_number=build_number,
                         build_link=build_link,
                         build_console_link=build_console_link,
                         build_date=build_date,
                         build_run_time=build_run_time)
    new_build.save()
    return new_build


class TestGroup(models.Model):
    class Meta:
        db_table = 'test_group'
        verbose_name = 'Test group'
        verbose_name_plural = 'Test groups'

    test_group_name = models.CharField(verbose_name="Test group name", max_length=200, unique=True)
    job = models.ManyToManyField(Job)
    jobs_number = models.IntegerField(verbose_name="Number of jobs", default=0)

    def __str__(self):
        return self.test_group_name

    def __unicode__(self):
        return self.test_group_name


class TestClass(models.Model):
    class Meta:
        db_table = 'test_class'
        verbose_name = 'Test class'
        verbose_name_plural = 'Test classes'

    test_class_name = models.CharField(verbose_name="Test class name", max_length=200)
    test_class_group = models.ManyToManyField(TestGroup)
    test_class_build = models.ForeignKey(JobBuild, null=True)
    test_class_enabled = models.BooleanField(default=True)
    test_class_comment = models.TextField(verbose_name="Test class comment", blank=True)

    def __str__(self):
        return self.test_class_name

    def __unicode__(self):
        return self.test_class_name


class TestCase(models.Model):
    class Meta:
        db_table = 'test_case'
        verbose_name = 'Test case'
        verbose_name_plural = 'Test cases'

    test_case_name = models.CharField(verbose_name="Test case name", max_length=200, blank=True)
    test_case_link = models.CharField(verbose_name="Test case link", max_length=200, blank=True)
    test_case_class = models.ForeignKey(TestClass, null=True)
    test_case_comment = models.TextField(verbose_name="Test case comment",
                                         blank=True)  # TODO implement getting comment from Trac and then check link in TestClass

    def __str__(self):
        return self.test_case_name

    def __unicode__(self):
        return self.test_case_name


class TestResult(models.Model):
    class Meta:
        db_table = 'test_result'
        verbose_name = 'Test execution result'
        verbose_name_plural = 'Test execution results'

    test_passed = models.CharField(verbose_name="Test passed", max_length=10)
    build = models.ForeignKey(JobBuild)
    test_class = models.ForeignKey(TestClass)
    test_stack_trace = models.TextField(verbose_name="Stack Trace", blank=True)

    def __str__(self):
        return "TestResult #" + str(self.id)

    def __unicode__(self):
        return "TestResult #" + str(self.id)


def create_new_test_result(build, test_class_name_from_report, passed,
                           failed_test_class_stack_trace):  # TODO move to class constructor
    test_classes_from_db = TestClass.objects.filter(test_class_name__contains=test_class_name_from_report)
    if len(test_classes_from_db) > 0:
        for test_class_obj in test_classes_from_db:
            if test_class_name_from_report == test_class_obj.test_class_name[:-1]:  # removing unknown symbol at the end
                new_test_result = TestResult(test_class=test_class_obj,
                                             build=build,
                                             test_passed=passed,
                                             test_stack_trace=failed_test_class_stack_trace)
                new_test_result.save()
    elif len(test_classes_from_db) > 1:
        logger.info("TEST CLASS DUPLICATION - 2 or more test class with name (or similar name)" +
                    test_class_name_from_report + " found in DB (Build id #" + str(build.id) + ")")
        for test_class_from_db in test_classes_from_db:
            logger.info("Found - test class id(" + str(test_class_from_db.id) + ") test class name(" +
                        test_class_from_db.test_class_name + ")")
    else:
        logger.info("TEST CLASS ABSENT - No test class with name " + test_class_name_from_report +
                    " found in DB (Build id #" + str(build.id) + ")")
        logger.info("Result not saved")


class ProgressBar(models.Model):
    class Meta:
        db_table = 'progress_bar'
        verbose_name = 'Progress bar data'

    def increase(self):
        self.progress_bar_current_val += 1
        self.save()

    def clear(self):
        self.progress_bar_current_val = 0
        self.progress_bar_max_val = 0
        self.save()

    progress_bar_max_val = models.IntegerField(verbose_name="Max value of progress bar", default=0)
    progress_bar_current_val = models.IntegerField(verbose_name="Current value of progress bar", default=0)


def init_progress_bar(max_value):
    if not ProgressBar.objects.all():
        progress_bar = ProgressBar()
        progress_bar.progress_bar_max_val = max_value
        progress_bar.save()
        return progress_bar
    else:
        progress_bar = ProgressBar.objects.last()
        progress_bar.progress_bar_max_val = max_value
        progress_bar.progress_bar_current_val = 0
        progress_bar.save()
        return progress_bar


class DataCollectionTimeStamps(models.Model):
    class Meta:
        db_table = 'data_collection_time_stamps'
        verbose_name = 'Data collection time stamps'

    parse_java_code = models.CharField(verbose_name="Parse java code",
                                       max_length=200, default="no data")
    save_instances_to_db = models.CharField(verbose_name="Save instances to DB",
                                            max_length=200, default="no data")

    get_jobs_acceptance = models.CharField(verbose_name="Get Acceptance jobs from Jenkins",
                                           max_length=200, default="no data")
    get_jobs_new_trunk = models.CharField(verbose_name="Get New Trunk jobs from Jenkins",
                                          max_length=200, default="no data")
    get_jobs_all_other = models.CharField(verbose_name="Get All Other jobs from Jenkins",
                                          max_length=200, default="no data")

    get_jobs_configs_acceptance = models.CharField(verbose_name="Get Acceptance jobs configs from Jenkins",
                                                   max_length=200, default="no data")
    get_jobs_configs_new_trunk = models.CharField(verbose_name="Get New Trunk jobs configs from Jenkins",
                                                  max_length=200, default="no data")
    get_jobs_configs_all_other = models.CharField(verbose_name="Get All Other jobs configs from Jenkins",
                                                  max_length=200, default="no data")
    get_builds_and_save_results_acceptance = models.CharField(verbose_name="Get Acceptance builds from Jenkins",
                                                              max_length=200, default="no data")
    get_builds_and_save_results_new_trunk = models.CharField(verbose_name="Get New Trunk builds from Jenkins",
                                                             max_length=200, default="no data")


def init_data_collection_time_stamps():
    if not DataCollectionTimeStamps.objects.all():
        time_stamp = DataCollectionTimeStamps()
        time_stamp.save()
        return time_stamp
    else:
        return DataCollectionTimeStamps.objects.last()


class ToDoNote(models.Model):
    class Meta:
        db_table = 'to_do_notes'
        verbose_name = 'ToDo notes'
    title = models.CharField(verbose_name="ToDo title", max_length=200)
    content = models.TextField(verbose_name="ToDo title")
    done = models.BooleanField(verbose_name="ToDo done", default=False)
    discarded = models.BooleanField(default=False, verbose_name="ToDo discarded")
    created = models.DateTimeField(verbose_name='ToDo created')
    modified = models.DateTimeField(verbose_name='ToDo modified')

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(ToDoNote, self).save(*args, **kwargs)

# Making migrations
# http://stackoverflow.com/a/29898483
# python manage.py makemigrations <app>
# python manage.py migrate --fake-initial
# python manage.py migrate
