// API Endpoints
const API_BASE = '/api';

// Cart State
let cart = [];
let currentCategory = 'الكل';
let allProducts = [];

// Initialize
document.addEventListener('DOMContentLoaded', function () {
    loadAds();
    loadOffers();
    loadCategories();
    loadProducts();
    
    // Create Toast Container
    createToastContainer();
});

// --- API Calls ---

async function fetchProducts(category = null) {
    let url = `${API_BASE}/products`;
    if (category && category !== 'الكل') {
        url += `?category=${encodeURIComponent(category)}`;
    }
    const response = await fetch(url);
    return await response.json();
}

async function fetchCategories() {
    const response = await fetch(`${API_BASE}/categories`);
    return await response.json();
}

async function fetchAds() {
    const response = await fetch(`${API_BASE}/ads`);
    return await response.json();
}

async function fetchOffers() {
    const response = await fetch(`${API_BASE}/offers`);
    return await response.json();
}

// --- UI Functions ---

async function loadProducts() {
    try {
        allProducts = await fetchProducts();
        displayProducts(allProducts);
    } catch (error) {
        console.error('Error loading products:', error);
        showToast('حدث خطأ أثناء تحميل المنتجات', 'error');
    }
}

async function loadCategories() {
    try {
        const categories = await fetchCategories();
        const categoriesGrid = document.querySelector('.categories-grid');

        if (!categoriesGrid) return;

        categoriesGrid.innerHTML = `
            <button class="category-btn active" onclick="filterProducts('الكل')">الكل</button>
            ${categories.map(cat =>
            `<button class="category-btn" onclick="filterProducts('${cat.name}')">${cat.icon || ''} ${cat.name}</button>`
        ).join('')}
        `;
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

async function loadAds() {
    try {
        const ads = await fetchAds();
        const adsSlider = document.getElementById('adsSlider');

        if (!adsSlider) return;

        if (ads.length === 0) {
            adsSlider.innerHTML = '<p style="text-align: center; color: #64748b;">لا توجد إعلانات حالياً</p>';
            return;
        }

        adsSlider.innerHTML = ads.map(ad => {
            let imageDisplay = '';
            if (ad.icon) {
                if (ad.icon.startsWith('http') || ad.icon.startsWith('data:image') || ad.icon.startsWith('logo.')) {
                    imageDisplay = `<img src="${ad.icon}" alt="${ad.title}" onerror="this.outerHTML='<span style=\\'font-size: 8rem;\\'>🎉</span>'">`;
                } else {
                    imageDisplay = ad.icon;
                }
            } else {
                imageDisplay = '🎉';
            }

            return `
                <div class="ad-card glass-card">
                    <div class="ad-icon">${imageDisplay}</div>
                    <h3>${ad.title}</h3>
                    <p>${ad.description}</p>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading ads:', error);
    }
}

async function loadOffers() {
    try {
        const offers = await fetchOffers();
        const offersGrid = document.getElementById('offersGrid');

        if (!offersGrid) return;

        if (offers.length === 0) {
            offersGrid.innerHTML = '<p style="text-align: center; color: #64748b;">لا توجد عروض حالياً</p>';
            return;
        }

        offersGrid.innerHTML = offers.map(offer => {
            let imageDisplay = '';
            if (offer.icon) {
                if (offer.icon.startsWith('http') || offer.icon.startsWith('data:image') || offer.icon.startsWith('logo.')) {
                    imageDisplay = `<img src="${offer.icon}" alt="${offer.title}" onerror="this.outerHTML='<span style=\\'font-size: 6rem;\\'>🎁</span>'">`;
                } else {
                    imageDisplay = offer.icon;
                }
            } else {
                imageDisplay = '🎁';
            }

            return `
                <div class="offer-card glass-card" style="background: linear-gradient(135deg, #a78bfa 0%, #ec4899 100%); color: white;">
                    <div class="offer-icon">${imageDisplay}</div>
                    <h3>${offer.title}</h3>
                    <p>${offer.discount}</p>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading offers:', error);
    }
}

function displayProducts(productsToShow) {
    const grid = document.getElementById('productsGrid');
    grid.innerHTML = '';

    if (productsToShow.length === 0) {
        grid.innerHTML = '<p style="text-align: center; grid-column: 1/-1; padding: 2rem; color: var(--text-light);">لا توجد منتجات في هذا القسم</p>';
        return;
    }

    productsToShow.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card glass-card';

        let imageDisplay = '';
        if (product.image) {
            if (product.image.startsWith('http') || product.image.startsWith('data:image') || product.image.startsWith('logo.')) {
                imageDisplay = `<img src="${product.image}" alt="${product.name}" onerror="this.outerHTML='<span style=\\'font-size: 4rem;\\'>📚</span>'">`;
            } else {
                imageDisplay = `<span style="font-size: 4rem;">${product.image}</span>`;
            }
        } else {
            imageDisplay = '<span style="font-size: 4rem;">📚</span>';
        }

        card.innerHTML = `
            <div class="product-image">${imageDisplay}</div>
            <div class="product-info">
                <h3 class="product-name">${product.name}</h3>
                <div class="product-footer">
                    <span class="product-price">${product.price} ريال</span>
                    <button class="add-to-cart-btn" onclick="addToCart(${product.id})">🛒</button>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

async function filterProducts(category) {
    currentCategory = category;

    // Update active button
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.textContent.includes(category)) {
            btn.classList.add('active');
        }
    });

    // Fetch filtered products
    try {
        const products = await fetchProducts(category);
        displayProducts(products);

        const title = category === 'الكل' ? 'جميع المنتجات' : `منتجات ${category}`;
        document.getElementById('productsTitle').textContent = title;
    } catch (error) {
        console.error('Error filtering products:', error);
        showToast('حدث خطأ أثناء تصفية المنتجات', 'error');
    }
}

// --- Cart Functions ---

function addToCart(productId) {
    const product = allProducts.find(p => p.id === productId);
    if (!product) return;

    const existingItem = cart.find(item => item.id === productId);

    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({ ...product, quantity: 1 });
    }

    updateCart();
    showToast(`تم إضافة "${product.name}" إلى السلة`);
}

function updateCart() {
    const cartItems = document.getElementById('cartItems');
    const cartBadge = document.getElementById('cartBadge');
    const cartFooter = document.getElementById('cartFooter');
    const cartTotal = document.getElementById('cartTotal');

    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    if (totalItems > 0) {
        cartBadge.style.display = 'flex';
        cartBadge.textContent = totalItems;
        
        // Animate badge
        cartBadge.style.animation = 'none';
        cartBadge.offsetHeight; /* trigger reflow */
        cartBadge.style.animation = 'bounce 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
    } else {
        cartBadge.style.display = 'none';
    }

    if (cart.length === 0) {
        cartItems.innerHTML = `
            <div class="empty-cart">
                <div class="empty-cart-icon">🛒</div>
                <p>سلة المشتريات فارغة</p>
                <p style="font-size: 0.875rem; margin-top: 0.5rem;">أضف بعض المنتجات للبدء</p>
            </div>
        `;
        cartFooter.style.display = 'none';
    } else {
        cartItems.innerHTML = cart.map(item => `
            <div class="cart-item">
                <div class="cart-item-image">${item.image && (item.image.startsWith('http') || item.image.startsWith('data:')) ? `<img src="${item.image}" style="width:100%;height:100%;object-fit:contain;">` : (item.image || '📚')}</div>
                <div class="cart-item-info">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-price">${item.price} ريال</div>
                </div>
                <div class="cart-item-controls">
                    <button class="qty-btn" onclick="updateQuantity(${item.id}, ${item.quantity - 1})">−</button>
                    <span class="quantity">${item.quantity}</span>
                    <button class="qty-btn plus" onclick="updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                </div>
                <button class="remove-item-btn" onclick="removeFromCart(${item.id})">×</button>
            </div>
        `).join('');

        cartFooter.style.display = 'block';

        const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        cartTotal.textContent = `${total.toFixed(2)} ريال`;
    }
}

function updateQuantity(productId, newQuantity) {
    if (newQuantity <= 0) {
        removeFromCart(productId);
    } else {
        const item = cart.find(item => item.id === productId);
        if (item) {
            item.quantity = newQuantity;
            updateCart();
        }
    }
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    updateCart();
}

function toggleCart() {
    const modal = document.getElementById('cartModal');
    modal.classList.toggle('show');
}

function checkout() {
    if (cart.length === 0) {
        showToast('سلة المشتريات فارغة!', 'error');
        return;
    }

    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    alert(`شكراً لك! إجمالي المشتريات: ${total.toFixed(2)} ريال يمني\n\nسيتم التواصل معك قريباً لإتمام الطلب.`);

    cart = [];
    updateCart();
    toggleCart();
    showToast('تم إرسال الطلب بنجاح! 🎉');
}

document.getElementById('cartModal').addEventListener('click', function (e) {
    if (e.target === this) {
        toggleCart();
    }
});

// --- Toast Notifications ---

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
}

function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
        <span>${type === 'success' ? '✅' : '⚠️'}</span>
        <span>${message}</span>
    `;
    
    document.body.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 400);
    }, 3000);
}
