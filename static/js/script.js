
// Function to add product
// Function to validate the login form
function validateLoginForm() {
    const email = document.forms["loginForm"]["email"].value;
    const password = document.forms["loginForm"]["password"].value;

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !password) {
        alert("Both email and password must be filled out.");
        return false;
    }
    if (password.length < 6) {
        alert("Password must be at least 6 characters long.");
        return false;
    }
    return true;
}

// Function to validate the signup form
function validateSignupForm() {
    const email = document.forms["signupForm"]["email"].value;
    const password = document.forms["signupForm"]["password"].value;

    if (!email || !password) {
        alert("Both email and password must be filled out.");
        return false;
    }
    return true;
}

// Function to confirm adding to cart
function confirmAddToCart(productName) {
    return confirm(`Are you sure you want to add ${productName} to your cart?`);
}

// Function to add product to localStorage
function addProduct() {
    const name = document.getElementById("productName").value;
    const description = document.getElementById("productDescription").value;
    const price = document.getElementById("productPrice").value;
    const timePeriod = document.getElementById("productDetails").value;
    const image = document.getElementById("productImage").files[0];

    const product = {
        name,
        description,
        price,
        timePeriod,
        imageURL: image ? URL.createObjectURL(image) : ''
    };

    let products = JSON.parse(localStorage.getItem("products")) || [];
    products.push(product);
    localStorage.setItem("products", JSON.stringify(products));

    displayProduct(product); // Display the new product
    document.getElementById("productForm").reset(); // Reset the form
}

// Function to display product on home and seller page
function displayProduct(product) {
    const productItem = document.createElement("div");
    productItem.classList.add("product-item");
    productItem.innerHTML = `
        <h3>${product.name}</h3>
        <p>${product.description}</p>
        <p>Price: ${product.price}</p>
        <p>Time Period: ${product.timePeriod}</p>
        <img src="${product.imageURL}" alt="${product.name}">
        <button onclick="addToCart('${product.name}')">Add to Cart</button>
    `;
    document.getElementById("productListHome").appendChild(productItem);
    document.getElementById("productListSeller").appendChild(productItem.cloneNode(true)); // Clone item for seller page
}

// Function to load products from localStorage
function loadProducts() {
    const products = JSON.parse(localStorage.getItem("products")) || [];
    document.getElementById("productListHome").innerHTML = ''; // Clear existing content
    document.getElementById("productListSeller").innerHTML = '';

    products.forEach((product) => {
        displayProduct(product); // Display products on home and seller page
    });
}

// Function to add to cart
function addToCart(productName) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    cart.push(productName);
    localStorage.setItem("cart", JSON.stringify(cart));
    alert(`${productName} has been added to your cart!`);
}

// Function to delete product
function deleteProduct(index) {
    let products = JSON.parse(localStorage.getItem("products")) || [];
    products.splice(index, 1);
    localStorage.setItem("products", JSON.stringify(products));
    loadProducts(); // Reload products to update the display
}

// Theme toggle functionality
function toggleTheme() {
    const body = document.body;
    const toggle = document.getElementById('theme-toggle');
    const status = document.getElementById('theme-status');

    if (toggle.checked) {
        body.classList.add('dark-mode');
        status.textContent = 'Dark Theme';
        localStorage.setItem('theme', 'dark');
    } else {
        body.classList.remove('dark-mode');
        status.textContent = 'Light Theme';
        localStorage.setItem('theme', 'light');
    }
}

// Load saved theme on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.getElementById('theme-toggle').checked = true;
        document.body.classList.add('dark-mode');
        document.getElementById('theme-status').textContent = 'Dark Theme';
    } else {
        document.getElementById('theme-toggle').checked = false;
        document.body.classList.remove('dark-mode');
        document.getElementById('theme-status').textContent = 'Light Theme';
    }

    loadProducts(); // Call function to load products when page loads
});











// script.js
function sendMessage() {
    var input = document.getElementById('user-input');
    var chatBox = document.getElementById('chat-box');

    if(input.value.trim()) {
        // Add user message
        chatBox.innerHTML += "<div>User: " + input.value + "</div>";

        // Simulate chatbot response
        setTimeout(function() {
            chatBox.innerHTML += "<div>Bot: " + "I am a bot! How can I help?" + "</div>";
            chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
        }, 1000);
    }

    input.value = ''; // Clear input field
}










function validateLoginForm() {
    const email = document.forms["loginForm"]["email"].value;
    const password = document.forms["loginForm"]["password"].value;

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !password) {
        alert("Both email and password must be filled out.");
        return false;
    }
    if (password.length < 6) {
        alert("Password must be at least 6 characters long.");
        return false;
    }
    return true;
}

// Function to validate the signup form
function validateSignupForm() {
    const email = document.forms["signupForm"]["email"].value;
    const password = document.forms["signupForm"]["password"].value;

    if (!email || !password) {
        alert("Both email and password must be filled out.");
        return false;
    }
    return true;
}

// Function to confirm adding to cart
function confirmAddToCart(productName) {
    return confirm(`Are you sure you want to add ${productName} to your cart?`);
}

function addProduct() {
    // Get form values
    const name = document.getElementById("productName").value;
    const description = document.getElementById("productDescription").value;
    const price = document.getElementById("productPrice").value;
    const timePeriod = document.getElementById("productDetails").value; // Ensure correct id
    const image = document.getElementById("productImage").files[0];

    // Create product object
    const product = {
        name,
        description,
        price,
        timePeriod, // Make sure to use the correct variable name
        imageURL: image ? URL.createObjectURL(image) : ''
    };

    // Save to localStorage
    let products = JSON.parse(localStorage.getItem("products")) || [];
    products.push(product);
    localStorage.setItem("products", JSON.stringify(products));

    // Add product to list below the form
    displayProduct(product);

    // Clear form
    document.getElementById("productForm").reset();
}

// Function to display products on home page
function loadProducts() {
    const products = JSON.parse(localStorage.getItem("products")) || [];
    const productListHome = document.getElementById("productListHome");
    productListHome.innerHTML = ''; // Clear existing content

    products.forEach((product, index) => {
        const productItem = document.createElement("div");
        productItem.classList.add("product-item");
        productItem.innerHTML = `
            <h3>${product.name}</h3>
            <p>${product.description}</p>
            <p>Price: ${product.price}</p>
            <p>Time Period: ${product.timePeriod}</p>
            <img src="${product.imageURL}" alt="${product.name}">
            <button onclick="deleteProduct(${index})">Delete</button>
        `;
        productListHome.appendChild(productItem);
    });
}

// Function to delete a product
function deleteProduct(index) {
    let products = JSON.parse(localStorage.getItem("products")) || [];
    products.splice(index, 1); // Remove the product at the specified index
    localStorage.setItem("products", JSON.stringify(products)); // Update local storage
    loadProducts(); // Reload the products to update the display
}

// Load products when the page loads
window.onload = function() {
    loadProducts(); // Call function to load products
};

function displayProduct(product) {
    const productList = document.getElementById("productList");
    const productItem = document.createElement("div");
    productItem.classList.add("product-item");
    productItem.innerHTML = `
        <h3>${product.name}</h3>
        <p>${product.description}</p>
        <p>Price: $${product.price}</p>
        <p>Time Period: ${product.timePeriod}</p>
        <img src="${product.imageURL}" alt="${product.name}">
        <button class="add-to-cart" onclick="addToCart('${product.name}')">Add to Cart</button>
        <button class="delete-product" onclick="deleteProduct('${product.name}')">Delete Product</button>
    `;
    productList.appendChild(productItem);
}

function addToCart(productName) {
    // Logic to add the product to cart
    alert(`${productName} has been added to your cart!`);
}

function deleteProduct(productName) {
    // Logic to delete the product from the local storage and refresh the display
    let products = JSON.parse(localStorage.getItem("products")) || [];
    products = products.filter(product => product.name !== productName);
    localStorage.setItem("products", JSON.stringify(products));
    location.reload(); // Refresh the page to show updated product list
}

function deleteProduct(identifier) {
    let products = JSON.parse(localStorage.getItem("products")) || [];
    if (typeof identifier === 'number') {
        products.splice(identifier, 1);
    } else {
        products = products.filter(product => product.name !== identifier);
    }
    localStorage.setItem("products", JSON.stringify(products));
    loadProducts();
}

function addToCart(productName) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    cart.push(productName);
    localStorage.setItem("cart", JSON.stringify(cart));
    alert(`${productName} has been added to your cart!`);
}

document.getElementById("productImage").addEventListener("change", function(event) {
    const imageFile = event.target.files[0];
    const preview = document.createElement("img");
    preview.src = URL.createObjectURL(imageFile);
    preview.style.maxWidth = "100px";  // Set preview size
    const imagePreviewDiv = document.getElementById("imagePreview");
    imagePreviewDiv.innerHTML = "";  // Clear previous preview
    imagePreviewDiv.appendChild(preview);
});

document.getElementById("productForm").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent the default form submission
    addProduct();  // Call the addProduct function
});


// Load products on page load
window.onload = loadProducts;


function setTheme(theme) {
    // Set the selected theme in the session using a form submission
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/set_language';  // Change this to your theme setting endpoint

    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'theme';
    input.value = theme;

    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}






function toggleTheme() {
    const body = document.body;
    const toggle = document.getElementById('theme-toggle');
    const status = document.getElementById('theme-status');

    if (toggle.checked) {
        body.classList.add('dark-mode');
        status.textContent = 'Dark Theme';
        // Store theme preference in session or localStorage
        sessionStorage.setItem('theme', 'dark');
    } else {
        body.classList.remove('dark-mode');
        status.textContent = 'Light Theme';
        sessionStorage.setItem('theme', 'light');
    }
}

// Load the saved theme on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = sessionStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.getElementById('theme-toggle').checked = true;
        document.body.classList.add('dark-mode');
        document.getElementById('theme-status').textContent = 'Dark Theme';
    } else {
        document.getElementById('theme-toggle').checked = false;
        document.body.classList.remove('dark-mode');
        document.getElementById('theme-status').textContent = 'Light Theme';
    }
});









document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("theme-toggle");

    // Load saved theme from localStorage
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
        toggle.checked = true; // Check the toggle
    }

    // Add event listener for theme toggle
    toggle.addEventListener("change", () => {
        document.body.classList.toggle("dark-mode");
        
        // Save the theme choice in localStorage
        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.setItem("theme", "light");
        }
    });
});








document.getElementById("productImage").addEventListener("change", function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement("img");
            img.src = e.target.result;
            img.className = "image-preview";
            document.getElementById("imagePreview").innerHTML = "";
            document.getElementById("imagePreview").appendChild(img);
        };
        reader.readAsDataURL(file);
    }
});






document.getElementById("productForm").addEventListener("submit", function(e) {
    e.preventDefault();
    const submitButton = document.querySelector("button[type='submit']");
    submitButton.innerHTML = "Adding...";
    submitButton.disabled = true;
    // Simulate submission delay
    setTimeout(() => {
        submitButton.innerHTML = "Add Product!";
        submitButton.disabled = false;
        alert("Product added successfully!");
    }, 1000);
});




function addProduct() {
    // ... [existing code]
    document.getElementById("feedback").innerText = `${product.name} has been added!`;
    document.getElementById("feedback").style.color = "green";
}





// Add Product to Server
function addProduct() {
    const name = document.getElementById("productName").value;
    const description = document.getElementById("productDescription").value;
    const price = document.getElementById("productPrice").value;
    const timePeriod = document.getElementById("productTimePeriod").value;
    const image = document.getElementById("productImage").files[0];

    const formData = new FormData();
    formData.append('name', name);
    formData.append('description', description);
    formData.append('price', price);
    formData.append('timePeriod', timePeriod);
    formData.append('image', image);

    fetch('/add-product', {  // Adjust the URL to your Flask route
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Handle success
        displayProduct(data.product);
        alert(`${data.product.name} has been added!`);
    })
    .catch(error => {
        // Handle error
        console.error('Error:', error);
        alert('There was an error adding the product.');
    });
}
