(() => {
    function isElementVisible(el) {
        let rect = el.getBoundingClientRect(),
            vWidth = window.innerWidth || document.documentElement.clientWidth,
            vHeight = window.innerHeight || document.documentElement.clientHeight,
            efp = function (x, y) {
                return document.elementFromPoint(x, y)
            };

        if (rect.right < 0 || rect.bottom < 0
            || rect.left > vWidth || rect.top > vHeight)
            return false;

        return (
            el.contains(efp(rect.left, rect.top))
            || el.contains(efp(rect.right, rect.top))
            || el.contains(efp(rect.right, rect.bottom))
            || el.contains(efp(rect.left, rect.bottom))
        );
    }

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
                if (!isElementVisible(parent)) {
                    parent.scrollIntoView()
                }
            }
        }
    })
})()