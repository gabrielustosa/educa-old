(() => {
    const targetModal = document.querySelector('#modal-note');

    const modal = new Modal(targetModal)

    htmx.on("htmx:afterSwap", e => {
        if (e.detail.target.id === "modal-body") {
            modal.show()
        }
    })

    document.querySelector("#modal-close").addEventListener('click', () => {
        modal.hide()
    })


})()