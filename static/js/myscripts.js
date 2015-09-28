$('#parse_java').click(function (event) {
    event.preventDefault();
    $.ajax({
        url: 'parse_java_code/',
        type: 'get', //this is the default though, you don't actually need to always mention it
        success: function (data) {
            alert("Successfully !!!");
        },
        failure: function (data) {
            alert('Got an error dude');
        }
    });
});

$('#save_instances').click(function (event) {
    event.preventDefault();
    $.ajax({
        url: 'save_instances/',
        type: 'get', //this is the default though, you don't actually need to always mention it
        success: function (data) {
            alert("Successfully !!!");
        },
        failure: function (data) {
            alert('Got an error dude');
        }
    });
});

$('#get_builds_info_from_jenkins').click(function (event) {
    event.preventDefault();
    $.ajax({
        url: 'get_builds_info_from_jenkins/',                       //TODO use Django Template tags if possible
        type: 'get', //this is the default though, you don't actually need to always mention it
        success: function (data) {
            alert("Successfully !!!");
        },
        failure: function (data) {
            alert('Got an error dude');
        }
    });                                                             //TODO refactor to parametrized call
});

$('#get_job_configs_from_jenkins').click(function (event) {
    event.preventDefault();
    $.ajax({
        url: 'get_job_configs_from_jenkins/',                       //TODO use Django Template tags if possible
        type: 'get', //this is the default though, you don't actually need to always mention it
        success: function (data) {
            alert("Successfully !!!");
        },
        failure: function (data) {
            alert('Got an error dude');
        }
    });
});

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

$(function () {
    $('button:contains("HIDE")').click(function () {
        if ($(this).text() == "HIDE") {
            $(this).text("SHOW");
        }
        else {
            $(this).text("HIDE");
        }
        ;
        job_id = $(this).attr("data-job_id");
        $('#' + job_id).toggle();
    });
});

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