import logging

from django.db import models

logger = logging.getLogger(__name__)


class Job(models.Model):
    class Meta:
        db_table = 'jobs'
        verbose_name = 'Jenkins job'
        verbose_name_plural = 'Jenkins jobs'

    job_name = models.CharField(verbose_name="Job name", max_length=200)
    job_env = models.CharField(verbose_name="Job environment", max_length=200, null=True)

    def __str__(self):
        return self.job_name

    def __unicode__(self):
        return self.job_name


def create_new_job(job_title):
    # creating new job
    new_job = Job(job_name=job_title)
    new_job.save()
    print(" >>> Saved new job - " + new_job.job_name)
    return new_job


class JobBuild(models.Model):
    class Meta:
        db_table = 'job_builds'
        verbose_name = 'Job build'
        verbose_name_plural = 'Job builds'

    job = models.ForeignKey(Job)
    build_number = models.IntegerField(verbose_name="Number of build")
    build_date = models.DateTimeField(verbose_name="Date of build", null=True)

    def __str__(self):
        return "Build #" + str(self.build_number) + " of " + self.job.job_name

    def __unicode__(self):
        return "Build #" + str(self.build_number) + " of " + self.job.job_name


def create_new_build(new_job, build_number):
    # creating new build
    new_build = JobBuild(job=new_job, build_number=build_number)
    new_build.save()
    print(" >>>> Saved new build #" + str(new_build.build_number) + " for >>> " + new_build.job.job_name)
    return new_build


class TestGroup(models.Model):
    class Meta:
        db_table = 'test_group'
        verbose_name = 'Test group'
        verbose_name_plural = 'Test groups'

    test_group_name = models.CharField(verbose_name="Test group name", max_length=200)
    job = models.ForeignKey(Job, null=True)

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
    test_class_blocked_by_ticket = models.CharField(verbose_name="Test class blocked by ticket", max_length=200, null=True)
    test_class_comment = models.TextField(verbose_name="Test class comment", null=True)

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
    test_case_comment = models.TextField(verbose_name="Test case comment", null=True)

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

    def __str__(self):
        return "TestResult #" + str(self.id)

    def __unicode__(self):
        return "TestResult #" + str(self.id)


def create_new_test_result(build, test_class_name, passed):
    test_classes = TestClass.objects.filter(test_class_name__contains=test_class_name)
    if len(test_classes) == 1:
        new_test_result = TestResult(test_class=test_classes[0], build=build, test_passed=passed)
        new_test_result.save()
        print(" >>>>>> Saved TestResult#" + str(new_test_result.id) + " for " + test_classes[0].test_class_name)
    elif len(test_classes) == 0:
        logger.info(" >>>>>> ERROR - No test class with name " + test_class_name + "found in DB")
    elif len(test_classes) > 1:
        logger.info(" >>>>>> ERROR - 2 or more test class with name " + test_class_name + "found in DB")
        for test in test_classes:
            logger.info(str(test.id) + test.test_class_name)
        logger.info(" >>>>>> Result not saved")


# http://stackoverflow.com/a/29898483
