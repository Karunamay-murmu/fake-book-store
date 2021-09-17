function productSlider() {
    const leftArrow = document.querySelector('#id_left-arrow')
    const rightArrow = document.querySelector('#id_right-arrow')
    leftArrow.addEventListener('click', function () {
        const slider = document.querySelector('#id_slider')
        slider.scrollLeft -= 276
    })
    rightArrow.addEventListener('click', function () {
        const slider = document.querySelector('#id_slider')
        slider.scrollLeft += 276
    })
}
productSlider()