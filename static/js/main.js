    const increaseButtons = document.querySelectorAll('.qty-increase');
    const decreaseButtons = document.querySelectorAll('.qty-decrease');


    increaseButtons.forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.getAttribute('data-product-id');
            const quantityInput = document.getElementById(`product-quantity-${productId}`);
            
            let currentValue = parseInt(quantityInput.value) || 0;
            quantityInput.value = currentValue + 1;
        });
    });

    decreaseButtons.forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.getAttribute('data-product-id');
            const quantityInput = document.getElementById(`product-quantity-${productId}`);
            
            let currentValue = parseInt(quantityInput.value) || 0;
            if (currentValue > 1) {
                quantityInput.value = currentValue - 1;
            }
        });
    });