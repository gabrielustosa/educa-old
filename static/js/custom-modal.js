(() => {
    htmx.on("htmx:afterSwap", e => {
        if (e.detail.target.id === "modal") {
            const modal = new bootstrap.Modal(document.getElementById("modal-course"))
            modal.show()
        }
    })
    htmx.on("hidden.bs.modal", () => {
        document.getElementById("modal-course").innerHTML = ""
    })
})()