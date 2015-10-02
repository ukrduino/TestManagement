// HOME PAGE BUTTONS
// START ACTIONS
$('#parse_java').click(function (event) {
    event.preventDefault();
    $.ajax({
        url: 'parse_java_code/',
        type: 'get', //this is the default though, you don't actually need to always mention it
        success: function () {
            alert("Successfully !!!");
        }
    });
});

$('#save_instances').click(function (event) {
    event.preventDefault();
    $.ajax({
        url: 'save_instances/',
        type: 'get', //this is the default though, you don't actually need to always mention it
        success: function () {
            alert("Successfully !!!");
        }
    });
});

$('#get_builds_info_from_jenkins').click(function (event) {
    event.preventDefault();
    $.ajax({
        url: 'get_builds_info_from_jenkins/',
        type: 'get', //this is the default though, you don't actually need to always mention it
        success: function () {
            alert("Successfully !!!");
        }
    });
});

// ACCEPTANCE ACTIONS
$('#get_acceptance_job_configs_from_jenkins').click(function (event) {
    event.preventDefault();
    $.ajax({
        url: 'get_acceptance_job_configs_from_jenkins/',
        type: 'get', //this is the default though, you don't actually need to always mention it
        success: function () {
            alert("Successfully !!!");
        }
    });
});

// TRUNK ACTIONS
$('#get_trunk_job_configs_from_jenkins').click(function (event) {
    event.preventDefault();
    $.ajax({
        url: 'get_trunk_job_configs_from_jenkins/',
        type: 'get', //this is the default though, you don't actually need to always mention it
        success: function () {
            alert("Successfully !!!");
        }
    });
});

// ACCEPTANCE PAGE BUTTONS
var job_id;
$(function () {
    $('button:contains("LOAD DATA")').click(function () {
        job_id = $(this).attr("data-job_id");
        $('img#loader' + job_id).toggle();
        $.ajax({
            type: 'POST',
            url: 'load_data/',                       //TODO use Django Template tags if possible
            data: {
                'job_id' : job_id,
                'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val()
            },
            success: tests_for_job,
            dataType: 'html'
        });
    });
});

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
$('#job_search_input').keyup(function () {
    $.ajax({
        type: 'POST',
        url: 'by_groups/',
        data: {
            'search_text' : $('#job_search_input').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val()
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
            'search_text' : $('#group_search_input').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val()
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
    alert(jenkins_page);
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