class Cart {

    constructor(totalQuantity = "", totalPrice = "", products = {}) {
        this.totalQuantity = totalQuantity
        this.totalPrice = totalPrice
        this.addingQuantity = 1
        this.products = products
    }

    fetchCart(url) {
        return fetch(url, {
            method: 'GET',
            mode: 'same-origin',
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then(stream => stream.json())
            .then(res => {
                return res
            })
            .catch(error => error)
    }

    loading(display, element) {
        const button = element.lastElementChild;
        const loader = element.firstElementChild;
        if (display === 'show') {
            loader.style.display = 'initial'
            button.style.display = 'none'
        }
        else if (display === 'hide') {
            loader.style.display = 'none'
            button.style.display = 'flex'
        }
    }


    setCart(product, totalQuantity, totalPrice) {
        this.totalQuantity = totalQuantity;
        this.totalPrice = totalPrice;
        this.products[`${product.id}`] = { ...product }
    }

    setQuantity = (element) => {
        const count = document.querySelector("#id_quantity")
        const qty = Number(element.dataset.qty)
        this.addingQuantity += qty
        count.textContent = this.addingQuantity
    }


    updateCartTotalQuantity() {
        const qty = document.querySelector("#id_cart-quantity");
        qty.textContent = this.totalQuantity;
    }

    updateCartTotalPrice() {
        console.log("hit")
        const price = document.querySelectorAll(".sub-total");
        console.log(price)
        price.forEach(field => {
            field.textContent = `\$${this.totalPrice}`;
        })
    }

    updateCartItemQuantity(product) {
        const qty = document.querySelector(`#id_quantity${product.id}`)
        const deleteQty = document.querySelector(`#id_delete${product.id}`)
        const totalPrice = document.querySelector(`#id_total-price${product.id}`)
        const {
            quantity,
            price
        } = this.products[product.id]
        const itemTotalPrice = (Number(price) * product.quantity).toFixed(2)
        qty.textContent = quantity
        totalPrice.textContent = itemTotalPrice
        deleteQty.dataset['qty'] = quantity
    }

    async add(element) {
        this.loading('show', element);
        const { url, productId } = element.dataset;
        const fetchURL = url + '?' + new URLSearchParams({
            "productId": productId,
            "quantity": this.addingQuantity
        })
        const {
            product,
            total_quantity,
            total_price,
        } = await this.fetchCart(fetchURL);
        this.setCart(product, total_quantity, total_price)
        this.updateCartTotalQuantity();
        this.updateCartTotalPrice();
        this.loading('hide', element);
    }

    async update(element) {
        const { url, productId, action, qty } = element.dataset;
        const noOfProduct = document.querySelector(`#id_quantity${productId}`).textContent
        if (action === 'remove' && noOfProduct <= 1) {
            return
        }
        const paramObj = {
            "productId": productId,
            "quantity": qty
        }
        if (action === "delete") {
            paramObj['delete'] = true
            const product = document.querySelector(`[data-index='${productId}']`)
            product.remove();
        }
        const fetchURL = url + '?' + new URLSearchParams(paramObj)
        const {
            product,
            total_quantity,
            total_price,
        } = await this.fetchCart(fetchURL);
        this.setCart(product, total_quantity, total_price)
        this.updateCartTotalQuantity();
        action !== "delete" && this.updateCartItemQuantity(product);
        this.updateCartTotalPrice();
        if (this.totalQuantity === 0) {
            window.location.reload();
            return
        }
    }
}

const cart = new Cart()
// CART_TOTAL_QUANTITY, CART_TOTAL_PRICE, CART_PRODUCTS
