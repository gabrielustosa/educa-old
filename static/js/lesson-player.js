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

    htmx.on("htmx:afterSwap", e => {
        if (document.querySelector('#note-content')) {
            let video_timer = document.querySelectorAll('.timer')
            video_timer.forEach(timer => {
                let time = timer.innerText.split(':')
                let total
                if (time.length === 3) {
                    let hours = time[1]
                    let minutes = time[2]
                    let seconds = time[3]
                    total = (+hours) * 60 * 60 + (+minutes) * 60 + (+seconds)
                } else {
                    let minutes = time[0]
                    let seconds = time[1]
                    total = (+minutes) * 60 + (+seconds)
                }
                timer.addEventListener('click', () => {
                    player.seekTo(total)
                })
            })
        }
    })
})()