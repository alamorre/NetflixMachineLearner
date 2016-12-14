/**
 * Created by Ericp on 2016-11-18.
 */

// The only reason I need this is because I just can't use autofocus, it causes issue during animation
// We can't focus the textarea until the animation is finished, 800ms would be enough
setTimeout(function () {
    var ans = document.getElementById("ans-textarea");
    ans.focus();
}, 800);

function pressed(e) {

    var ans = document.getElementById("ans-textarea");
    if (e.keyCode == 13) {
        e.preventDefault();
        if (ans.value.trim().length > 0) {
            // TODO: submit to backend for language processing
            alert("language for processing: " + ans.value.trim());
        } else {
            ans.value = "";
            ans.setAttribute("placeholder", "Come on, just tell us something...");
        }
    }
}
