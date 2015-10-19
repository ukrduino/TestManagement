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
    show_progress_bar('#save_instances_progress');
    setTimeout(update_progress_bar, 5000);
    displayOverlay("Saving test classes and test cases to DB");
    $.ajax({
        url: 'save_instances/',
        type: 'get',
        success: function () {
            update_progress_bar_to_full();
            removeOverlay()
            alert("Successfully saved test classes and test cases!!!");
            destroy_progress_bar();
        }
    });
});

$('.get_jobs').click(function (event) {
    event.preventDefault();
    var jenkins_page = $(this).attr("data-jenkins_page");
    if (jenkins_page == "Acceptance"){
        show_progress_bar('#get_jobs_acceptance_progress');
    }
    if (jenkins_page == "Trunk"){
        show_progress_bar('#get_jobs_trunk_progress');
    }
    if (jenkins_page == "New trunk"){
        show_progress_bar('#get_jobs_new_trunk_progress');
    }
    if (jenkins_page == "All other"){
        show_progress_bar('#get_jobs_all_other_progress');
    }
    setTimeout(update_progress_bar, 5000);
    displayOverlay("Saving jobs from " + jenkins_page + " page");
    $.ajax({
        type: 'post',
        url: 'get_jobs/',
        data: {
            'jenkins_page': jenkins_page,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function () {
            update_progress_bar_to_full();
            removeOverlay()
            alert("Successfully saved jobs from " + jenkins_page + " page!!!");
            destroy_progress_bar();
        }
    });
});

$('.get_jobs_configs').click(function (event) {
    event.preventDefault();
    var jenkins_page = $(this).attr("data-jenkins_page");
    if (jenkins_page == "Acceptance"){
        show_progress_bar('#get_jobs_configs_acceptance_progress');
    }
    if (jenkins_page == "Trunk"){
        show_progress_bar('#get_jobs_configs_trunk_progress');
    }
    if (jenkins_page == "New trunk"){
        show_progress_bar('#get_jobs_configs_new_trunk_progress');
    }
    setTimeout(update_progress_bar, 5000);
    displayOverlay("Saving jobs configs from " + jenkins_page + " page");
    $.ajax({
        type: 'post',
        url: 'get_jobs_configs/',
        data: {
            'jenkins_page': jenkins_page,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function () {
            update_progress_bar_to_full();
            removeOverlay();
            alert("Successfully saved jobs configs from " + jenkins_page + " page!!!");
            destroy_progress_bar();
        }
    });
});

$('.get_builds_and_save_results').click(function (event) {
    event.preventDefault();
    var jenkins_page = $(this).attr("data-jenkins_page");
    if (jenkins_page == "Acceptance"){
        show_progress_bar('#get_builds_and_save_results_acceptance_progress');
    }
    if (jenkins_page == "Trunk"){
        show_progress_bar('#get_builds_and_save_results_trunk_progress');
    }
    if (jenkins_page == "New trunk"){
        show_progress_bar('#get_builds_and_save_results_new_trunk_progress');
    }
    setTimeout(update_progress_bar, 5000);
    displayOverlay("Saving build results for jobs from " + jenkins_page + " page");
    $.ajax({
        type: 'post',
        url: 'get_builds_and_save_results/',
        data: {
            'jenkins_page': jenkins_page,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function () {
            update_progress_bar_to_full()
            removeOverlay();
            alert("Successfully saved build results for jobs from " + jenkins_page + " page!!!");
            destroy_progress_bar();
        }
    });
});

$('.delete').click(function (event) {
    event.preventDefault();
    var object_to_delete = $(this).attr("data-delete");
    $.ajax({
        type: 'post',
        url: 'delete/',
        data: {
            'object_to_delete': object_to_delete,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
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
    $('button#showButton' + job_id).show().click(function () {
        job_id = $(this).attr("data-job_id");
        $('#' + job_id).toggle();
    });
    $('button#loadButton' + job_id).hide();
}

$('#myModal').on('show.bs.modal', function (e) {
    var stack_trace = $(e.relatedTarget).data('stack');
    $(e.currentTarget).find('pre.stack_trace').text(stack_trace)
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

function show_progress_bar(progress_bar) {
    $(progress_bar).html('' +
        '<div class="panel-footer">' +
        '<div class="progress progress-striped">' +
        '<div class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>' +
        '</div>');
}

function destroy_progress_bar() {
    $('.progressDiv').each(function() {
        $(this).html("");
    });
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
            var current_perc = resp.current_val / resp.max_val * 100;
            if (current_perc <= 100) {
                //http://stackoverflow.com/a/21182722
                $('.progress-bar').css('width', current_perc + '%').attr('aria-valuenow', current_perc);
                //http://stackoverflow.com/a/5052606
                setTimeout(update_progress_bar, 5000)
            }
        },
        error: function () {
            update_progress_bar();
        }
    });
}
function update_progress_bar_to_full() {
    $('.progress-bar').css('width', 100 + '%').attr('aria-valuenow', 100);
}
//http://stackoverflow.com/a/25187060
function displayOverlay(text) {
    $("<table id='overlay'><tbody><tr><td>" + text + "</td></tr></tbody></table>").css({
        "position": "fixed",
        "top": "0px",
        "left": "0px",
        "width": "100%",
        "height": "100%",
        "background-color": "rgba(0,0,0,.5)",
        "z-index": "10000",
        "vertical-align": "middle",
        "text-align": "center",
        "color": "#fff",
        "font-size": "40px",
        "font-weight": "bold",
        "cursor": "wait"
    }).appendTo("body");
}

function removeOverlay() {
    $("#overlay").remove();
}