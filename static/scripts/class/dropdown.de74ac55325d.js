class Dropdown {
    state = false
    open(element) {
        this.state = true
        const containerId = element.dataset.elementId
        const dropdown = document.querySelector(`#${containerId}`);

        element.classList.toggle('button-active')
        if (element.classList.contains('button-active')) {
            dropdown.style.maxHeight = dropdown.scrollHeight + '8px';
            dropdown.style.padding = ".5rem 0"
            
        } else {
            dropdown.style.maxHeight = 0;
            dropdown.style.padding = 0;
            this.state = false
        }
    }
}

dropdown = new Dropdown();