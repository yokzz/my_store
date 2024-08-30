console.log('Working fine');

const monthNames = ["Jan", "Feb", "Mar", "April",
    "May", "June", "July", "Aug", "Sept", "Oct",
    "Nov", "Dec"
];


$("#reviewForm").submit(function(event){
    event.preventDefault();

    let dt = new Date();
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function(response){
            console.log('Review saved to DB...');
            
            if (response.bool == true){
                $("#review-response").html("Review added successfully");
                $(".hide-review").hide();
                $(".hide-review-form").hide();

                let _html = '<!-- Single Review -->'
                    _html += '<div class="single-review">'

                    _html += '<!-- Review User Logo & Username -->'
                    _html += '<div class="review-header">'
                    _html += '<img src="" alt="User Avatar" class="review-avatar" id="review-avatar" />'
                    _html += '<a href="#" class="review-username">'+ response.context.user +'</a>'
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

                    for(let i = 1; i <= response.context.rating; i++){
                        _html += '<span>★</span>';
                    }

                    _html += '</div>'
                    _html += '</div>'

                $(".reviews").prepend(_html); 
            }
        }
    });
});

$(document).ready(function (){
    $(".filter-checkbox, #price-filter-btn").on("click", function(){
        console.log("A checkbox have been clicked");

        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function(){
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

    $(".add-to-cart-btn").on("click", function(){

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
                    this_val.html('<i class="fas fa-shopping-cart"></i><i class="fa-solid fa-check"></i>');
                    console.log("Added products to cart...");
                    $(".cart-items-count").text(response.total_cart_items)
                },
                error: function(){
                    console.log("Failed to add products to cart...")
                }
            })
        }
    
    })
    
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
                $(".cart-items-count").text(response.total_cart_items)
                $("#cart-page").html(response.data)
            }
        })

    })

    $(document).on("click", ".update-product", function(){
    
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let quantity = $("#product-quantity-" + product_id).val()
    
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
                $(".cart-items-count").text(response.total_cart_items)
                $("#cart-page").html(response.data)
            }
        })

    })
})