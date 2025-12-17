// API Endpoints
const API_BASE = '/api';

// Initialize admin panel
document.addEventListener('DOMContentLoaded', function () {
    // التحقق من تسجيل الدخول
    if (!checkAdminAuth()) {
        return;
    }

    // عرض اسم المدير
    displayAdminInfo();

    loadCategories();
    loadProducts();
    loadAds();
    loadOffers();
    // updateStats called within load functions
    populateCategoryDropdown();
});

// التحقق من تسجيل دخول المدير
function checkAdminAuth() {
    const localAuth = localStorage.getItem('adminAuth');
    const sessionAuth = sessionStorage.getItem('adminAuth');

    if (!localAuth && !sessionAuth) {
        window.location.href = 'admin-login'; // Flask route
        return false;
    }

    const authData = JSON.parse(localAuth || sessionAuth);
    if (!authData.isLoggedIn) {
        window.location.href = 'admin-login'; // Flask route
        return false;
    }

    return true;
}

// عرض معلومات المدير
function displayAdminInfo() {
    const localAuth = localStorage.getItem('adminAuth');
    const sessionAuth = sessionStorage.getItem('adminAuth');
    const authData = JSON.parse(localAuth || sessionAuth);

    const usernameElement = document.getElementById('adminUsername');
    if (usernameElement) {
        usernameElement.textContent = `مرحباً، ${authData.username}`;
    }
}

// تسجيل الخروج
function logout() {
    if (confirm('هل أنت متأكد من تسجيل الخروج؟')) {
        localStorage.removeItem('adminAuth');
        sessionStorage.removeItem('adminAuth');
        window.location.href = 'admin-login'; // Flask route
    }
}

// Show section
function showSection(section) {
    document.querySelectorAll('.content-section').forEach(sec => {
        sec.classList.remove('active');
    });

    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });

    event.target.classList.add('active');

    if (section === 'products') {
        document.getElementById('productsSection').classList.add('active');
        document.getElementById('sectionTitle').textContent = 'إدارة المنتجات';
    } else if (section === 'categories') {
        document.getElementById('categoriesSection').classList.add('active');
        document.getElementById('sectionTitle').textContent = 'إدارة الأقسام';
    } else if (section === 'ads') {
        document.getElementById('adsSection').classList.add('active');
        document.getElementById('sectionTitle').textContent = 'الإعلانات والعروض';
    } else if (section === 'orders') {
        document.getElementById('ordersSection').classList.add('active');
        document.getElementById('sectionTitle').textContent = 'الطلبات';
    }
}

// --- API Helpers ---

async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    if (data) {
        options.body = JSON.stringify(data);
    }
    const response = await fetch(`${API_BASE}${endpoint}`, options);
    if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
    }
    if (method !== 'DELETE') {
        return await response.json();
    }
}

// --- Products Management ---

async function loadProducts() {
    try {
        const products = await apiCall('/products');
        const tbody = document.getElementById('productsTableBody');
        tbody.innerHTML = '';

        products.forEach(product => {
            const row = document.createElement('tr');

            // Display image
            let imageDisplay = '';
            if (product.image) {
                if (product.image.startsWith('http') || product.image.startsWith('data:image') || product.image.startsWith('logo.')) {
                    imageDisplay = `<img src="${product.image}" style="width: 40px; height: 40px; object-fit: contain; border-radius: 5px;" onerror="this.outerHTML='<span class=\"product-icon\">📚</span>'">`;
                } else {
                    imageDisplay = `<span class="product-icon">${product.image}</span>`;
                }
            } else {
                imageDisplay = '<span class="product-icon">📚</span>';
            }

            row.innerHTML = `
                <td>${imageDisplay}</td>
                <td>${product.name}</td>
                <td>${product.price} ريال</td>
                <td>${product.category}</td>
                <td class="product-actions">
                    <button class="btn btn-edit" onclick="editProduct(${product.id})">✏️ تعديل</button>
                    <button class="btn btn-danger" onclick="deleteProduct(${product.id})">🗑️ حذف</button>
                </td>
            `;
            tbody.appendChild(row);
        });
        updateStats(products.length);
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

function updateStats(productCount) {
    if (productCount !== undefined) {
        document.getElementById('totalProducts').textContent = productCount;
    }
}

function showAddProductModal() {
    document.getElementById('modalTitle').textContent = 'إضافة منتج جديد';
    document.getElementById('productForm').reset();
    document.getElementById('productId').value = '';
    document.getElementById('productModal').classList.add('show');
}

function closeProductModal() {
    document.getElementById('productModal').classList.remove('show');
}

async function saveProduct(event) {
    event.preventDefault();

    const id = document.getElementById('productId').value;
    const imageInput = document.getElementById('productImage').value || '📚';

    const product = {
        name: document.getElementById('productName').value,
        price: parseFloat(document.getElementById('productPrice').value),
        category: document.getElementById('productCategory').value,
        image: imageInput
    };

    try {
        if (id) {
            await apiCall(`/products/${id}`, 'PUT', product);
        } else {
            await apiCall('/products', 'POST', product);
        }

        loadProducts();
        closeProductModal();
        alert('تم حفظ المنتج بنجاح!');
    } catch (error) {
        console.error('Error saving product:', error);
        alert('حدث خطأ أثناء حفظ المنتج');
    }
}

function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('productImage').value = e.target.result;

            // Show preview
            const preview = document.getElementById('imagePreview');
            const previewImg = document.getElementById('previewImg');
            previewImg.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

async function editProduct(id) {
    try {
        // In a real app, we might fetch single product, but here we can filter from list or fetch all
        // Let's fetch all for simplicity or fetch single if endpoint existed (we didn't make one, but PUT exists)
        // We can use the row data or fetch fresh. Let's fetch list again to find it.
        const products = await apiCall('/products');
        const product = products.find(p => p.id === id);

        if (product) {
            document.getElementById('modalTitle').textContent = 'تعديل المنتج';
            document.getElementById('productId').value = product.id;
            document.getElementById('productName').value = product.name;
            document.getElementById('productPrice').value = product.price;
            document.getElementById('productCategory').value = product.category;
            document.getElementById('productImage').value = product.image || '';

            if (product.image && (product.image.startsWith('http') || product.image.startsWith('data:image'))) {
                const preview = document.getElementById('imagePreview');
                const previewImg = document.getElementById('previewImg');
                previewImg.src = product.image;
                preview.style.display = 'block';
            }

            document.getElementById('productModal').classList.add('show');
        }
    } catch (error) {
        console.error('Error editing product:', error);
    }
}

async function deleteProduct(id) {
    if (confirm('هل أنت متأكد من حذف هذا المنتج؟')) {
        try {
            await apiCall(`/products/${id}`, 'DELETE');
            loadProducts();
            alert('تم حذف المنتج بنجاح!');
        } catch (error) {
            console.error('Error deleting product:', error);
            alert('حدث خطأ أثناء حذف المنتج');
        }
    }
}

// --- Ads Management ---

async function loadAds() {
    try {
        const ads = await apiCall('/ads');
        const adsList = document.getElementById('adsList');

        if (ads.length === 0) {
            adsList.innerHTML = '<p style="color: #94a3b8; padding: 1rem;">لا توجد إعلانات</p>';
            return;
        }

        adsList.innerHTML = ads.map((ad) => {
            let imageDisplay = '';
            if (ad.icon) {
                if (ad.icon.startsWith('http') || ad.icon.startsWith('data:image') || ad.icon.startsWith('logo.')) {
                    imageDisplay = `<img src="${ad.icon}" style="width: 60px; height: 60px; object-fit: fill; border-radius: 8px;" onerror="this.outerHTML='<span style=\"font-size: 2rem;\">🎉</span>'">`;
                } else {
                    imageDisplay = `<span style="font-size: 2rem;">${ad.icon}</span>`;
                }
            } else {
                imageDisplay = '<span style="font-size: 2rem;">🎉</span>';
            }

            return `
                <div class="ad-item">
                    <div class="ad-preview">
                        <div class="ad-image">${imageDisplay}</div>
                        <div>
                            <h4>${ad.title}</h4>
                            <p style="color: #64748b; font-size: 0.875rem;">${ad.description}</p>
                        </div>
                    </div>
                    <div style="display: flex; gap: 0.5rem;">
                        <button class="btn btn-edit" onclick="editAd(${ad.id})">✏️</button>
                        <button class="btn btn-danger" onclick="deleteAd(${ad.id})">🗑️</button>
                    </div>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading ads:', error);
    }
}

function showAddAdModal() {
    document.getElementById('adModalTitle').textContent = 'إضافة إعلان جديد';
    document.getElementById('adForm').reset();
    document.getElementById('adIndex').value = ''; // Using this as ID
    document.getElementById('adImagePreview').style.display = 'none';
    document.getElementById('adModal').classList.add('show');
}

function closeAdModal() {
    document.getElementById('adModal').classList.remove('show');
}

function handleAdImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('adIcon').value = e.target.result;

            const preview = document.getElementById('adImagePreview');
            const previewImg = document.getElementById('adPreviewImg');
            previewImg.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

async function saveAd(event) {
    event.preventDefault();

    const id = document.getElementById('adIndex').value;
    const iconInput = document.getElementById('adIcon').value || '🎉';

    const ad = {
        title: document.getElementById('adTitle').value,
        description: document.getElementById('adDescription').value,
        icon: iconInput
    };

    try {
        if (id) {
            await apiCall(`/ads/${id}`, 'PUT', ad);
        } else {
            await apiCall('/ads', 'POST', ad);
        }

        loadAds();
        closeAdModal();
        alert('تم حفظ الإعلان بنجاح!');
    } catch (error) {
        console.error('Error saving ad:', error);
        alert('حدث خطأ أثناء حفظ الإعلان');
    }
}

async function editAd(id) {
    try {
        const ads = await apiCall('/ads');
        const ad = ads.find(a => a.id === id);

        if (ad) {
            document.getElementById('adModalTitle').textContent = 'تعديل الإعلان';
            document.getElementById('adIndex').value = ad.id;
            document.getElementById('adTitle').value = ad.title;
            document.getElementById('adDescription').value = ad.description;
            document.getElementById('adIcon').value = ad.icon || '';

            if (ad.icon && (ad.icon.startsWith('http') || ad.icon.startsWith('data:image'))) {
                const preview = document.getElementById('adImagePreview');
                const previewImg = document.getElementById('adPreviewImg');
                previewImg.src = ad.icon;
                preview.style.display = 'block';
            }

            document.getElementById('adModal').classList.add('show');
        }
    } catch (error) {
        console.error('Error editing ad:', error);
    }
}

async function deleteAd(id) {
    if (confirm('هل تريد حذف هذا الإعلان؟')) {
        try {
            await apiCall(`/ads/${id}`, 'DELETE');
            loadAds();
        } catch (error) {
            console.error('Error deleting ad:', error);
        }
    }
}

// --- Offers Management ---

async function loadOffers() {
    try {
        const offers = await apiCall('/offers');
        const offersList = document.getElementById('offersList');

        if (offers.length === 0) {
            offersList.innerHTML = '<p style="color: #94a3b8; padding: 1rem;">لا توجد عروض</p>';
            return;
        }

        offersList.innerHTML = offers.map((offer) => {
            let imageDisplay = '';
            if (offer.icon) {
                if (offer.icon.startsWith('http') || offer.icon.startsWith('data:image') || offer.icon.startsWith('logo.')) {
                    imageDisplay = `<img src="${offer.icon}" style="width: 60px; height: 60px; object-fit: fill; border-radius: 8px;" onerror="this.outerHTML='<span style=\"font-size: 2rem;\">🎁</span>'">`;
                } else {
                    imageDisplay = `<span style="font-size: 2rem;">${offer.icon}</span>`;
                }
            } else {
                imageDisplay = '<span style="font-size: 2rem;">🎁</span>';
            }

            return `
                <div class="offer-item">
                    <div class="ad-preview">
                        <div class="ad-image">${imageDisplay}</div>
                        <div>
                            <h4>${offer.title}</h4>
                            <p style="color: #64748b; font-size: 0.875rem;">${offer.discount}</p>
                        </div>
                    </div>
                    <div style="display: flex; gap: 0.5rem;">
                        <button class="btn btn-edit" onclick="editOffer(${offer.id})">✏️</button>
                        <button class="btn btn-danger" onclick="deleteOffer(${offer.id})">🗑️</button>
                    </div>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading offers:', error);
    }
}

function showAddOfferModal() {
    document.getElementById('offerModalTitle').textContent = 'إضافة عرض جديد';
    document.getElementById('offerForm').reset();
    document.getElementById('offerIndex').value = '';
    document.getElementById('offerImagePreview').style.display = 'none';
    document.getElementById('offerModal').classList.add('show');
}

function closeOfferModal() {
    document.getElementById('offerModal').classList.remove('show');
}

function handleOfferImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('offerIcon').value = e.target.result;

            const preview = document.getElementById('offerImagePreview');
            const previewImg = document.getElementById('offerPreviewImg');
            previewImg.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

async function saveOffer(event) {
    event.preventDefault();

    const id = document.getElementById('offerIndex').value;
    const iconInput = document.getElementById('offerIcon').value || '🎁';

    const offer = {
        title: document.getElementById('offerTitle').value,
        discount: document.getElementById('offerDiscount').value,
        icon: iconInput
    };

    try {
        if (id) {
            await apiCall(`/offers/${id}`, 'PUT', offer);
        } else {
            await apiCall('/offers', 'POST', offer);
        }

        loadOffers();
        closeOfferModal();
        alert('تم حفظ العرض بنجاح!');
    } catch (error) {
        console.error('Error saving offer:', error);
        alert('حدث خطأ أثناء حفظ العرض');
    }
}

async function editOffer(id) {
    try {
        const offers = await apiCall('/offers');
        const offer = offers.find(o => o.id === id);

        if (offer) {
            document.getElementById('offerModalTitle').textContent = 'تعديل العرض';
            document.getElementById('offerIndex').value = offer.id;
            document.getElementById('offerTitle').value = offer.title;
            document.getElementById('offerDiscount').value = offer.discount;
            document.getElementById('offerIcon').value = offer.icon || '';

            if (offer.icon && (offer.icon.startsWith('http') || offer.icon.startsWith('data:image'))) {
                const preview = document.getElementById('offerImagePreview');
                const previewImg = document.getElementById('offerPreviewImg');
                previewImg.src = offer.icon;
                preview.style.display = 'block';
            }

            document.getElementById('offerModal').classList.add('show');
        }
    } catch (error) {
        console.error('Error editing offer:', error);
    }
}

async function deleteOffer(id) {
    if (confirm('هل تريد حذف هذا العرض؟')) {
        try {
            await apiCall(`/offers/${id}`, 'DELETE');
            loadOffers();
        } catch (error) {
            console.error('Error deleting offer:', error);
        }
    }
}

// --- Categories Management ---

async function loadCategories() {
    try {
        const categories = await apiCall('/categories');
        const categoriesList = document.getElementById('categoriesList');

        if (!categoriesList) return;

        if (categories.length === 0) {
            categoriesList.innerHTML = '<p style="color: #94a3b8; padding: 1rem;">لا توجد أقسام</p>';
            return;
        }

        categoriesList.innerHTML = categories.map((category) => `
            <div class="ad-item">
                <div class="ad-preview">
                    <div class="ad-image">${category.icon || '📁'}</div>
                    <div>
                        <h4>${category.name}</h4>
                    </div>
                </div>
                <div style="display: flex; gap: 0.5rem;">
                    <button class="btn btn-edit" onclick="editCategory(${category.id})">✏️</button>
                    <button class="btn btn-danger" onclick="deleteCategory(${category.id})">🗑️</button>
                </div>
            </div>
        `).join('');

        document.getElementById('totalCategories').textContent = categories.length;
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

function showAddCategoryModal() {
    document.getElementById('categoryModalTitle').textContent = 'إضافة قسم جديد';
    document.getElementById('categoryForm').reset();
    document.getElementById('categoryIndex').value = '';
    document.getElementById('categoryModal').classList.add('show');
}

function closeCategoryModal() {
    document.getElementById('categoryModal').classList.remove('show');
}

async function saveCategory(event) {
    event.preventDefault();

    const id = document.getElementById('categoryIndex').value;

    const category = {
        name: document.getElementById('categoryName').value,
        icon: document.getElementById('categoryIcon').value
    };

    try {
        if (id) {
            await apiCall(`/categories/${id}`, 'PUT', category);
        } else {
            await apiCall('/categories', 'POST', category);
        }

        loadCategories();
        populateCategoryDropdown();
        closeCategoryModal();
        alert('تم حفظ القسم بنجاح!');
    } catch (error) {
        console.error('Error saving category:', error);
        alert('حدث خطأ أثناء حفظ القسم');
    }
}

async function editCategory(id) {
    try {
        const categories = await apiCall('/categories');
        const category = categories.find(c => c.id === id);

        if (category) {
            document.getElementById('categoryModalTitle').textContent = 'تعديل القسم';
            document.getElementById('categoryIndex').value = category.id;
            document.getElementById('categoryName').value = category.name;
            document.getElementById('categoryIcon').value = category.icon;

            document.getElementById('categoryModal').classList.add('show');
        }
    } catch (error) {
        console.error('Error editing category:', error);
    }
}

async function deleteCategory(id) {
    if (confirm('هل تريد حذف هذا القسم؟ سيتم حذف جميع المنتجات في هذا القسم أيضاً.')) {
        try {
            await apiCall(`/categories/${id}`, 'DELETE');
            loadCategories();
            loadProducts();
            populateCategoryDropdown();
            alert('تم حذف القسم والمنتجات المرتبطة به بنجاح!');
        } catch (error) {
            console.error('Error deleting category:', error);
            alert('حدث خطأ أثناء حذف القسم');
        }
    }
}

async function populateCategoryDropdown() {
    try {
        const categories = await apiCall('/categories');
        const dropdown = document.getElementById('productCategory');

        if (!dropdown) return;

        dropdown.innerHTML = categories.map(cat =>
            `<option value="${cat.name}">${cat.icon || ''} ${cat.name}</option>`
        ).join('');
    } catch (error) {
        console.error('Error populating categories:', error);
    }
}
