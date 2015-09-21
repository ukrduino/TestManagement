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

$('#get_results_from_jenkins').click(function (event) {
    event.preventDefault();
    $.ajax({
        url: 'get_results_from_jenkins/', //TODO use Django Template tags
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
    $('a[class=job_title_link]').click(function () {
        job_id = $(this).attr("data-job_id");
        $.ajax({
            url: 'http://127.0.0.1:8000/acceptance_jobs/' + job_id,
            //url: 'acceptance_jobs/' + job_id,
            type: 'get',
            success: tests_for_job,
            dataType: 'html'

        });
    });
});

function tests_for_job(data) {
    $('#' + job_id).html(data);
}

