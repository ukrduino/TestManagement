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

// ACCEPTANCE ACTIONS
$('#get_acceptance_builds_info_from_jenkins').click(function (event) {
    event.preventDefault();
    $.ajax({
        url: 'get_acceptance_builds_info_from_jenkins/',
        type: 'get', //this is the default though, you don't actually need to always mention it
        success: function () {
            alert("Successfully !!!");
        }
    });
});

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
$('#get_trunk_builds_info_from_jenkins').click(function (event) {
    event.preventDefault();
    $.ajax({
        url: 'get_trunk_builds_info_from_jenkins/',
        type: 'get', //this is the default though, you don't actually need to always mention it
        success: function () {
            alert("Successfully !!!");
        }
    });
});

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
    $(e.currentTarget).find('div.stack_trace').text(stack_trace)
});

$(function () {
    $('button:contains("HIDE/SHOW")').click(function () {
        job_id = $(this).attr("data-job_id");
        $('#' + job_id).toggle();
    });
});

// SEARCH JOB PAGE BUTTON
$('#job_search_input').keyup(function () {
    $.ajax({
        type: 'POST',
        url: 'by_groups/',                       //TODO use Django Template tags if possible
        data: {
            'search_text' : $('#job_search_input').val(),
            'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val()
        },
        success: search_Successful,
        dataType: 'html'
    });
});

function search_Successful(data) {
    $('#found_jobs_list_in_template').html(data);
}