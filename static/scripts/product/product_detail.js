const increaseQuantity = () => {
    const count = document.querySelector("#id_quantity")
    count.textContent = Number(count.textContent) + 1
}

const decreaseQuantity = () => {
    const count = document.querySelector("#id_quantity");
    const qty = Number(count.textContent);
    if (qty > 1) {
        count.textContent = qty - 1
    }
}   