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


                let _html = '<!-- Single Review -->';
                    _html += '<div class="single-review">'
                    _html += '<!-- Review User Logo & Username -->';
                    _html += '<div class="review-header">';
                    _html += '<img src='+ adminLogoUrl +'alt="User Avatar" class="review-avatar" />';
                    _html += '<a href="#" class="review-username">'+ response.context.user +'</a>';
                    _html += '</div>';

                    _html += '<!-- Review Content -->';
                    _html += '<div class="review-content">';
                    _html += '<p>'+ response.context.review  +'</p>';
                    _html += '</div>';

                    _html += '<!-- Review Date -->';
                    _html += '<div class="review-date">';
                    _html += '<span>'+ time +'</span>';
                    _html += '</div>';

                    _html += '<!-- Review Rating -->';
                    _html += '<div class="review-rating">';

                    for(let i = 1; i <= response.context.rating; i++){
                        _html += '<span>★</span>';
                    }

                    _html += '</div>';
                    _html += '</div>';

                    $(".reviews").prepend(_html); 
            }
        }
    });
});