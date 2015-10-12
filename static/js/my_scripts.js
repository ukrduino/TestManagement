// DATA COLLECTION PAGE
$('#parse_java').click(function (event) {
    event.preventDefault();
    $.ajax({
        url: 'parse_java_code/',
        type: 'get',
        success: function () {
            alert("Successfully !!!");
        }
    });
});

$('#save_instances').click(function (event) {
    event.preventDefault();
    show_progress_bar();
    setTimeout(update_progress_bar, 5000);
    $.ajax({
        url: 'save_instances/',
        type: 'get',
        success: function () {
            destroy_progress_bar();
            alert("Successfully saved test classes and test cases!!!")
        }
    });
});

$('.get_jobs').click(function (event) {
    event.preventDefault();
    var jenkins_page = $(this).attr("data-jenkins_page");
    $.ajax({
        url: 'get_jobs/',
        data: {
            'jenkins_page': jenkins_page,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        type: 'POST',
        success: function () {
            alert("Successfully !!!");
        }
    });
});

$('.get_jobs_configs').click(function (event) {
    event.preventDefault();
    var jenkins_page = $(this).attr("data-jenkins_page");
    $.ajax({
        url: 'get_jobs_configs/',
        data: {
            'jenkins_page': jenkins_page,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        type: 'POST',
        success: function () {
            alert("Successfully !!!");
        }
    });
});

$('.get_builds_and_save_results').click(function (event) {
    event.preventDefault();
    var jenkins_page = $(this).attr("data-jenkins_page");
    $.ajax({
        url: 'get_builds_and_save_results/',
        data: {
            'jenkins_page': jenkins_page,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        type: 'POST',
        success: function () {
            alert("Successfully !!!");
        }
    });
});

$('.delete').click(function (event) {
    event.preventDefault();
    var object_to_delete = $(this).attr("data-delete");
    $.ajax({
        url: 'delete/',
        data: {
            'object_to_delete': object_to_delete,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        type: 'POST',
        success: function () {
            alert("Successfully deleted " + object_to_delete);
        }
    });
});

// JOBS RESULTS PAGE BUTTONS
var job_id;

$('.show_jobs_results').click(function (event) {
    event.preventDefault();
    var jenkins_page = $(this).attr("data-jenkins_page");
    $.ajax({
        url: 'show_jobs_results/',
        data: {
            'jenkins_page': jenkins_page,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        type: 'POST',
        success: show_jobs_results_in_template,
        dataType: 'html'
    });
});

function show_jobs_results_in_template(data) {
    $('#jobs_results_in_template').html(data);
    $('button:contains("LOAD DATA")').click(function () {
        job_id = $(this).attr("data-job_id");
        $('img#loader' + job_id).toggle();
        $.ajax({
            type: 'POST',
            url: 'load_data/',
            data: {
                'job_id': job_id,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: tests_for_job,
            dataType: 'html'
        });
    });
    $('[data-toggle="tooltip"]').tooltip()
}

function tests_for_job(data) {
    $('#' + job_id).html(data);
    $('img#loader' + job_id).toggle();
    $('button#showButton' + job_id).show();
    $('button#loadButton' + job_id).hide();
}

$('#myModal').on('show.bs.modal', function (e) {
    var stack_trace = $(e.relatedTarget).data('stack');
    $(e.currentTarget).find('pre.stack_trace').text(stack_trace)
});

$(function () {
    $('button:contains("HIDE/SHOW")').click(function () {
        job_id = $(this).attr("data-job_id");
        $('#' + job_id).toggle();
    });
});

// SEARCH JOB PAGE
$('#job_search_by_groups_input').keyup(function () {
    $.ajax({
        type: 'POST',
        url: 'by_groups/',
        data: {
            'search_text': $('#job_search_by_groups_input').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: job_search_successful,
        dataType: 'html'
    });
});

$('#job_search_by_job_name_input').keyup(function () {
    $.ajax({
        type: 'POST',
        url: 'by_job_name/',
        data: {
            'search_text': $('#job_search_by_job_name_input').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: job_search_successful,
        dataType: 'html'
    });
});

function job_search_successful(data) {
    $('#found_jobs_list_in_template').html(data);
}

$('#group_search_input').keyup(function () {
    $.ajax({
        type: 'POST',
        url: 'search_group/',
        data: {
            'search_text': $('#group_search_input').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: group_search_successful,
        dataType: 'html'
    });
});

function group_search_successful(data) {
    $('#found_groups_list_in_template').html(data);
}

// JOBS CONFIGS PAGE
$('.show_jobs_configs').click(function (event) {
    event.preventDefault();
    var jenkins_page = $(this).attr("data-jenkins_page");
    $.ajax({
        url: 'show_jobs_configs/',
        data: {
            'jenkins_page': jenkins_page,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        type: 'POST',
        success: show_jobs_configs,
        dataType: 'html'
    });
});

function show_jobs_configs(data) {
    $('#jobs_configs_in_template').html(data);
}

function show_progress_bar() {
    $('#progressDiv').html('' +
        '<div class="panel-footer">' +
        '<div class="progress progress-striped active">' +
        '<div class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>' +
        '</div>');
}

function destroy_progress_bar() {
    $('#progressDiv').html("");
}

//http://stackoverflow.com/a/5109076
function update_progress_bar() {
    $.ajax({
        type: 'post',
        url: 'json/', // or your absolute-path
        data: {
            'process': "updating progress bar",
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        success: function (resp) {
            console.info("Ajax Response is there.....");
            console.log(resp);
            var current_perc = resp.current_val / resp.max_val * 100
            if (current_perc < 100) {
                //http://stackoverflow.com/a/21182722
                $('.progress-bar').css('width', current_perc + '%').attr('aria-valuenow', current_perc);
                //http://stackoverflow.com/a/5052606
                setTimeout(update_progress_bar, 5000)
            }
            else {
                destroy_progress_bar()
            }
        },
        error: function () {
            update_progress_bar();
        }
    });
}