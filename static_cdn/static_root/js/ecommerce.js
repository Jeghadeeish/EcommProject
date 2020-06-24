$(document).ready(function(){
    // Contact form handler
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")
    contactForm.submit(function(event){
        event.preventDefault()
        var contactFormData = contactForm.serialize()
        var thisForm = $(this)
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,
            success: function(data){
                contactForm[0].reset()
                contactForm.reset()
                $.alert({
                    title: 'Success!',
                    content: data.message,
                    theme: "modern",
                });
            },
            error: function(error){
                console.log(error.responseJSON)
                var jsonData = error.responseJSON
                var msg = ""
                $.each(jsonData, function(key, value){
                    msg += key + ": " + value[0].message + "<br/>"
                })
                
                $.alert({
                    title: 'Oops!',
                    content: msg,
                    theme: "modern",
                });
            }
            
        })
    })

    // Auto Search
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']")     // Input name='q'
    var typingTimer;
    var typingInterval = 1000    // .5 seconds
    var searchBtn = searchForm.find("[type='submit']")

    searchInput.keyup(function(event){
        // console.log(event)
        // console.log(searchInput.val())
        // key released
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
    })

    searchInput.keydown(function(){
        // key pressed
        clearTimeout(typingTimer)
    })

    function doSearch(){
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
    }

    function performSearch(){
        doSearch()
        var query = searchInput.val()
        setTimeout(function(){
            window.location.href='/search/?q=' + query
        }, 1000)
    }

    // Cart + Add Products
    var productForm = $(".form-product-ajax")   // form selector
    
    productForm.submit(function(event){         
        event.preventDefault();                 // default action
        var thisForm = $(this)
        var actionEndpoint = thisForm.attr("data-endpoint");   // where its going
        var httpMethod = thisForm.attr("method");       // method
        var fromData = thisForm.serialize();             // 

        $.ajax({                // asynchronous java script request
            url: actionEndpoint,
            method:httpMethod,
            data: fromData,
            success: function(data){
                console.log("success") 
                console.log(data)
                console.log("Added",data.added)
                console.log("Removed",data.removed)
                var submitSpan = thisForm.find(".submit-span")
                if (data.added){
                    submitSpan.html("In cart <button type='submit' class='btn btn-link'>Remove</button>")
                } else {
                    submitSpan.html("<button type='submit' class='btn btn-success'>Add to cart</button>")
                }
                // console.log(submitSpan.html())
                var navbarCount = $(".navbar-cart-count")
                navbarCount.text(data.cartItemCount)
                var currentPath = window.location.href
                if (currentPath.indexOf("cart") != -1) {
                    refreshCart()
                }
                },
            error: function(errorData){
                $.alert({
                    title: 'Oops!',
                    content: 'An error occurred!',
                    theme: "modern",
                });
                // console.log("error")
                // console.log(errorData)
            }

        })
    }) 
    function refreshCart(){
        console.log("in current cart")
        var cartTable = $(".cart-table")
        var cartBody = cartTable.find(".cart-body")
        // cartBody.html("<h1>Changed</h1>")
        var productRows = cartBody.find(".cart-product")
        var currentUrl = window.location.href

        var refreshCartUrl = '/api/cart/'
        var refreshCartMethod = 'GET';
        var data = {};
        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data: data,
            success: function(data){
                console.log("success")
                console.log(data)
                var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
                if (data.products.length > 0){
                    productRows.html(" ")
                    // productRows.html("<tr><td colspan=3>Coming Soon</td></tr>")
                    i = data.products.length
                    $.each(data.products, function(index, value){
                        console.log(value)
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                        newCartItemRemove.css("display","block")
                        newCartItemRemove.find(".cart-item-product-id").val(value.id)
                        cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.name + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td</tr>")
                        i --
                    })
                    // cartBody.prepend("<tr><th scope=\"row\">{{ forloop.counter }}</th><td colspan=3> Coming Soon</td></tr>")
                    cartBody.find(".cart-subtotal").text(data.subtotal)
                    cartBody.find(".cart-total").text(data.total)
                } else {
                    window.location.href = currentUrl
                }
            },
            error: function(errorData){
                // console.log("error")
                // console.log(errorData)
                $.alert({
                    title: 'Oops!',
                    content: 'An error occurred!',
                    theme: "modern",
                });
            }
        })
    }
})