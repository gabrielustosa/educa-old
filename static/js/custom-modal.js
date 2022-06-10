(() => {
    const targetModal = document.querySelector('#modal');

    const modal = new Modal(targetModal)

    htmx.on("htmx:afterSwap", e => {
        if (e.detail.target.id === "modal-body") {
            modal.show()
        }
    })

    window.onclick = e => {
        console.log(e.target.hasAttribute("modal-close"))
        if (e.target.hasAttribute("modal-close")) {
            modal.hide()
        }
    }
})()