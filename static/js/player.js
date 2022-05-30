(async function () {
    const playVideo = videoId => {
        if (player) {
            player.destroy()
        }
        player = new YT.Player('player', {
            'videoId': videoId,
            events: {
                'onStateChange': onPlayerStateChange,
            }
        })
    }
    htmx.on("htmx:afterRequest", e => {
        if (e.detail.target.id === 'video') {
            fetch(`http://${location.host}/api/v1/lesson/${document.lesson_id}`)
                .then((response) => response.json())
                .then(data => playVideo(data.video_id))
        }
    })
})()