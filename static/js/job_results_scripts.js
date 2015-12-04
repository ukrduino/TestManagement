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
    $('.removeResultsButton').click(function () {
            var job = $(this).attr("data-delete-job_id")
            $('#' + job).remove();
        }
    );
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

$(document).ready(function () {
        $("input[type='radio']").change(function () {
                var env = $("input[type='radio']:checked").val();
                console.log(env);
                filter_jobs_results_by_env(env);
            }
        );
    }
);

function filter_jobs_results_by_env(env){
    if(env == "ALL"){
        $(".jobs_results_table").show()
    }
    if(env == "AUTO1"){
        $(".jobs_results_table").hide();
        $("[id*='AUTO1']").show()
    }
    if(env == "AUTO2"){
        $(".jobs_results_table").hide();
        $("[id*='AUTO2']").show()
    }
    if(env == "AUTO3"){
        $(".jobs_results_table").hide();
        $("[id*='AUTO3']").show()
    }
    if(env == "AUTO4"){
        $(".jobs_results_table").hide();
        $("[id*='AUTO4']").show()
    }
    if(env == "TEST"){
        $(".jobs_results_table").hide();
        $("[id*='TEST']").show()
    }
    if(env == "DEV1"){
        $(".jobs_results_table").hide();
        $("[id*='DEV1']").show()
    }
    if(env == "FAILED"){
        $(".success_True").hide();
        $(".success_False").show();
    }
    if(env == "PASSED"){
        $(".success_True").show();
        $(".success_False").hide();
    }
}
