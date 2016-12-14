/**
 * Created by Ericp on 2016-11-18.
 */
function startSurvey(e) {
    if (e.keyCode == 13) {
        e.preventDefault(); // avoid line break
        var but = document.getElementById("start-button");
        but.setAttribute("style", "background-color: #e50914");
        setTimeout(function() {
            window.location.href = "/view_question_1?";
        }, 150);

    }
}