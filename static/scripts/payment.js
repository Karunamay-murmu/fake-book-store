(() => {
    const cartTotalQuantity = document.querySelector('#id_cart-quantity').textContent;
    if (cartTotalQuantity == 0) {
        return
    }
    const stripe = Stripe('pk_test_51HqGZuGM1S732NcOMOtiofdbPX5K6GiA2GrM54TkPvz52YkEbrSNhcPyoyKJ8TBj2DfqohZPbHHJgZMcxR8dBoV000XMq78gTy')
    const elements = stripe.elements(),
        payoutBtn = document.querySelector("#id_paybtn"),
        paymentForm = document.querySelector("#id_payment-form"),
        formLoadingSpinner = document.querySelector("#id_form-loading-spinner"),
        form = document.querySelector("#id_payment-form"),
        url = payoutBtn.dataset.url;


    function showInputError(id, error) {
        document.querySelector(id).textContent = error ? error.message : "";
    }


    async function fetchSecretKey() {
        try {
            const stream = await fetch(url, {
                method: 'GET',
                mode: 'same-origin',
                headers: {
                    "Content-Type": "application/json",
                },
            })
            const key = await stream.json();
            return key.secret_key;
        } catch (error) {
            return error
        }
    }


    function createElement(name, options) {
        return elements.create(name, {
            style: {
                base: {
                    color: "#2C394B",
                    fontFamily: 'Poppins, sans-serif',
                    fontSmoothing: "antialiased",
                    fontSize: "18px",
                },
                invalid: {
                    fontFamily: 'Poppins, sans-serif',
                    color: "#d11a2a",
                    iconColor: "#d11a2a"
                }
            },
            classes: {
                focus: 'form__element--focus',
                invalid: 'form__element--invalid'
            },
            ...options
        })
    }


    function handleFormSubmit(cardNumber) {
        form.onsubmit = async (event) => {
            event.preventDefault();
            paymentProcessLoading();
            const key = await fetchSecretKey();
            makePayment(cardNumber, key);
        }
    }


    async function makePayment(cardNumber, key) {
        const address = document.querySelector('#id_shipping-address');
        const { addressId, customerId, customerEmail, customerPhone } = address.dataset;
        try {
            const order = await (await fetch('http://127.0.0.1:8000/order/create/', {
                method: 'POST',
                mode: 'same-origin',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": CSRF_TOKEN,
                },
                body: JSON.stringify({
                    key,
                    customerId,
                    addressId
                })
            })).json()
            if (order.create) {
                const customerName = document.querySelector("[data-name='name']").textContent
                const line1 = document.querySelector("[data-address='line1']").textContent
                const city = document.querySelector("[data-address='city']").textContent
                const postal_code = document.querySelector("[data-address='zip']").textContent
                const country = document.querySelector("[data-address='country']").dataset['countryCode']
                try {
                    const result = await stripe.confirmCardPayment(key, {
                        payment_method: {
                            card: cardNumber,
                            billing_details: {
                                email: customerEmail,
                                phone: customerPhone,
                                name: customerName,
                                address: {
                                    line1,
                                    city,
                                    postal_code,
                                    country
                                },
                            },
                        }
                    })
                    console.log(result)
                    if (result.paymentIntent.status === 'succeeded') {
                        window.location.replace(`http://127.0.0.1:8000/order/placed/id/${result.paymentIntent.client_secret}/`)
                    }
                } catch (error) {
                    console.log(error)
                }
            }
        } catch (error) {
            console.log(error)
        }

    }


    async function processPaymentIntent() {

        const cardNumber = createElement("cardNumber", { showIcon: true, iconStyle: 'solid' });
        const expiry = createElement("cardExpiry");
        const cvc = createElement("cardCvc");

        cardNumber.mount("#id_card-element");
        expiry.mount("#id_expiry-element");
        cvc.mount("#id_cvc-element");

        cardNumber.on("change", function (event) {
            payoutBtn.disabled = false;
            showInputError("#id_card-error", event.error)
        });
        expiry.on("change", function (event) {
            payoutBtn.disabled = false;
            showInputError("#id_expiry-error", event.error)
        })
        cvc.on("change", function (event) {
            payoutBtn.disabled = false;
            showInputError("#id_cvc-error", event.error)
        })

        formLoadingSpinner.style.display = "none";
        paymentForm.style.display = "grid";


        handleFormSubmit(cardNumber);
    }

    processPaymentIntent();


    function paymentProcessLoading() {
        const wrapper = document.querySelector("#id_payment-processing-message");
        const message = "Payment is processing. Please do not reload or close the tab";
        const formContainer = document.querySelector("#id_form-container");

        wrapper.innerHTML = message;
        formLoadingSpinner.appendChild(wrapper);
        paymentForm.style.display = "none";
        formLoadingSpinner.style.display = "initial";
        formContainer.style.border = "1px solid #e7e7e9"
        formContainer.style.borderRadius = ".5rem"

    }



})()

