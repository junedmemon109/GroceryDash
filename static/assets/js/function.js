setTimeout(() => {
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        alert.style.display = 'none';
    });
}, 3000);

form = document.getElementById("commentForm")
if (form) {
form.addEventListener("submit", function(event) {
    event.preventDefault();
    console.log(event)

    let dt = new Date();
    let monthNames = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ];
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear();

    // Serialize form data
    const formData = new FormData(this);

    // Get form action and method
    const action = this.getAttribute("action");
    const method = this.getAttribute("method");

    // Construct fetch options
    const options = {
        method: method,
        body: formData
    };

    // Send AJAX request using fetch API
    fetch(action, options)
        .then(response => response.json())
        .then(res => {
            console.log("comment saved to DB..");

            let userName = res.context.user;
            let capitalizedUserName = userName.charAt(0).toUpperCase() + userName.slice(1);

            if (res.bool === true) {
                document.getElementById("review-res").innerHTML = "Review added successfully.";
                document.querySelector(".hide-comment-form").style.display = "none";
                document.querySelector(".add-review").style.display = "none";

                let _html = `<div class="review">
                                <img src="../../static/assets/imgs/user.png" alt="User Avatar" height="60">
                                <div class="review-content">
                                <div>
                                    <p class="reviewer-name"><strong>${capitalizedUserName}</strong> - ${time}</p>
                                    <p class="user-review">${res.context.review}</p>
                                    </div>
                                    <div class="stars">`
                                        for(var i=1; i<=res.context.rating; i++){
                                            _html+=`<i class="fa-solid fa-star"></i>`
                                        }
                                   _html+= `</div>
                                </div>
                            </div>`;
                document.querySelector("#review-section").querySelector("h2").insertAdjacentHTML("afterend", _html);
            }
        })
        .catch(error => {
            // Handle error
            console.error('Error:', error);
        });
});
}


//Add to cart

function initializeAdd(){
// Get all buttons with the class name "add-to-cart-btn"
var buttons = document.querySelectorAll('.add-to-cart-btn');

// Loop through each button and attach a click event listener
buttons.forEach(function (button) {
    button.addEventListener('click', function () {
        var container = button.closest('.products-wrap'); // Find the nearest ancestor with the class 'product-container'
        var index = button.getAttribute("data-index");
        var quantity = Number(container.querySelector(".quantity-"+index).value);
        var product_title = container.querySelector(".product-title-"+index).value;
        var product_id = Number(container.querySelector(".product-id-"+index).value);
        // var product_price = Number(container.querySelector(".price-"+index).textContent);
        var product_pid = container.querySelector(".product-pid-"+index).value;
        // var product_image = container.querySelector(".product-image-"+index).value;

        console.log(quantity)
        console.log(product_title)
        console.log(product_id)
        // console.log(product_price)
        console.log(product_pid)
        // console.log(product_image)
        console.log(index)

        var url = '/add-to-cart';
        var params = {
            id: product_id,
            qty: quantity,
            title: product_title,
            // price: product_price,
            pid: product_pid,
            // image: product_image
        };

        var queryString = Object.keys(params).map(key => key + '=' + encodeURIComponent(params[key])).join('&');

        fetch(url + '?' + queryString)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {

                button.innerText = "✔ Added to cart"
                document.getElementById('count-cart').innerText = data.totalcartitems

                console.log("Added Product to Cart!");
                console.log("Cart data:", data.data);
                console.log("Total cart items:", data.totalcartitems);
                // Handle success response, if needed
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                // Handle error
            });

        console.log("Adding Product to Cart...");
    });

});

//Add to wishlist

// Get all buttons with the class name "add-to-wishlist-btn"
var buttons = document.querySelectorAll('.add-to-wishlist-btn');

// Loop through each button and attach a click event listener
buttons.forEach(function (button) {
    button.addEventListener('click', function () {
        var container = button.closest('.products-wrap'); // Find the nearest ancestor with the class 'product-container'
        var product_id = button.getAttribute("data-product-item");
        console.log(product_id)

        var url = '/add-to-wishlist';
        var params = {
            id: product_id,
        };

        var queryString = Object.keys(params).map(key => key + '=' + encodeURIComponent(params[key])).join('&');

        fetch(url + '?' + queryString)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                button.innerText = "✔"
                if(data.bool == true){
                    // Get the current value as a number
                    var count = parseInt(document.getElementById('count-wishlist').innerText);

                    // Increment the count
                    count += 1;

                    // Update the element's text content with the new count
                    document.getElementById('count-wishlist').innerText = count;

                console.log("Added Product to wishlist!");
                
                // Handle success response, if needed
                }
                
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                // Handle error
            });

        console.log("Adding Product to Wishlist...");
    });

});
}

initializeAdd()


function initialize(){

    const productsQuantity = document.querySelectorAll(".product-quantity");

      productsQuantity.forEach((productQuantity) => {
        const input = productQuantity.querySelector("input[type='text']");
        const upButton = productQuantity.querySelector(".arrow.up");
        const downButton = productQuantity.querySelector(".arrow.down");

        upButton.addEventListener("click", function () {
          input.value = parseInt(input.value) + 1;
        });

        downButton.addEventListener("click", function () {
          if (parseInt(input.value) > 1) {
            input.value = parseInt(input.value) - 1;
          }
        });
      });

// Get all buttons with the class name "delete-product"
var deleteButtons = document.querySelectorAll('.delete-product');

// Loop through each button and attach a click event listener
deleteButtons.forEach(function (button) {
    button.addEventListener('click', function () {
        var container = button.closest('.cart-products'); // Find the nearest ancestor with the class 'cart-products'
        var product_id = container.getAttribute("data-product");

        console.log(product_id);

        var url = '/delete-from-cart';
        var params = {
            id: product_id
        };

        var queryString = Object.keys(params).map(key => key + '=' + encodeURIComponent(params[key])).join('&');

        fetch(url + '?' + queryString)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log("Product deleted from cart");
                document.getElementById('count-cart').innerText = data.totalcartitems;
                document.getElementById('cart-list').innerHTML = data.data;
                // document.getElementById('paraspan').innerText = data.totalcartitems;
                // Hide the deleted product container
                container.style.display = 'none';
                // Handle success response, if needed

                initialize()
                
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                // Handle error
            });

        console.log("Deleting product from Cart...");
    });
});


// Get all buttons with the class name "update-product"
// var updateButtons = document.querySelectorAll('.update-product');

// Get all arrow icons with the class name "arrow"
var updateButtons = document.querySelectorAll('.arrow'); //up or down arrow

// Loop through each button and attach a click event listener
updateButtons.forEach(function (button) {
    button.addEventListener('click', function () {
        var container = button.closest('.cart-products'); // Find the nearest ancestor with the class 'cart-products'
        var product_id = container.getAttribute("data-product");
        var product_qty = Number(container.querySelector(".product-qty-"+product_id).value);
        console.log(product_id, product_qty);

        var url = '/update-cart';
        var params = {
            id: product_id,
            qty: product_qty
        };

        var queryString = Object.keys(params).map(key => key + '=' + encodeURIComponent(params[key])).join('&');

        fetch(url + '?' + queryString)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log("Product updated to cart");
                document.getElementById('count-cart').innerText = data.totalcartitems;
                document.getElementById('cart-list').innerHTML = data.data;
                //document.getElementById('paraspan').innerText = data.totalcartitems;
                
                // Handle success response, if needed
                console.log(data.cart_total_amount)

                initialize()
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                // Handle error
            });

        console.log("Updating product in Cart...");
    });
});


//Removing from wishlist

// Get all buttons with the class name "delete-product"
var deleteButtons = document.querySelectorAll('.delete-wishlist-product');

// Loop through each button and attach a click event listener
deleteButtons.forEach(function (button) {
    button.addEventListener('click', function () {
        var container = button.closest('.cart-products'); // Find the nearest ancestor with the class 'cart-products'
        var product_id = container.getAttribute("data-wishlist-product");

        console.log(product_id);

        var url = '/remove-from-wishlist';
        var params = {
            id: product_id
        };

        var queryString = Object.keys(params).map(key => key + '=' + encodeURIComponent(params[key])).join('&');

        fetch(url + '?' + queryString)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log("Product deleted from wishlist");
                // Get the current value as a number
                var count = parseInt(document.getElementById('count-wishlist').innerText);

                // Increment the count
                count -= 1;

                // Update the element's text content with the new count
                document.getElementById('count-wishlist').innerText = count;

                document.getElementById('wishlist-list').innerHTML = data.data;
            
                // Hide the deleted product container
                container.style.display = 'none';
                // Handle success response, if needed

                initialize()
                
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                // Handle error
            });

        console.log("Deleting product from Wishlist...");
    });
});

}

initialize()


// Making default address

// Get all buttons with the class name "make-default-address"
var defaultButtons = document.querySelectorAll('.make-default-address');

// Loop through each button and attach a click event listener
defaultButtons.forEach(function (button) {
    button.addEventListener('click', function () {
        var container = button.closest('.address'); // Find the nearest ancestor with the class 'cart-products'
        var id = container.getAttribute("data-address-id");

        var url = '/make-default-address';
        var params = {
            id: id
        };

        var queryString = Object.keys(params).map(key => key + '=' + encodeURIComponent(params[key])).join('&');

        fetch(url + '?' + queryString)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log("Product updated to cart");
                if (data.boolean == true){
                    document.querySelectorAll('.check').forEach(function(check) {
                        check.style.display = 'none';
                    });
                    document.querySelectorAll('.make-default-address').forEach(function(btn) {
                        btn.style.display = 'block';
                    });
                    
                    // Show the checkmark for the clicked address and hide its "Make Default" button
                    container.querySelector(".check-" + id).style.display = 'inline-block';
                    container.querySelector(".button-" + id).style.display = 'none';
                    
                    
                }

            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                // Handle error
            });

        console.log("Making default address...");
    });
});




// $(document).ready(function (){
//     $(".filter-checkbox, #price-filter-btn").on("click", function(){
//         console.log("A checkbox have been clicked");
    
//         let filter_object = {}
//         let min_price=$(this).attr("min")
//         let max_price=$(this).val()

//         filter_object.min_price = min_price;
//         filter_object.max_price = max_price;

//         $(".filter-checkbox").each(function(){ 
//             let filter_value = $(this).val()
//             let filter_key = $(this).data("filter") // vendor, category
            
//             // console.log("Filter value is:", filter_value); 
//             // console.log("Filter key is:", filter_key);

//             filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
//                 return element.value;
//             })
//         })

//         console.log("Filter object is: ", filter_object)
//         $.ajax({
//             url: '/filter-products',
//             data: filter_object,
//             beforeSend: function(){
//                 console.log("Trying to filter products...")
//             },
//             success: function(response){
//                 console.log(response)
//                 console.log("Data filtered successfully...")
//                 $("filtered-product").html(response.data)
//             }
//         })
//     })

//     $("#max_price").on("blur", function(){
//         let min_price=$(this).attr("min")
//         let max_price=$(this).attr("max")
//         let current_price=$(this).val()

//         // console.log("current price is: ",current_price)

//         if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
//             console.log("error occured")
//             min_price = Math.round(min_price*100)/100
//             max_price = Math.round(max_price*100)/100

//             // console.log("Max Price: ", max_price)
//             // console.log("Min Price: ", min_price)

//             alert("Price must be between ", min_price, " and ", max_price)
//             $(this).val=min_price
//             $('#range').val(min_price)
//             $(this).focus()
//         }  
//     })
// })


// document.addEventListener('DOMContentLoaded', function () {
//     document.querySelectorAll('.filter-checkbox, #price-filter-btn').forEach(function (element) {
//         element.addEventListener('click', function () {
//             console.log('A checkbox has been clicked');

//             let filter_object = {};
//             let min_price = document.getElementById('range').min;
//             let max_price = document.getElementById('range').value;

//             filter_object.min_price = min_price;
//             filter_object.max_price = max_price;

//             document.querySelectorAll('.filter-checkbox').forEach(function (checkbox) {
//                 let filter_value = checkbox.value;
//                 let filter_key = checkbox.dataset.filter;

//                 filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function (element) {
//                     return element.value;
//                 });
//             });

//             console.log('Filter object is: ', filter_object);

//             // Construct URL with query parameters
//             let url = '/filter-products/?';

//             // Append min_price and max_price to the URL if they are present
//             if (min_price !== undefined && max_price !== undefined) {
//                 url += 'min_price=' + min_price + '&';
//                 url += 'max_price=' + max_price + '&';
//             }

//             // Append category[] to the URL if it is present
//             if (filter_object['category']) {
//                 url += 'category[]=';
//                 url += filter_object['category'].join('&category[]=') + '&';
//             }

//             // Remove trailing '&' if present
//             url = url.replace(/&$/, '');

//             fetch(url)
//             .then(function (response) {
//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }
//                 return response.json();
//             })
//             .then(function (data) {
//                 console.log(data);
//                 console.log('Data filtered successfully...');
//                 document.getElementById('filtered-product').innerHTML = data.data;
//             })
//             .catch(function (error) {
//                 console.error('There was a problem with the fetch operation:', error);
//             });
//         });
//     });

//     document.getElementById('max_price').addEventListener('blur', function () {
//         let min_price = parseFloat(this.min);
//         let max_price = parseFloat(this.max);
//         let current_price = parseFloat(this.value);

//         if (current_price < min_price || current_price > max_price) {
//             console.log('error occurred');
//             min_price = Math.round(min_price * 100) / 100;
//             max_price = Math.round(max_price * 100) / 100;

//             alert('Price must be between ' + min_price + ' and ' + max_price);
//             this.value = min_price;
//             document.getElementById('range').value = min_price;
//             this.focus();
//         }
//     });
// });

            // Define the searchValue variable outside of the event listener
            var searchValue;

            var searchInput = document.querySelector("#searchquery");
            
            if (searchInput){
                searchValue = searchInput.value;
                // Add an event listener for the input event
            searchInput.addEventListener("input", function() {
                // Retrieve the value of the input field
                searchValue = searchInput.value;
                
                // Now you can use the searchValue variable to access the input value
                
            });
            }
            
            // You can use the searchValue variable here or in any other place within the same scope or outer scopes

//**************************************** below is working ************************************************* *

// function handleFilter(){
//     console.log('A checkbox has been clicked');
    
//             let filter_object = {};
//             let sorting = document.getElementById('sorting').value
//             let min_price = document.getElementById('range').min;
//             let max_price = document.getElementById('range').value;

//             filter_object.min_price = min_price;
//             filter_object.max_price = max_price;

//             document.querySelectorAll('.filter-checkbox').forEach(function (checkbox) {
//                 let filter_value = checkbox.value;
//                 let filter_key = checkbox.dataset.filter;

//                 filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function (element) {
//                     return element.value;
//                 });
//             });

//             console.log('Filter object is: ', filter_object);

//             // Construct URL with query parameters
//             let url = '/filter-products/?';

//             url += 'sorting=' + sorting + '&';
//             // Append min_price and max_price to the URL if they are present
//             if (min_price !== undefined && max_price !== undefined) {
//                 url += 'min_price=' + min_price + '&';
//                 url += 'max_price=' + max_price + '&';
//             }

//             if (searchValue){
//                 url += 'search=' + searchValue + '&';
//                 console.log("Search value:", searchValue);
//             }

//             // Append other filter parameters to the URL
//             for (let key in filter_object) {
//                 if (Array.isArray(filter_object[key]) && filter_object[key].length > 0) {
//                     url += key + '=' + filter_object[key].join(',') + '&';
//                 }
//             }

//             // Remove trailing '&' if present
//             url = url.replace(/&$/, '');

//             fetch(url)
//             .then(function (response) {
//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }
//                 return response.json();
//             })
//             .then(function (data) {
                
//                 console.log(data);
//                 console.log('Data filtered successfully...');
//                 document.getElementById('filtered-product').innerHTML = data.data;
                
//                 var productCountHTML;
//                 if (data.count == 1) {
//                     productCountHTML = `We've got <span class="productparaspan">${data.count}</span> product for you!`;
//                 } else {
//                     productCountHTML = `We've got <span class="productparaspan">${data.count}</span> products for you!`;
//                 }

//                 // Set the innerHTML of both elements
//                 document.querySelector('.heading-banner-content>p').innerHTML = productCountHTML;
//                 document.querySelector('.operation-options-2>p').innerHTML = productCountHTML;

//                 initializeRatings()
//             })
//             .catch(function (error) {
//                 console.error('There was a problem with the fetch operation:', error);
//             });
// }


// document.querySelectorAll('.filter-checkbox, #price-filter-btn').forEach(function (element) {
//     element.addEventListener('click', function () {
//         handleFilter()
//     });
// });

// document.getElementById('sorting').addEventListener('change', function () {
//     console.log('The sorting option has been changed');
//     handleFilter(); // Call the common function to handle filter changes
// });



// document.getElementById('max_price').addEventListener('blur', function () {
//     let min_price = parseFloat(this.min);
//     let max_price = parseFloat(this.max);
//     let current_price = parseFloat(this.value);

//     if (current_price < min_price || current_price > max_price) {
//         console.log('error occurred');
//         min_price = Math.round(min_price * 100) / 100;
//         max_price = Math.round(max_price * 100) / 100;

//         alert('Price must be between ' + min_price + ' and ' + max_price);
//         this.value = min_price;
//         document.getElementById('range').value = min_price;
//         this.focus();
//     }
// });

function handleFilter() {
    console.log('A checkbox has been clicked');

    let filter_object = {};
    let sorting = document.getElementById('sorting').value;
    let min_price = document.getElementById('range').min;
    let max_price = document.getElementById('range').value;

    filter_object.min_price = min_price;
    filter_object.max_price = max_price;

    // Check if any category or tag is selected
    let isCategorySelected = false;
    let isTagSelected = false;

    document.querySelectorAll('.filter-checkbox').forEach(function (checkbox) {
        let filter_value = checkbox.value;
        let filter_key = checkbox.dataset.filter;

        filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function (element) {
            return element.value;
        });

        if (filter_key === 'category' && filter_object[filter_key].length > 0) {
            isCategorySelected = true;
        } else if (filter_key === 'tag' && filter_object[filter_key].length > 0) {
            isTagSelected = true;
        }
    });

    // If no category is selected, use default values
    if (!isCategorySelected) {
        let defaultCategories = Array.from(document.querySelectorAll('.default-checkbox[data-filter="default-category"]'));
        let defaultCategoryValues = defaultCategories.map(function (defaultCategory) {
            return defaultCategory.value;
        })
        filter_object['category'] = defaultCategoryValues;
    }

    // If no tag is selected, use default values
    if (!isTagSelected) {
        let defaultTags = Array.from(document.querySelectorAll('.default-checkbox[data-filter="default-tag"]'));
        let defaultTagValues = defaultTags.map(function (defaultTag) {
            return defaultTag.value;
        })
        filter_object['tag'] = defaultTagValues;
    }

    console.log('Filter object is: ', filter_object);

    // Construct URL with query parameters
    let url = '/filter-products/?';

    url += 'sorting=' + sorting + '&';
    // Append min_price and max_price to the URL if they are present
    if (min_price !== undefined && max_price !== undefined) {
        url += 'min_price=' + min_price + '&';
        url += 'max_price=' + max_price + '&';
    }

    if (searchValue){
        url += 'search=' + searchValue + '&';
        console.log("Search value:", searchValue);
    }

    // Append other filter parameters to the URL
    for (let key in filter_object) {
        if (Array.isArray(filter_object[key]) && filter_object[key].length > 0) {
            url += key + '=' + filter_object[key] + '&';
        }
    }

    // Remove trailing '&' if present
    url = url.replace(/&$/, '');

    fetch(url)
    .then(function (response) {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(function (data) {
        
        console.log(data);
        console.log('Data filtered successfully...');
        document.getElementById('filtered-product').innerHTML = data.data;
        
        var productCountHTML;
        if (data.count == 1) {
            productCountHTML = `We've got <span class="productparaspan">${data.count}</span> product for you!`;
        } else {
            productCountHTML = `We've got <span class="productparaspan">${data.count}</span> products for you!`;
        }

        // Set the innerHTML of both elements
        document.querySelector('.heading-banner-content>p').innerHTML = productCountHTML;
        document.querySelector('.operation-options-2>p').innerHTML = productCountHTML;

        initializeAdd()
        initializeRatings()
        
    })
    .catch(function (error) {
        console.error('There was a problem with the fetch operation:', error);
    });
}

// Attach event listeners
document.querySelectorAll('.filter-checkbox, #price-filter-btn').forEach(function (element) {
    element.addEventListener('click', function () {
        handleFilter();
    });
});

sorting_ele = document.getElementById('sorting');
if (sorting_ele){
    document.getElementById('sorting').addEventListener('change', function () {
        console.log('The sorting option has been changed');
        handleFilter(); // Call the common function to handle filter changes
    });
}

max_price_ele = document.getElementById('max_price');
if (max_price_ele){
max_price_ele.addEventListener('blur', function () {
    let min_price = parseFloat(this.min);
    let max_price = parseFloat(this.max);
    let current_price = parseFloat(this.value);

    if (current_price < min_price || current_price > max_price) {
        console.log('error occurred');
        min_price = Math.round(min_price * 100) / 100;
        max_price = Math.round(max_price * 100) / 100;

        alert('Price must be between ' + min_price + ' and ' + max_price);
        this.value = min_price;
        document.getElementById('range').value = min_price;
        this.focus();
    }
});
}




function initializeRatings(){ 
    var ratingElements = document.querySelectorAll(".rating");
    ratingElements.forEach((ratingElement) => {
        var ratingValue = parseFloat(ratingElement.querySelector(".rating-value").innerText);
        var truncValue = Math.trunc(ratingValue);
        var stars = ratingElement.querySelectorAll("i");

        for (let i = 0; i < truncValue; i++) {
            stars[i].classList.remove("fa-regular");
            stars[i].classList.add("fa-solid");
        }

        if (ratingValue !== truncValue) {
            stars[truncValue].classList.remove("fa-regular");
            stars[truncValue].classList.add("fa-solid");
            stars[truncValue].classList.remove("fa-star");
            stars[truncValue].classList.add("fa-star-half-stroke");
        }

    });

}

initializeRatings()

// // Get the filter button
// var filterBtn = document.getElementById("filter-btn");

// // Get the nav-lower section
// var navLower = document.getElementById("nav-lower");

// // Add click event listener to the filter button
// filterBtn.addEventListener("click", function() {
//     // Toggle the visibility of nav-lower by adding or removing the 'hidden' class
//     navLower.classList.toggle("hidden");
// });

// Get the filter button
var filterBtn = document.getElementById("filter-btn");

// Get the nav-lower section
var navLower = document.getElementById("nav-lower");

// Get the chevron icon
var chevronIcon = document.querySelector("#filter-btn i.fa-solid.fa-chevron-down");

if (filterBtn){
    // Add click event listener to the filter button
filterBtn.addEventListener("click", function() {
    // Toggle the visibility of nav-lower by adding or removing the 'hidden' class
    navLower.classList.toggle("hidden");
    
    // Check if nav-lower is visible
    var isNavLowerVisible = !navLower.classList.contains("hidden");
    
    // Change the chevron icon based on visibility
    if (isNavLowerVisible) {
        // If nav-lower is visible, change the chevron to up
        chevronIcon.classList.remove("fa-chevron-down");
        chevronIcon.classList.add("fa-chevron-up");
    } else {
        // If nav-lower is hidden, change the chevron to down
        chevronIcon.classList.remove("fa-chevron-up");
        chevronIcon.classList.add("fa-chevron-down");
    }
});

}