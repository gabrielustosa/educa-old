(() => {
    htmx.on('htmx:afterRequest', e => {
        if (e.detail.requestConfig.elt.hasAttribute('hx-error')) {
            let parent = document.querySelector(e.detail.requestConfig.elt.getAttribute('hx-error'))
            parent.innerText = ''
        }
        if (e.detail.xhr.status === 400) {
            if (e.detail.elt.hasAttribute('hx-error')) {
                let messages = e.detail.xhr.responseText.split('&')
                let parent = document.querySelector(e.detail.elt.getAttribute('hx-error'))
                parent.innerText = ''
                for (let message of messages) {
                    let li = document.createElement('li')
                    li.innerText = message
                    parent.appendChild(li)
                }
                parent.scrollIntoView()
            }
        }
    })
})()