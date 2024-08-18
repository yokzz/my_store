console.log('Working fine')

$("#reviewForm").submit(function(event){
    event.preventDefault();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(response){
            console.log('Review saved to DB...');
        
            if (response.bool == true){
                $("#review-response").html("Review added successfully")
            }
        },
    })
});
