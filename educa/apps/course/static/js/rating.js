(() => {
    let course_id = JSON.parse(document.getElementById('course_id').textContent)

    htmx.on('htmx:afterSwap', e => {
        if (e.target.querySelector('#rating-content')) {
            htmx.ajax('GET', `/course/rating/view/${course_id}`, '#rating-list')

            let progressbars = document.querySelectorAll('.progress')
            progressbars.forEach(progress => {
                progress.addEventListener('click', () => {
                    progress.classList.remove('opacity-25')
                    let progress_data = parseInt(progress.getAttribute('data-value'))
                    document.querySelector(`#close-${progress_data}`).classList.remove('hidden')

                    htmx.ajax('GET', `/course/rating/filter/${course_id}/?filter=${progress_data}`, '#rating-list')

                    progressbars.forEach(other_progress => {
                        let other_progress_data = parseInt(other_progress.getAttribute('data-value'))
                        if (other_progress_data !== progress_data) {
                            other_progress.classList.add('opacity-25')
                            document.querySelector(`#close-${other_progress_data}`).classList.add('hidden')
                        }
                    })
                })
            })

            let close_buttons = document.querySelectorAll('.close')
            close_buttons.forEach(close => {
                close.addEventListener('click', () => {
                    close.classList.add('hidden')
                    htmx.ajax('GET', `/course/rating/view/${course_id}`, '#rating-list')
                    progressbars.forEach(progress => {
                        progress.classList.remove('opacity-25')
                    })
                })
            })

            document.querySelector('#select-filter').addEventListener('change', e => {
                document.querySelector('#rating-filter').setAttribute('value', e.target.value)
                let search_value = document.querySelector('#rating-search').value
                if (search_value === "") {
                    htmx.ajax('GET', `/course/rating/filter/${course_id}/?filter=${e.target.value}`, '#rating-list')
                } else {
                    htmx.ajax('GET', `/course/rating/search/${course_id}/?search=${search_value}&filter=${e.target.value}`, '#rating-list')
                }
            })
        }
        if (e.target.id === "rating-list") {
            if (e.detail.requestConfig.path.includes('page')) {
                let elem = document.getElementById('see-more')
                elem.parentNode.removeChild(elem)
            }
        }
    })

})()