const fields = document.querySelectorAll(".field--error");
fields.forEach(field => {
    const input = field.previousElementSibling;
    const label = input.previousElementSibling;
    input.classList.add("error-input")
    label.classList.add("error-label")
})