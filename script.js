// --- STATE MANAGEMENT ---
let catalog = [];
let wishlist = JSON.parse(localStorage.getItem('cartItWishlist')) || [];

// --- FETCH DATA FROM BACKEND ---
async function fetchProducts() {
    try {
        const response = await fetch('http://15.207.71.36:5000/api/products');
        catalog = await response.json();
        
        renderProducts(catalog);
        updateWishlistUI();
    } catch (error) {
        console.error("Error fetching products:", error);
        document.getElementById('product-list').innerHTML = "<p>Failed to load products from server.</p>";
    }
}

// --- WISHLIST LOGIC ---
function toggleWishlist(productName) {
    const index = wishlist.findIndex(item => item.name === productName);
    
    if (index > -1) {
        wishlist.splice(index, 1);
    } else {
        const product = catalog.find(item => item.name === productName);
        if (product) wishlist.push(product);
    }
    
    localStorage.setItem('cartItWishlist', JSON.stringify(wishlist));
    updateWishlistUI();
    reRenderCurrentCategory();
}

function updateWishlistUI() {
    document.getElementById('wishlist-trigger').innerText = `WISHLIST (${wishlist.length})`;
    const wishlistContainer = document.getElementById('wishlist-content');
    wishlistContainer.innerHTML = "";
    
    if (wishlist.length === 0) {
        wishlistContainer.innerHTML = "<p>Your wishlist is currently empty.</p>";
        return;
    }

    wishlist.forEach(item => {
        const itemHTML = `
            <div class="wishlist-item">
                <img src="${item.image_url || item.image}" alt="${item.name}">
                <div class="wishlist-item-info">
                    <h4>${item.name}</h4>
                    <p>${item.price}</p>
                    <button class="remove-wishlist" onclick="toggleWishlist('${item.name}')">Remove</button>
                </div>
            </div>
        `;
        wishlistContainer.innerHTML += itemHTML;
    });
}

// --- RENDERING LOGIC ---
const productContainer = document.getElementById('product-list');

function renderProducts(itemsToRender) {
    productContainer.innerHTML = ""; 
    
    itemsToRender.forEach((product, index) => {
        const isSaved = wishlist.some(item => item.name === product.name);
        const heartClass = isSaved ? "wishlist-icon active" : "wishlist-icon";
        const heartSymbol = isSaved ? "♥" : "♡";
        const animationDelay = (index * 0.05) + 's'; 
        
        const imageUrl = product.image_url || product.image;
        
        const cardHTML = `
            <div class="card" style="animation-delay: ${animationDelay};">
                <div class="image-placeholder" style="background: url('${imageUrl}') center/cover no-repeat;">
                    <button class="${heartClass}" onclick="toggleWishlist('${product.name}')">${heartSymbol}</button>
                </div>
                <h3>${product.name}</h3>
                <p class="price">${product.price}</p>
               <button class="add-btn" onclick="addToCart('${product.name}')">Add to Bag</button>
            </div>
        `;
        productContainer.innerHTML += cardHTML;
    });
}

function reRenderCurrentCategory() {
    const activeBtn = document.querySelector('.filter-btn.active');
    if (!activeBtn) return;
    
    const selectedCategory = activeBtn.getAttribute('data-category');
    if (selectedCategory === "All") {
        renderProducts(catalog);
    } else {
        renderProducts(catalog.filter(item => item.category === selectedCategory));
    }
}

// --- FILTER BUTTON LISTENERS ---
const filterButtons = document.querySelectorAll('.filter-btn');
filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        filterButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        reRenderCurrentCategory();
    });
});

// --- SIDEBAR TOGGLE LOGIC ---
const sidebar = document.getElementById('wishlist-sidebar');
const overlay = document.getElementById('overlay');
const trigger = document.getElementById('wishlist-trigger');
const closeBtn = document.getElementById('close-wishlist');

function openSidebar() {
    sidebar.classList.add('open');
    overlay.classList.add('open');
}

function closeSidebar() {
    sidebar.classList.remove('open');
    overlay.classList.remove('open');
}

if(trigger) trigger.addEventListener('click', openSidebar);
if(closeBtn) closeBtn.addEventListener('click', closeSidebar);
if(overlay) overlay.addEventListener('click', closeSidebar);


// --- MODAL UI LOGIC ---
function openAuthModal() { document.getElementById('auth-modal').classList.add('open'); }
function closeAuthModal() { document.getElementById('auth-modal').classList.remove('open'); }

function switchAuthTab(tab) {
    document.getElementById('tab-login').classList.remove('active-tab');
    document.getElementById('tab-register').classList.remove('active-tab');
    document.getElementById('form-login').classList.remove('active-form');
    document.getElementById('form-register').classList.remove('active-form');

    document.getElementById(`tab-${tab}`).classList.add('active-tab');
    document.getElementById(`form-${tab}`).classList.add('active-form');
    document.getElementById('auth-message').innerText = "";
}

// --- AUTH API LOGIC ---
const API_BASE = "http://15.207.71.36:5000"; 

async function registerUser() {
    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;

    const response = await fetch(`${API_BASE}/api/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
    });
    const data = await response.json();
    
    const msgEl = document.getElementById('auth-message');
    msgEl.innerText = data.message || data.error;
    msgEl.style.color = response.ok ? "green" : "red";
    
    if (response.ok) setTimeout(() => switchAuthTab('login'), 1500);
}

async function loginUser() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    const response = await fetch(`${API_BASE}/api/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    const data = await response.json();

    const msgEl = document.getElementById('auth-message');
    if (response.ok) {
        localStorage.setItem('cartItUser', JSON.stringify(data.user));
        updateNavForUser(data.user.username);
        closeAuthModal();
        fetchCart(); 
    } else {
        msgEl.style.color = "red";
        msgEl.innerText = data.error;
    }
}

function updateNavForUser(username) {
    const trigger = document.getElementById('auth-trigger');
    const ordersTrigger = document.getElementById('orders-trigger');
    
    if (trigger) {
        trigger.innerText = `HI, ${username.toUpperCase()}`;
        trigger.onclick = null; 
    }
    if (ordersTrigger) {
        ordersTrigger.style.display = 'inline';
    }
}

// Initialization on load
const savedUser = JSON.parse(localStorage.getItem('cartItUser'));
if (savedUser) {
    updateNavForUser(savedUser.username);
}

// --- CART LOGIC ---
async function addToCart(productName) {
    const savedUser = JSON.parse(localStorage.getItem('cartItUser'));
    
    if (!savedUser) {
        alert("Please login first to add items to your bag!");
        openAuthModal();
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/cart/add`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: savedUser.id,
                product_name: productName
            })
        });
        const data = await response.json();
        
        if (response.ok) {
            alert("Added to bag successfully!");
            fetchCart(); 
        } else {
            alert(data.error);
        }
    } catch (error) {
        console.error("Error adding to cart:", error);
    }
}

// --- ADVANCED FETCH & RENDER CART ---
async function fetchCart() {
    const savedUser = JSON.parse(localStorage.getItem('cartItUser'));
    if (!savedUser) return;

    try {
        const response = await fetch(`${API_BASE}/api/cart/${savedUser.id}`);
        const cartItems = await response.json();
        
        const bagTrigger = document.getElementById('bag-trigger');
        const bagContent = document.getElementById('bag-content');
        const checkoutSection = document.getElementById('checkout-section');
        const totalPriceEl = document.getElementById('bag-total-price');
        
        let totalItems = 0;
        let totalPrice = 0;

        bagContent.innerHTML = "";
        
        if (cartItems.length === 0) {
            if (bagTrigger) bagTrigger.innerText = `BAG (0)`;
            bagContent.innerHTML = "<p>Your bag is currently empty.</p>";
            if (checkoutSection) checkoutSection.style.display = "none";
            return;
        }

        cartItems.forEach(item => {
            totalItems += item.quantity;
            const rawPrice = parseInt(item.price.replace(/[^0-9]/g, ''));
            totalPrice += (rawPrice * item.quantity);

            bagContent.innerHTML += `
                <div class="wishlist-item" style="margin-bottom: 1rem;">
                    <img src="${item.image_url}" alt="${item.name}">
                    <div class="wishlist-item-info" style="width: 100%;">
                        <h4>${item.name}</h4>
                        <p>${item.price}</p>
                        <div style="display: flex; align-items: center; gap: 10px; margin-top: 5px;">
                            <button onclick="updateQty(${item.cart_id}, ${item.quantity - 1})" style="padding: 2px 8px; cursor: pointer; border: 1px solid #ccc; background: #fff;">-</button>
                            <span style="font-size: 0.85rem; font-weight: bold;">${item.quantity}</span>
                            <button onclick="updateQty(${item.cart_id}, ${item.quantity + 1})" style="padding: 2px 8px; cursor: pointer; border: 1px solid #ccc; background: #fff;">+</button>
                        </div>
                    </div>
                </div>
            `;
        });

        if (bagTrigger) bagTrigger.innerText = `BAG (${totalItems})`;
        if (totalPriceEl) totalPriceEl.innerText = "₹" + totalPrice.toLocaleString('en-IN');
        if (checkoutSection) checkoutSection.style.display = "block";

    } catch (error) {
        console.error("Error fetching cart:", error);
    }
}

async function updateQty(cartId, newQty) {
    if (newQty > 10) {
        alert("You can only order a maximum of 10 units per item.");
        return;
    }
    try {
        await fetch(`${API_BASE}/api/cart/update`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cart_id: cartId, quantity: newQty })
        });
        fetchCart(); 
    } catch (error) {
        console.error("Error updating qty:", error);
    }
}

// --- ORDERS API LOGIC ---
async function placeOrder() {
    const savedUser = JSON.parse(localStorage.getItem('cartItUser'));
    const name = document.getElementById('del-name').value;
    const phone = document.getElementById('del-phone').value;
    const address = document.getElementById('del-address').value;
    const payment = document.querySelector('input[name="payment"]:checked').value;

    if (!name || !phone || !address) {
        alert("Please fill in all delivery details!");
        return;
    }

    const totalPrice = document.getElementById('bag-total-price').innerText;
    const bagItems = document.querySelectorAll('#bag-content h4');
    let itemsSummary = Array.from(bagItems).map(item => item.innerText).join(", ");

    try {
        const response = await fetch(`${API_BASE}/api/orders/place`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: savedUser.id,
                items_summary: itemsSummary,
                total_price: totalPrice,
                payment_method: payment,
                delivery_details: `${name}, ${phone}, ${address}`
            })
        });
        
        const data = await response.json(); 

        if (response.ok) {
            alert(`Order placed successfully!\nTrack it in the ORDERS tab.`);
            document.getElementById('del-name').value = '';
            document.getElementById('del-phone').value = '';
            document.getElementById('del-address').value = '';
            closeBag();
            fetchCart(); 
        } else {
            alert("Backend Error: " + data.error); 
        }
    } catch (error) {
        console.error("Error placing order:", error);
    }
}

function openOrdersModal() {
    document.getElementById('orders-modal').classList.add('open');
    fetchOrders();
}

function closeOrdersModal() {
    document.getElementById('orders-modal').classList.remove('open');
}

async function fetchOrders() {
    const savedUser = JSON.parse(localStorage.getItem('cartItUser'));
    const content = document.getElementById('orders-content');
    if (!savedUser) return;

    try {
        const response = await fetch(`${API_BASE}/api/orders/${savedUser.id}`);
        const data = await response.json();
        
        if (!response.ok) {
            content.innerHTML = `<p style='text-align:center; color:red;'>Database Error: ${data.error}</p>`;
            return;
        }
        
        content.innerHTML = "";
        if (data.length === 0) {
            content.innerHTML = "<p style='text-align:center;'>You haven't placed any orders yet.</p>";
            return;
        }

        data.forEach(order => {
            const date = new Date(order.created_at).toLocaleDateString('en-IN');
            content.innerHTML += `
                <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 4px;">
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #eee; padding-bottom: 8px; margin-bottom: 8px;">
                        <span style="font-weight: bold; font-size: 0.85rem;">Order #${order.id}</span>
                        <span style="font-size: 0.85rem; color: #555;">${date}</span>
                    </div>
                    <p style="font-size: 0.85rem; color: #333; margin-bottom: 8px;"><strong>Items:</strong> ${order.items_summary}</p>
                    <p style="font-size: 0.85rem; margin-bottom: 8px;"><strong>Total:</strong> ${order.total_price} | <strong>Via:</strong> ${order.payment_method}</p>
                    <p style="font-size: 0.85rem; font-weight: bold; color: #d00000;">Status: ${order.status}</p>
                </div>
            `;
        });
    } catch (error) {
        console.error("Error fetching orders:", error);
    }
}

// Call fetchCart when user logs in or page loads
if (savedUser) {
    fetchCart();
}

// --- BAG SIDEBAR UI LOGIC ---
const bagSidebar = document.getElementById('bag-sidebar');
const bagTrigger = document.getElementById('bag-trigger');
const closeBagBtn = document.getElementById('close-bag');

function openBag() {
    if (bagSidebar) bagSidebar.classList.add('open');
    if (overlay) overlay.classList.add('open');
}
function closeBag() {
    if (bagSidebar) bagSidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
}

if(bagTrigger) bagTrigger.addEventListener('click', openBag);
if(closeBagBtn) closeBagBtn.addEventListener('click', closeBag);

// Call the fetch function to load products
fetchProducts();