// DATA COLLECTION PAGE

// ON PAGE LOAD
$(function () {
    updateTimeStamps();
});

$('#parse_java_code').click(function (event) {
    event.preventDefault();
    $.ajax({
        url: 'parse_java_code/',
        type: 'get',
        success: function () {
            alert("Successfully !!!");
            updateTimeStamps();
        }
    });
});

$('#save_instances_to_db').click(function (event) {
    event.preventDefault();
    show_progress_bar('#save_instances_to_db_progress');
    setTimeout(update_progress_bar, 5000);
    displayOverlay("Saving test classes and test cases to DB");
    $.ajax({
        url: 'save_instances/',
        type: 'get',
        success: function () {
            update_progress_bar_to_full();
            removeOverlay();
            alert("Successfully saved test classes and test cases!!!");
            destroy_progress_bar();
            updateTimeStamps();
        }
    });
});

$('.get_jobs').click(function (event) {
    event.preventDefault();
    var jenkins_page = $(this).attr("data-jenkins_page");
    if (jenkins_page == "Acceptance") {
        show_progress_bar('#get_jobs_acceptance_progress');
    }
    if (jenkins_page == "Trunk") {
        show_progress_bar('#get_jobs_trunk_progress');
    }
    if (jenkins_page == "New trunk") {
        show_progress_bar('#get_jobs_new_trunk_progress');
    }
    if (jenkins_page == "All other") {
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
            removeOverlay();
            alert("Successfully saved jobs from " + jenkins_page + " page!!!");
            destroy_progress_bar();
            updateTimeStamps();
        }
    });
});

$('.get_jobs_configs').click(function (event) {
    event.preventDefault();
    var jenkins_page = $(this).attr("data-jenkins_page");
    if (jenkins_page == "Acceptance") {
        show_progress_bar('#get_jobs_configs_acceptance_progress');
    }
    if (jenkins_page == "Trunk") {
        show_progress_bar('#get_jobs_configs_trunk_progress');
    }
    if (jenkins_page == "New trunk") {
        show_progress_bar('#get_jobs_configs_new_trunk_progress');
    }
    if (jenkins_page == "All other") {
        show_progress_bar('#get_jobs_configs_all_other_progress');
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
            updateTimeStamps();
        }
    });
});

$('.get_builds_and_save_results').click(function (event) {
    event.preventDefault();
    var jenkins_page = $(this).attr("data-jenkins_page");
    if (jenkins_page == "Acceptance") {
        show_progress_bar('#get_builds_and_save_results_acceptance_progress');
    }
    if (jenkins_page == "Trunk") {
        show_progress_bar('#get_builds_and_save_results_trunk_progress');
    }
    if (jenkins_page == "New trunk") {
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
            update_progress_bar_to_full();
            removeOverlay();
            alert("Successfully saved build results for jobs from " + jenkins_page + " page!!!");
            destroy_progress_bar();
            updateTimeStamps();
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
            updateTimeStamps();
        }
    });
});

function show_progress_bar(progress_bar) {
    $(progress_bar).html('' +
        '<div class="panel-footer">' +
        '<div class="progress progress-striped">' +
        '<div class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>' +
        '</div>');
}

function destroy_progress_bar() {
    $('.progressDiv').each(function () {
        $(this).html("");
    });
}

//http://stackoverflow.com/a/5109076
function update_progress_bar() {
    $.ajax({
        type: 'post',
        url: 'update_progress_bar/', // or your absolute-path
        data: {
            'process': "updating progress bar",
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        success: function (resp) {
            console.info("Progress bar update ...");
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

function updateTimeStamps() {
    $.ajax({
        url: 'update_time_stamps/',
        type: 'get',
        dataType: 'json',
        success: function (resp) {
            console.info("Response updateTimeStamps");
            //console.log(resp);
            $.each(resp, function (key, val) {
                console.log(key + ' - ' + val);
                var timeStamp = $('#' + key + ' span');
                timeStamp.text(val);
                if (val == "no data") {
                    timeStamp.css({
                        "background-color": "grey"
                    })
                }
                else{
                    timeStamp.css({
                        "background-color": "deepskyblue"
                    })
                }
            });
        }
    });
}
