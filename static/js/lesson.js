(() => {
    const setLessonID = () => {
        let lesson_element = document.getElementById('lesson_id')
        document.lesson_id = lesson_element.getAttribute('data-value')
    }
    setLessonID()

    htmx.on("htmx:afterRequest", e => {
        if (e.detail.target.id === 'video') {
            setLessonID()
            let course_id = JSON.parse(document.getElementById('course_id').textContent)
            window.history.pushState("", "", `/students/course/${course_id}/lesson/${document.lesson_id}/`);
            fetch(`/students/course/update_lesson/${course_id}/`, {
                method: 'post',
                body: JSON.stringify({'lesson_id': document.lesson_id}),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                }
            }).then((response) => response.json())
        }
    })
})()
