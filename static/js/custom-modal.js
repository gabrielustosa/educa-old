(() => {
    const targetModal = document.querySelector('#modal');

    const modal = new Modal(targetModal)

    htmx.on("htmx:afterSwap", e => {
        if (e.detail.target.id === "modal-body") {
            modal.show()
            targetModal.querySelector("#modal-close").addEventListener('click', () => {
                modal.hide()
            })
        }
    })
})()