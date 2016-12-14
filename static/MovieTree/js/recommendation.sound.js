/**
 * Created by Ericp on 2016-11-19.
 */

var sound = new Howl({
    src: ["static/MovieTree/mp3/recommendation.mp3"]
});

setTimeout(function () {
    sound.play();
}, 2000);
