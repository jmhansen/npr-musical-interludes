
function playAudio(music, icon) {
	if (music.paused) {
		music.play();
        icon.html('pause_circle_filled');
	} else {
        music.pause();
        icon.html('play_circle_filled');
    }
}

$('.play').hover(
    function() {
        var $music = $(this).next('audio')[0]
        if ($music.paused) {
            $(this).html('play_circle_filled');
        } else {
            $(this).html('pause_circle_filled');
        }
    },function() {
        var $music = $(this).next('audio')[0]
        if ($music.paused) {
            $(this).html('play_circle_outline');
        } else {
            $(this).html('pause_circle_outline');
        }
    });


$('.play').click(function() {
    var $this = $(this)
    var $music = $this.next('audio')[0]
    playAudio($music, $this);
})
