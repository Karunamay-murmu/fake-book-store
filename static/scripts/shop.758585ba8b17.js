const expand = document.querySelectorAll('.expand-filter')
expand.forEach(btn => {
    btn.addEventListener('click', () => {
        const accordion = btn.parentElement.nextElementSibling;
        btn.innerHTML = '<path d="M0 0h24v24H0V0z" fill="none"/><path d="M19 13H5v-2h14v2z"/>'
        accordion.classList.toggle('hide-filter')
        if (accordion.classList.contains('hide-filter')) {
            accordion.style.maxHeight = accordion.scrollHeight + 'px';
        } else {
            accordion.style.maxHeight = 0 + 'px';
            btn.innerHTML =
                '<path d="M0 0h24v24H0V0z" fill="none" /><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />'
        }
    })
})

const sliderMinValue = document.querySelector('#id_filter-price-min')
const sliderMaxValue = document.querySelector('#id_filter-price-max')
const slider1 = document.querySelector('#id_range-1');
const slider2 = document.querySelector('#id_range-2');
const sliderTrack = document.querySelector('#id_slider-track')

const sliderGap = 10

if (window.location.search) {
    const urlSearchParams = new URLSearchParams(window.location.search);
    const p_min = urlSearchParams.get('p_min')
    const p_max = urlSearchParams.get('p_max')
    if (p_min && p_max) {
        slider1.value = p_min
        slider2.value = p_max
    }
}

function sliderRange1() {
    if (parseInt(slider2.value) - parseInt(slider1.value) <= sliderGap) {
        slider1.value = parseInt(slider2.value) - sliderGap;
    }
    sliderMinValue.textContent = slider1.value;
    fillColor();
}

function sliderRange2() {
    if (parseInt(slider2.value) - parseInt(slider1.value) <= sliderGap) {
        slider2.value = parseInt(slider1.value) + sliderGap;
    }
    sliderMaxValue.textContent = slider2.value;
    fillColor();
}

function fillColor() {
    const percent1 = (slider1.value / slider1.max) * 100;
    const percent2 = (slider2.value / slider2.max) * 100;
    sliderTrack.style.background =
        `linear-gradient(to right, #156b6a33 ${percent1}%, #156b6a ${percent1}%, #156b6a ${percent2}%, #156b6a33 ${percent2}%)`;
}
fillColor()