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


