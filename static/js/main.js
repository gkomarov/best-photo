$(document).ready(function () {
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(".take_vote").click(function () {
        let person_id = $(this).parent().attr("person_id")
        let voting_id = $(this).parent().attr("voting_id")
        $.ajax({
            url: 'voting/update',
            method: 'post',
            data: {
                person_id,
                voting_id
            },
            success: function (res) {
                if (res.reach_limit) {
                    console.info(location.host)
                    window.location = 'http://' + location.host + '/voting'
                } else {
                    window.location.reload()
                }
            },
            error: function (e) {
                console.info(e.responseText)
            }
        })
    })
})