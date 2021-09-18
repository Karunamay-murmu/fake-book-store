function mobileMenu() {
    const svg = `<svg width="20px" height="18px"> <path fill-rule="evenodd" fill="rgb(25, 17, 11)" d="M-0.000,-0.000 L20.000,-0.000 L20.000,2.000 L-0.000,2.000 L-0.000,-0.000 Z"></path> <path fill-rule="evenodd" fill="rgb(25, 17, 11)" d="M-0.000,8.000 L15.000,8.000 L15.000,10.000 L-0.000,10.000 L-0.000,8.000 Z"></path> <path fill-rule="evenodd" fill="rgb(25, 17, 11)" d="M-0.000,16.000 L20.000,16.000 L20.000,18.000 L-0.000,18.000 L-0.000,16.000 Z"></path> </svg>`
    const nav = document.getElementById('id_nav')
    const logo = document.getElementById('id_logo')
    const div = document.createElement('div');
    const width = window.matchMedia("(max-width: 1200px)")

    div.setAttribute('id', 'id_mobile-menu')
    div.setAttribute('onclick', 'toggleMobileMenu()')
    div.dataset['action'] = 'open'
    div.classList.add('m-menu-icon');
    div.innerHTML = svg

    const category = document.querySelector('#id_navbar-category-wrapper')
    const onWindowMatch = () => {
        nav.insertBefore(div, logo)
        category.style.display = 'none'
    }
    if (width.matches) {
        onWindowMatch()
    }

    width.addEventListener('change', () => {
        if (width.matches) {
            onWindowMatch()
        } else {
            const menuIcon = document.getElementById('id_mobile-menu')
            menuIcon.remove()
            category.style.display = 'initial'
        }
    })
}

mobileMenu();

function toggleMobileMenu() {
    const mobileMenu = document.querySelector("#id_m-menu")
    mobileMenu.classList.toggle('show-m-menu')
    document.querySelector('body').classList.toggle('fixed-body-on-scroll')
}

const stack = []

function showSubMenu(element) {
    const id = element.dataset['child']
    const menu = document.querySelector(`#${id}`)

    menu.style.left = '0px'
    stack.push(menu)
}

function hideSubMenu(element) {
    const menu = element.parentElement
    menu.style.left = `${menu.offsetWidth}px`
    stack.pop()
}