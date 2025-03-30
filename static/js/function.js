console.log('Working fine');

document.addEventListener('DOMContentLoaded', () => {
    const slider = document.querySelector('.price-slider input[type="range"]');
    const sliderContainer = document.querySelector('.price-slider');
    const increaseButton = document.querySelectorAll('#prc-increase');
    const decreaseButton = document.querySelectorAll('#prc-decrease');
    const priceInput = document.querySelectorAll('.prc-input');
    const tabs = document.querySelectorAll('.navbar__link');
    const contents = document.querySelectorAll('.tab-content');
    const forms = document.querySelector(".forms");

    setTimeout(() => {
        const messages = document.querySelectorAll('.msg');
        messages.forEach(message => {
            message.style.transition = 'opacity 0.5s ease';
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500);
        });
    }, 2000);

    const toggleSliderActive = (isActive) => {
        sliderContainer.classList.toggle('price-slider-active', isActive);
    };

    pwShowHide = document.querySelectorAll(".eye-icon");
    pwShowHide.forEach(eyeIcon => {
    eyeIcon.addEventListener("click", () => {
        let pwFields = eyeIcon.parentElement.parentElement.querySelectorAll(".password");
        pwFields.forEach(password => {
        if (password.type === "password") { // If password is hidden
            password.type = "text"; // Show password
            eyeIcon.classList.replace("bx-hide", "bx-show"); // Change icon to show state
            return;
        }
        password.type = "password"; // Hide password
        eyeIcon.classList.replace("bx-show", "bx-hide"); // Change icon to hide state
        });
    });
    });

    increaseButton.forEach((increaseBtn, index) => {
        increaseBtn.addEventListener('click', () => {
            priceInput[index].stepUp();
        });
    });

    decreaseButton.forEach((decreaseBtn, index) => {
        decreaseBtn.addEventListener('click', () => {
            priceInput[index].stepDown();
        });
    });

    tabs.forEach((tab, index) => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));
            
            tab.classList.add('active');
            contents[index].classList.add('active');
        });
    })

    if (slider) {
        slider.addEventListener('mousedown', () => toggleSliderActive(true));
        slider.addEventListener('mouseup', () => toggleSliderActive(false));
        slider.addEventListener('mouseleave', () => toggleSliderActive(false));
        slider.addEventListener('touchstart', () => toggleSliderActive(true));
        slider.addEventListener('touchend', () => toggleSliderActive(false));
    
        slider.addEventListener('click', (event) => {
            event.preventDefault();
            event.stopPropagation();
        });
    }

    const viewUnpaid = document.getElementById('show-unpaid');
    const unpaidOrders = document.getElementsByClassName('unpaid-orders-container');

    if (viewUnpaid) {
        viewUnpaid.addEventListener('click', () => {
            if (unpaidOrders[0].style.display === 'block') {
                unpaidOrders[0].style.display = 'none';
            } else {
                unpaidOrders[0].style.display = 'block';
            }
        });
    }

    const fileInput = document.getElementById('id_image');
    const currentlyInput = document.getElementById('currently');

    // product preview
    const title = document.getElementById('id_title');
    const description = document.getElementById('id_description');
    const price = document.getElementById('id_price');
    const old_price = document.getElementById('id_old_price');
    const category = document.getElementById('id_category');

    const prev_title = document.getElementById('prev-title');
    const prev_desc = document.getElementById('prev-desc');
    const prev_price = document.getElementById('prev-price');
    const prev_old_price = document.getElementById('prev-old-price');
    const prev_category = document.getElementById('prev-ctitle');
    const prev_disc = document.getElementById('prev-disc');
    const prev_image = document.getElementById('prev-img');

    const bars = document.querySelector('.bars');
    const dropdown = document.querySelector('.bars-dropdown');

    const close_sidecart = document.getElementById('closeCart');
    const side_cart = document.getElementById('cart-sidebar');

    const navbar = document.querySelector('.navbar');
    const navbar_open = document.querySelector('.navbar__open');
    const navbar_close = document.querySelector('.navbar__close');

    if (bars) {
        bars.addEventListener('click', () => {
            dropdown.style.display = getComputedStyle(dropdown).display === 'flex' ? 'none' : 'flex';
        });
    
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.bars') && !e.target.closest('.dropdown')) {
                dropdown.style.display = 'none';
            }
        });
    }

    if (navbar_open || navbar_close) {
        navbar_open.addEventListener('click', () => {
            navbar.style.display = "flex";
            navbar_open.style.display = "none";
        });
    
        navbar_close.addEventListener('click', () => {
            navbar.style.display = "none";
            navbar_open.style.display = "flex";
        });
    }

    if (close_sidecart) {
        close_sidecart.addEventListener('click', () => {
            side_cart.classList.add('hidden');
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
    
                reader.onload = function(e) {
                    currentlyInput.value = file.name;
                    prev_image.src = e.target.result;
                };
    
                reader.readAsDataURL(file);
            }
        });
    }

    if (title || description || category || price || old_price) {
        function truncateText(text, maxLength = 75) {
            return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
        }

        title.addEventListener('input', () => {
            prev_title.textContent = title.value || '';
        });
    
        description.addEventListener('input', () => {
            prev_desc.textContent = truncateText(description.value);
        });
    
        category.addEventListener('input', () => {
            prev_category.textContent = category.value || '';
        });
    
        price.addEventListener('input', () => {
            prev_price.textContent = price.value || '0.00';
        });
    
        old_price.addEventListener('input', () => {
            const oldPriceValue = parseFloat(old_price.value) || 0;
            const priceValue = parseFloat(price.value) || 0;
            prev_old_price.textContent = oldPriceValue ? `$${oldPriceValue.toFixed(2)}` : '0.00';
    
            const discount = oldPriceValue > 0 ? (((oldPriceValue - priceValue) / oldPriceValue) * 100).toFixed(0) : 0;
            prev_disc.textContent = `-${discount}%`;
        });
    }
});

const monthNames = ["Jan", "Feb", "Mar", "April",
    "May", "June", "July", "Aug", "Sept", "Oct",
    "Nov", "Dec"
];

const mainImage = document.getElementById('mainImage');
    
    function changeMainImage(clickedExtraImage) {
        const newMainImageUrl = clickedExtraImage.src;
    
        if (mainImage.src === newMainImageUrl) return;
        
        mainImage.classList.add('fade-out');
    
         setTimeout(() => {
            mainImage.src = newMainImageUrl;
            mainImage.classList.remove('fade-out');
        }, 300);
    }
    
let currentIndex = 0;

function handleSearch() {
    document.querySelector('#search-form').style.display = 'block';
    
    document.getElementById('wishlist-cont').style.display = 'none';
    document.getElementById('cart-cont').style.display = 'none';
}

function moveSlide(direction) {
    const slides = document.querySelector('.slides');
    const totalSlides = slides.children.length;
    const maxIndex = totalSlides - 3;

    currentIndex += direction;

    if (currentIndex < 0) {
        currentIndex = maxIndex;
    } else if (currentIndex > maxIndex) {
        currentIndex = 0;
    }

    slides.style.transform = `translateX(-${currentIndex * 75}%)`;

}

function initializeDropdown(barsSelector, dropdownSelector, svgBtnsSelector) {
    const bars = document.querySelector(barsSelector);
    const dropdown = document.querySelector(dropdownSelector);
    const svg_btns = document.querySelector(svgBtnsSelector);

    if (!bars || !dropdown || !svg_btns) {
        console.error("Один или несколько элементов не найдены!");
        return;
    }

    // Обработчик для открытия/закрытия меню
    bars.addEventListener('click', () => {
        dropdown.style.display = dropdown.style.display === 'flex' ? 'none' : 'flex';
    });

    // Обработчик для кликов вне меню
    svg_btns.addEventListener('click', (e) => {
        if (!bars.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });
}

$(document).ready(function () {
    // Decrease quantity
    $(document).on("click", ".decrease", function () {
        let productId = $(this).attr("data-product");
        let quantityInput = $("#product-quantity-" + productId);
        let currentValue = parseInt(quantityInput.text()) || 0; // Ensure currentValue is a valid number

        if (currentValue > 1) {
            quantityInput.text(currentValue - 1); // Decrease value
        }
    });

    // Increase quantity
    $(document).on("click", ".increase", function () {
        let productId = $(this).attr("data-product");
        let quantityInput = $("#product-quantity-" + productId);
        let currentValue = parseInt(quantityInput.text()) || 0; // Ensure currentValue is a valid number

        quantityInput.text(currentValue + 1); // Increase value
    });
});

$(document).ready(function (){
    $("#reviewForm").on("submit", function(event){
        event.preventDefault();
    
        let dt = new Date();
        let time = dt.getUTCDate() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()
    
        $.ajax({
            data: $(this).serialize(),
            method: $(this).attr("method"),
            url: $(this).attr("action"),
            dataType: "json",
            success: function(response){
                console.log('Review saved to DB...');
                
                if (response.bool == true){
                    $("#review-container").html('<div class="msg msg-success"><p>Review added successfully</p></div>');
                    $(".hide-review").hide();
                    $(".hide-review-form").hide();$(".rating-bg").val(response.avg_reviews.rating);
                    $("#avg-rating-count").text(response.avg_reviews.rating.toFixed(1));
                    $(".5star").val(response.rating_prc["5"]);
                    $(".4star").val(response.rating_prc["4"]);
                    $(".3star").val(response.rating_prc["3"]);
                    $(".2star").val(response.rating_prc["2"]);
                    $(".1star").val(response.rating_prc["1"]);

                    setTimeout(() => {
                        const messages = document.querySelectorAll('.msg');
                        messages.forEach(message => {
                            message.style.transition = 'opacity 0.5s ease';
                            message.style.opacity = '0';
                            setTimeout(() => message.remove(), 500);
                        });
                    }, 2000);
    
                    let _html = '<!-- Single Review -->'
                        _html += '<div class="single-review">'
    
                        _html += '<!-- Review User Logo & Username -->'
                        _html += '<div class="review-header">'
                        _html += '<img src="'+ response.profile_image +'" alt="User Avatar" class="review-avatar" id="review-avatar" />'
                        _html += '<p class="review-username">'+ response.context.user +'</p>'
                        _html += '</div>'
    
                        _html += '<!-- Review Content -->'
                        _html += '<div class="review-content">'
                        _html += '<p>'+ response.context.review +'</p>'
                        _html += '</div>'
    
                        _html += '<!-- Review Date -->'
                        _html += '<div class="review-date">'
                        _html += '<span>'+ time +'</span>'
                        _html += '</div>'
    
                        _html += '<!-- Review Rating -->'
                        _html += '<div class="review-rating">'
    
                        _html += '<div class="star-progress">'
                        _html += '<progress class="rating-bg" value="'+ response.context.rating +'" max="5"></progress>'
                        _html += '<svg><use xlink:href="#fivestars"/></svg>'
                        _html += '</div>'
    
                        _html += '</div>'
                        _html += '</div>'
    
                    $(".reviews").prepend(_html); 
                }
            }
        });
    })

    $(".filter-cbx, #price-filter-btn").on("click", function(){
        console.log("A checkbox have been clicked");

        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-cbx").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter='+ filter_key +']:checked')).map(function(element){
                return element.value
            })
        })
        console.log("Filter Object is ", filter_object)
        $.ajax({
            url: '/filter-product',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log("Trying to filter products...");
            },
            success: function(response){
                console.log(response);
                console.log("Data filtered successfully...")
                $("#filtered-product").html(response.data)
            }
        })
    })

    $("#max_price").on("blur", function(){
        let min_price = $(this).attr("min");
        let max_price = $(this).attr("max");
        let current_price = $(this).val();

        if(current_price < parseFloat(min_price)){
            min_price = Math.round(min_price * 100) / 100
            
            alert("The price you specified is below the range")
            $(this).val(min_price)
            $('#range').val(min_price)
        }
        else if(current_price > parseFloat(max_price)){
            max_price = Math.round(max_price * 100) / 100

            alert("The price you is above the range")
            $(this).val(max_price)
            $('#range').val(max_price)
            $(this).focus()

            return false
        }
    })

    $(document).on("click", ".add-to-cart-btn", function(){

        let this_val = $(this)
        let index = this_val.attr("data-index")
    
        let quantity = $(".product-quantity-" + index).val()
        let product_title = $(".product-title-" + index).val()
        let product_id = $(".product-id-" + index).val()
        let product_pid = $(".product-pid-" + index).val()
        let product_price = $(".current-price-" + index).text()
        let product_image = $(".product-image-" + index).val()
        
    
        console.log("Quantity: ", quantity);
        console.log("Title: ", product_title);
        console.log("ID: ", product_id);
        console.log("Price: ", product_price);
        console.log("PID: ", product_pid);
        console.log("Current Element: ", this_val);
        console.log("Product Image: ", product_image)
    
        if (parseInt(quantity) < 1) {
            alert("The quantity you specified is below than 1");
            this_val.val(1)
            return false;
        }
        else {
            $.ajax({
                url: '/add-to-cart',
                data: {
                    'id': product_id,
                    'pid': product_pid,
                    'quantity': quantity,
                    'title': product_title,
                    'price': parseFloat(product_price),
                    'image': product_image,
                },
                dataType: 'json',
                beforeSend: function(){
                    console.log("Adding products to cart...");
                },
                success: function(response){
                    console.log("Added products to cart...");
                    $("#cart-sidebar").removeClass('hidden');
                    $(".cart-count").text(response.total_cart_items).hide().fadeIn(500);

                    renderCart(response.cart_data);
                },
                error: function(){
                    console.log("Failed to add products to cart...")
                }
            })
        }
    
    })

    function renderCart(cartData) {
        console.log("Rendering Cart:", cartData);  // Log the cart data to verify it's being passed
        let $cartSidebarItems = $(".cart-sidebar-items");
        $cartSidebarItems.empty(); // Clear existing items
    
        // Loop through cart data and regenerate HTML
        for (let productId in cartData) {
            let product = cartData[productId];
            $cartSidebarItems.append(`
                <div class="cart-sidebar-item">
                    <img src="${product.image}" alt="${product.title}" />
                    <div class="cart-sidebar-item-details">
                        <div class="line">
                            <h3>${product.title}</h3>
                            <p class="price"><span>$</span><span>${product.price}</span></p>
                        </div>
                        <div class="btns">
                            <div class="quantity-controls">
                                <button class="decrease" data-product="${productId}">-</button>
                                <span class="quantity" id="product-quantity-${productId}">${product.quantity}</span>
                                <button class="increase" data-product="${productId}">+</button>
                            </div>
                            <button class="delete-side-product" data-product="${productId}"><i class="fa-solid fa-trash-can"></i></button>
                            <button class="update-side-product" data-product="${productId}"><i class="fa-solid fa-arrows-rotate"></i></button>
                        </div>
                    </div>
                </div>
            `);
        }
    }
    
    $(document).on("click", ".delete-product", function(){
    
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
    
        console.log("Product ID: ", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-count").text(response.total_cart_items)
                $("#cart-page").html(response.data)
            }
        })

    })

    $(document).on("click", ".delete-side-product", function(){
    
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
    
        console.log("Product ID: ", product_id);

        $.ajax({
            url: "/delete-from-side-cart",
            data: {
                "id": product_id,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                this_val.closest(".cart-sidebar-item").remove();
                $(".cart-count").text(response.total_cart_items)
            }
        })

    })

    $(document).on("click", ".update-product", function(){
    
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let quantity = $("#product-quantity-" + product_id).text()
    
        console.log("Product ID: ", product_id);
        console.log("Product Quantity: ", quantity);

        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "quantity": quantity,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-count").text(response.total_cart_items)
                $("#cart-page").html(response.data)
            }
        })

    })
    
    $(document).on("click", ".update-side-product", function(){
    
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let quantity = $("#product-quantity-" + product_id).text()
    
        console.log("Product ID: ", product_id);
        console.log("Product Quantity: ", quantity);

        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "quantity": quantity,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-count").text(response.total_cart_items)
                $("#cart-page").html(response.data)
            }
        })

    })

    $(document).on("click", ".qty-increase", function() {
        const productId = $(this).attr("data-product-id");
        const quantityInput = $("#product-quantity-" + productId);

        let currentValue = parseInt(quantityInput.val()) || 0;
        quantityInput.val(currentValue + 1);
    });

    $(document).on("click", ".qty-decrease", function() {
        const productId = $(this).attr("data-product-id");
        const quantityInput = $("#product-quantity-" + productId);

        let currentValue = parseInt(quantityInput.val()) || 0;
        if (currentValue > 1) {
            quantityInput.val(currentValue - 1);
        }
    });

    // Making Address Default
    $(document).on("click", ".make-default", function(){
        let id = $(this).attr("data-address-id")
        let this_val = $(this)

        console.log("ID:", id);
        console.log("Element:", this_val)

        $.ajax({
            url: "/customer/make-address-default",
            data: {
                "id": id,
            },
            dataType: "json",
            success: function(response){
                console.log("Address is now Default");
                if (response.boolean == true){

                    $(".default").hide()
                    $(".action_btn").show()

                    $(".check-" + id).show()
                    $(".button-" + id).hide()
                }
            }
        })
    })

    $(document).on("click", ".remove-default", function(){
        let id = $(this).attr("data-address-id")
        let this_val = $(this)

        var target = this_val.closest(".address-card")

        console.log("ID:", id);
        console.log("Element:", this_val)

        function removeElement(target) {
            target.animate({
              opacity: "-=1"
            }, 1000, function() {
              target.remove();
            });
          }

        $.ajax({
            url: "/customer/remove-address",
            data: {
                "id": id,
            },
            dataType: "json",
            beforeSend: function(){
                console.log("removing address")
            },
            success: function(response){
                removeElement(target);
                setTimeout(function() {
                    $("#address-container").html(response.data);
                }, 1000);
            }
        })
    })

    // Adding to wishlist
    $(document).on("click", ".add-to-wishlist", function(){
        let product_id = $(this).attr("data-product-item")
        let in_wishlist = $(this).attr("in-wishlist")
        let isInWishlist = in_wishlist === "true";
        let this_val = $(this)

        console.log("ID:", product_id)
        console.log("Current element: ", this_val);
        
        $.ajax({
            url: isInWishlist ? "/remove-from-wishlist-card" : "/add-to-wishlist",
            data: {
                "id": product_id,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.html('<i class="fa-solid fa-spinner fa-spin"></i>');
            },
            success: function(response){
                if (response.bool == true) {
                    console.log("Added to wishlist")
                    $(".wishlist-count").text(response.wishlist_count)
                }

                else {
                    $(".wishlist-count").text(response.wishlist_count)
                }

                if (isInWishlist) {
                    this_val.html('<i class="fa-regular fa-heart"></i>');
                    this_val.attr("in-wishlist", "false");
                } else {
                    this_val.html('<i class="fa-solid fa-heart"></i>');
                    this_val.attr("in-wishlist", "true");
                }
            }
        })
    })

    // Remove from wishlist
    $(document).on("click", ".remove-from-wishlist", function(){
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)

        console.log("wishlist ID is:", wishlist_id);

        $.ajax({
            url: "/remove-from-wishlist",
            data: {
                "id": wishlist_id,
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Removing product from wishlist...")
            },
            success: function(response){
                $("#wishlist").html(response.data)
                $(".wishlist-count").text(response.wishlist_count)
            }
        })
    })

    $(document).on("submit", "#contact-form", function(event){
        event.preventDefault()
        
        console.log("Submited...");

        let first_name = $("#first_name").val()
        let last_name = $("#last_name").val()
        let email = $("#email").val()
        let phone_number = $("#phone").val()
        let subject = $("#subject").val()
        let message = $("#message").val()

        $.ajax({
            url:"/customer/ajax-contact-us",
            data: {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone_number": phone_number,
                "subject": subject,
                "message": message,
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Sending data to server...");
            },
            success: function(response){
                console.log("Sent data to server.")
                $("#contact-form").hide()
                $("#contact-img").hide()
                $(".contact-container").hide()
                $("#message-response").show()
            }
        })
    })
})