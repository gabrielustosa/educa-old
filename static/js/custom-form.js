(() => {
    const getFormInputs = form => {
        let inputs = form.querySelectorAll('input, textarea')
        let values = {}
        inputs.forEach(input => {
            values[input.name] = input.value
        })
        return values
    }

    htmx.on("htmx:configRequest", e => {
        if (e.detail.verb === 'post') {
            if (e.detail.elt.hasAttribute('hx-parent')) {
                let parent_data = e.detail.elt.getAttribute('hx-parent')
                let parent = document.querySelector(parent_data)
                let values = getFormInputs(parent)
                for (const [name, value] of Object.entries(values)) {
                    e.detail.parameters[name] = value
                }
            }
        }
        if (e.detail.target.id !== 'video') {
            e.detail.parameters['lesson_id'] = document.lesson_id
        }
    })
})()