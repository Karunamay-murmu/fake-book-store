const button = document.querySelectorAll(".accordion__button")
button.forEach(btn => {
    btn.onclick = () => {
        if (btn.dataset.type === 'link') {
            const redirect = btn.dataset.url
            const next = window.location.pathname
            window.location.replace(`${redirect}?next=${next}`)
            return
        }
        const content = btn.parentElement.nextElementSibling;
        const parent = content.parentElement;
        parent.classList.toggle('accordion--active')
        if (parent.classList.contains('accordion--active')) {
            content.style.maxHeight = content.scrollHeight + 'px'
            content.style.margin = "1rem 0 0 0"
        } else {
            content.style = {
                maxHeight: 0,
                marginTop: 0
            }
        }
    }
})
