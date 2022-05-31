(() => {
    htmx.on("htmx:afterSwap", e => {
        if (e.detail.target.id === "modal-confirm") {
            let modal = new bootstrap.Modal(document.getElementById("confirmation"))
            modal.show()
        }
        if (e.detail.target.id === "modal-note") {
            let modal = new bootstrap.Modal(document.getElementById("anotation"))
            modal.show()
        }
    })
    htmx.on("hidden.bs.modal", () => {
        document.getElementById("confirmation").innerHTML = ""
        document.getElementById("modal-note").innerHTML = ""
    })
})()