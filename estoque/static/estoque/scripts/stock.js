document.addEventListener('DOMContentLoaded', () => {

    const API_PREFIX = '/api';

    let state = {
        products: [],
        categories: [],
        currentUser: null,
    };

    const elements = {
        categoryCount: document.getElementById('category-count'),
        productCount: document.getElementById('product-count'),
        categoriesTableBody: document.getElementById('categories-table-body'),
        productsTableBody: document.getElementById('products-table-body'),
        movementsTableBody: document.getElementById('movements-table-body'),
    };

    async function checkAuthentication() {
        try {
            const token = localStorage.getItem('token');
            if (!token) throw new Error('Não autenticado');

            const response = await fetch(`${API_PREFIX}/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            if (!response.ok) throw new Error('Não autenticado');

            state.currentUser = await response.json();
            await initPage();
            document.body.classList.remove('hidden');
        } catch (error) {
            console.error('Falha na autenticação:', error.message);
            window.location.href = '/';
        }
    }

    async function initPage() {
        await Promise.all([
            loadCategories(),
            loadProducts(),
            loadMovements()
        ]);
        setupEventListeners();
    }

    async function fetchData(url, options = {}) {
        const fullUrl = `${API_PREFIX}${url}`;
        const token = localStorage.getItem('token');
        options.headers = {
            ...(options.headers || {}),
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };

        const response = await fetch(fullUrl, options);
        if (!response.ok) {
            let err;
            try {
                err = await response.json();
            } catch {
                err = {};
            }
            throw new Error(err.detail || err.error || 'Falha na requisição');
        }
        if (options.method === 'DELETE' || response.status === 204) return;
        return response.json();
    }

    async function loadCategories() {
        try {
            const categories = await fetchData('/category');
            state.categories = categories;
            elements.categoryCount.textContent = categories.length;
            elements.categoriesTableBody.innerHTML = '';

            if (categories.length === 0) {
                renderEmptyRow(elements.categoriesTableBody, 4, "Nenhuma categoria encontrada.");
                return;
            }

            categories.forEach(cat => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${cat.id}</td>
                    <td>${cat.name}</td>
                    <td>${cat.description || 'N/A'}</td>
                    <td class="text-end action-icons">
                        <button class="btn-action edit" data-id="${cat.id}" title="Editar"><i class="fa-solid fa-pencil"></i></button>
                        <button class="btn-action delete" data-id="${cat.id}" title="Excluir"><i class="fa-solid fa-trash-can"></i></button>
                    </td>
                `;
                elements.categoriesTableBody.appendChild(tr);
            });
        } catch (error) {
            console.error('Erro ao carregar categorias:', error);
            renderEmptyRow(elements.categoriesTableBody, 4, "Erro ao carregar categorias.");
        }
    }

    async function loadProducts() {
        try {
            const products = await fetchData('/products');
            state.products = products;
            elements.productCount.textContent = products.length;
            elements.productsTableBody.innerHTML = '';

            if (products.length === 0) {
                renderEmptyRow(elements.productsTableBody, 7, "Nenhum produto encontrado.");
                return;
            }

            products.forEach(p => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${p.name}</td>
                    <td>${p.description || 'N/A'}</td>
                    <td>${p.quatityStock}</td>
                    <td>R$ ${p.costPrice.toFixed(2)}</td>
                    <td>R$ ${p.salePrice.toFixed(2)}</td>
                    <td>${p.categoryName}</td>
                    <td class="text-end action-icons">
                        <button class="btn-action edit" data-id="${p.id}" title="Editar"><i class="fa-solid fa-pencil"></i></button>
                        <button class="btn-action delete" data-id="${p.id}" title="Excluir"><i class="fa-solid fa-trash-can"></i></button>
                    </td>
                `;
                elements.productsTableBody.appendChild(tr);
            });
        } catch (error) {
            console.error('Erro ao carregar produtos:', error);
            renderEmptyRow(elements.productsTableBody, 7, "Erro ao carregar produtos.");
        }
    }

    async function loadMovements() {
        try {
            const movements = await fetchData('/stock/movements');
            elements.movementsTableBody.innerHTML = '';

            if (movements.length === 0) {
                renderEmptyRow(elements.movementsTableBody, 7, "Nenhuma movimentação encontrada.");
                return;
            }

            movements.forEach(mov => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${mov.id}</td>
                    <td><span class="badge bg-${mov.type === 'ENTRADA' ? 'success' : 'danger'}">${mov.type}</span></td>
                    <td>${mov.quantity}</td>
                    <td>${mov.product.name}</td>
                    <td>${mov.user.name}</td>
                    <td>${formatDate(mov.date)}</td>
                    <td class="text-end action-icons">
                        <button class="btn-action edit" data-id="${mov.id}" title="Editar"><i class="fa-solid fa-pencil"></i></button>
                        <button class="btn-action delete" data-id="${mov.id}" title="Excluir"><i class="fa-solid fa-trash-can"></i></button>
                    </td>
                `;
                elements.movementsTableBody.appendChild(tr);
            });

        } catch (error) {
            console.error('Erro ao carregar movimentações:', error);
            renderEmptyRow(elements.movementsTableBody, 7, "Erro ao carregar movimentações.");
        }
    }

    function renderEmptyRow(tbody, colSpan, message) {
        tbody.innerHTML = `
            <tr><td colspan="${colSpan}" class="text-center text-muted">${message}</td></tr>
        `;
    }

    function formatDate(isoString) {
        if (!isoString) return 'N/A';
        const date = new Date(isoString);
        return date.toLocaleString('pt-BR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    function setupEventListeners() {
        document.getElementById('btn-new-category').addEventListener('click', () => showCategoryModal());
        document.getElementById('btn-new-product').addEventListener('click', () => showProductModal());
        document.getElementById('btn-new-movement').addEventListener('click', () => showMovementModal());

        elements.categoriesTableBody.addEventListener('click', e => handleTableActions(e, 'category'));
        elements.productsTableBody.addEventListener('click', e => handleTableActions(e, 'product'));
        elements.movementsTableBody.addEventListener('click', e => handleTableActions(e, 'movement'));

        // Busca de Categorias
        const searchCategoriesInput = document.getElementById('search-categories');
        const searchCategoriesBtn = searchCategoriesInput.nextElementSibling;
        
        searchCategoriesBtn.addEventListener('click', () => filterCategories());
        searchCategoriesInput.addEventListener('keyup', (e) => {
            if (e.key === 'Enter') filterCategories();
        });
        searchCategoriesInput.addEventListener('input', () => {
            if (searchCategoriesInput.value === '') filterCategories();
        });

        // Busca de Produtos
        const searchProductsInput = document.getElementById('search-products');
        const searchProductsBtn = searchProductsInput.nextElementSibling;
        
        searchProductsBtn.addEventListener('click', () => filterProducts());
        searchProductsInput.addEventListener('keyup', (e) => {
            if (e.key === 'Enter') filterProducts();
        });
        searchProductsInput.addEventListener('input', () => {
            if (searchProductsInput.value === '') filterProducts();
        });

        // Busca de Movimentações
        const searchMovementsInput = document.getElementById('search-movements');
        const searchMovementsBtn = searchMovementsInput.nextElementSibling;
        
        searchMovementsBtn.addEventListener('click', () => filterMovements());
        searchMovementsInput.addEventListener('keyup', (e) => {
            if (e.key === 'Enter') filterMovements();
        });
        searchMovementsInput.addEventListener('input', () => {
            if (searchMovementsInput.value === '') filterMovements();
        });

        document.getElementById('logout-btn').addEventListener('click', e => {
            e.preventDefault();
            localStorage.removeItem('token');
            localStorage.removeItem('refresh');
            window.location.href = '/';
        });
    }

    function handleTableActions(e, type) {
        const btn = e.target.closest('.btn-action');
        if (!btn) return;
        const id = btn.dataset.id;

        if (btn.classList.contains('edit')) {
            if (type === 'category') showCategoryModal(id);
            if (type === 'product') showProductModal(id);
            if (type === 'movement') showMovementModal(id);
        }
        if (btn.classList.contains('delete')) {
            showDeleteModal(id, type);
        }
    }

    // --- MODAIS ---

    async function showDeleteModal(id, type) {
        const result = await Swal.fire({
            title: 'Tem certeza?',
            text: 'Esta ação não pode ser desfeita!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sim, excluir',
            cancelButtonText: 'Cancelar'
        });
        if (result.isConfirmed) handleDelete(id, type);
    }

    async function handleDelete(id, type) {
        let url, reload;
        if (type === 'product') { url = `/products/${id}`; reload = loadProducts; }
        else if (type === 'category') { url = `/category/${id}`; reload = loadCategories; }
        else if (type === 'movement') { url = `/stock/movements/${id}`; reload = loadMovements; }
        else return;

        try {
            await fetchData(url, { method: 'DELETE' });
            Swal.fire('Excluído!', 'Removido com sucesso.', 'success');
            await loadProducts();
            await loadCategories();
            await loadMovements();
        } catch (e) {
            Swal.fire('Erro!', e.message, 'error');
        }
    }

    async function showCategoryModal(id = null) {
        const isEdit = !!id;
        let cat = { name: '', description: '' };

        if (isEdit) {
            try {
                cat = await fetchData(`/category/${id}`);
            } catch {
                return Swal.fire('Erro!', 'Falha ao carregar categoria.', 'error');
            }
        }

        const { value: data } = await Swal.fire({
            title: isEdit ? 'Editar Categoria' : 'Nova Categoria',
            html: `
                <div class="row justify-content-center align-items-center">
                    <label for="cat-name" class="form-label col-12">Nome</label>
                    <input id="cat-name" class="swal2-input col-12" placeholder="Nome" value="${cat.name || ''}">
                </div>
                <div class="row justify-content-center align-items-center">
                    <label for="cat-desc" class="form-label col-12">Descrição</label>
                    <textarea id="cat-desc" class="swal2-textarea col-12" placeholder="Descrição">${cat.description || ''}</textarea>
                </div>
            `,
            focusConfirm: false,
            preConfirm: () => ({
                name: document.getElementById('cat-name').value,
                description: document.getElementById('cat-desc').value
            }),
            showCancelButton: true,
            confirmButtonText: isEdit ? 'Salvar' : 'Cadastrar'
        });

        if (data) {
            try {
                if (isEdit)
                    await fetchData(`/category/${id}`, { method: 'PUT', body: JSON.stringify(data) });
                else
                    await fetchData(`/category`, { method: 'POST', body: JSON.stringify(data) });

                Swal.fire('Sucesso!', 'Categoria salva com sucesso.', 'success');
                loadCategories();
            } catch (e) {
                Swal.fire('Erro!', e.message, 'error');
            }
        }
    }

    async function showProductModal(id = null) {
        const isEdit = !!id;
        let product = { name: '', description: '', costPrice: '', salePrice: '', quatityStock: 0, categoryId: '' };

        if (isEdit) {
            try {
                product = await fetchData(`/products/${id}`);
            } catch {
                return Swal.fire('Erro!', 'Falha ao carregar produto.', 'error');
            }
        }

        const options = state.categories.map(c => `
            <option value="${c.id}" ${c.id === product.categoryId ? 'selected' : ''}>${c.name}</option>
        `).join('');

        const { value: data } = await Swal.fire({
            title: isEdit ? 'Editar Produto' : 'Novo Produto',
            html: `
                <div class="row justify-content-center align-items-center">
                    <label for="prod-name" class="form-label col-12">Nome</label>
                    <input id="prod-name" class="swal2-input col-12" placeholder="Nome" value="${product.name || ''}">
                </div>
                <div class="row justify-content-center align-items-center">
                    <label for="prod-desc" class="form-label col-12">Descrição</label>
                    <textarea id="prod-desc" class="swal2-textarea col-12" placeholder="Descrição">${product.description || ''}</textarea>
                </div>
                <div class="row justify-content-center align-items-center">
                    <label for="prod-cost" class="form-label col-12">Preço de custo</label>
                    <input id="prod-cost" type="number" class="swal2-input col-12" placeholder="Preço de custo" value="${product.costPrice || ''}">
                </div>
                <div class="row justify-content-center align-items-center">
                    <label for="prod-sale" class="form-label col-12">Preço de venda</label>
                    <input id="prod-sale" type="number" class="swal2-input col-12" placeholder="Preço de venda" value="${product.salePrice || ''}">
                </div>
                <div class="row justify-content-center align-items-center">
                    <label for="prod-stock" class="form-label col-12">Estoque</label>
                    <input id="prod-stock" type="number" class="swal2-input col-12" placeholder="Estoque" value="${product.quatityStock || 0}">
                </div>
                <div class="row justify-content-center align-items-center">
                    <label for="prod-cat" class="form-label col-12">Categoria</label>
                    <select id="prod-cat" class="swal2-select col-12">${options}</select>
                </div>
            `,
            preConfirm: () => ({
                name: document.getElementById('prod-name').value,
                description: document.getElementById('prod-desc').value,
                costPrice: parseFloat(document.getElementById('prod-cost').value),
                salePrice: parseFloat(document.getElementById('prod-sale').value),
                quatityStock: parseInt(document.getElementById('prod-stock').value),
                categoryId: parseInt(document.getElementById('prod-cat').value)
            }),
            showCancelButton: true,
            confirmButtonText: isEdit ? 'Salvar' : 'Cadastrar'
        });

        if (data) {
            try {
                if (isEdit)
                    await fetchData(`/products/${id}`, { method: 'PUT', body: JSON.stringify(data) });
                else
                    await fetchData(`/products`, { method: 'POST', body: JSON.stringify(data) });

                Swal.fire('Sucesso!', 'Produto salvo com sucesso.', 'success');
                loadProducts();
            } catch (e) {
                Swal.fire('Erro!', e.message, 'error');
            }
        }
    }

    async function showMovementModal(id = null) {
        const isEdit = !!id;
        let mov = {};

        const productOptions = state.products.map(p => `
            <option value="${p.id}">${p.name} (Estoque: ${p.quatityStock})</option>
        `).join('');

        if (isEdit) {
            try {
                mov = await fetchData(`/stock/movements/${id}`);
            } catch {
                return Swal.fire('Erro!', 'Falha ao carregar movimentação.', 'error');
            }
        }

        const { value: data } = await Swal.fire({
            title: isEdit ? 'Editar Movimentação' : 'Nova Movimentação',
            html: `
                
                <div class="row justify-content-center align-items-center">
                    <label for="mov-type" class="form-label col-12">Tipo</label>
                    <select id="mov-type" class="swal2-select col-12">
                    <option value="ENTRADA" ${mov.type === 'ENTRADA' ? 'selected' : ''}>ENTRADA</option>
                    <option value="SAIDA" ${mov.type === 'SAIDA' ? 'selected' : ''}>SAÍDA</option>
                </select>
                </div>
                <div class="row justify-content-center align-items-center">
                    <label for="mov-prod" class="form-label col-12">Produto</label>
                    <select id="mov-prod" class="swal2-select col-12" ${isEdit ? 'disabled' : ''}>
                    <option value="">Selecione o produto</option>${productOptions}
                </select>
                </div>
                <div class="row justify-content-center align-items-center">
                    <label for="mov-qty" class="form-label col-12">Quantidade</label>
                    <input id="mov-qty" type="number" class="swal2-input col-12" min="1" value="${mov.quantity || 1}">
                </div>
                
            `,
            preConfirm: () => {
                const type = document.getElementById('mov-type').value;
                const qty = parseInt(document.getElementById('mov-qty').value);
                const product_id = isEdit ? mov.product.id : parseInt(document.getElementById('mov-prod').value);
                if (!product_id || !qty) {
                    Swal.showValidationMessage('Preencha todos os campos.');
                    return;
                }
                return { type, quantity: qty, product_id };
            },
            showCancelButton: true,
            confirmButtonText: isEdit ? 'Salvar' : 'Registrar'
        });

        if (data) {
            try {
                if (isEdit)
                    await fetchData(`/stock/movements/${id}`, { method: 'PUT', body: JSON.stringify(data) });
                else
                    await fetchData(`/stock/movements`, { method: 'POST', body: JSON.stringify(data) });

                Swal.fire('Sucesso!', 'Movimentação salva com sucesso.', 'success');
                loadMovements();
                loadProducts();
            } catch (e) {
                Swal.fire('Erro!', e.message, 'error');
            }
        }
    }

    function filterCategories() {
        const searchTerm = document.getElementById('search-categories').value.toLowerCase().trim();
        const filteredCategories = state.categories.filter(cat => 
            cat.name.toLowerCase().includes(searchTerm) ||
            (cat.description && cat.description.toLowerCase().includes(searchTerm)) ||
            cat.id.toString().includes(searchTerm)
        );

        elements.categoriesTableBody.innerHTML = '';
        if (filteredCategories.length === 0) {
            renderEmptyRow(elements.categoriesTableBody, 4, "Nenhuma categoria encontrada.");
            return;
        }

        filteredCategories.forEach(cat => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${cat.id}</td>
                <td>${cat.name}</td>
                <td>${cat.description || 'N/A'}</td>
                <td class="text-end action-icons">
                    <button class="btn-action edit" data-id="${cat.id}" title="Editar"><i class="fa-solid fa-pencil"></i></button>
                    <button class="btn-action delete" data-id="${cat.id}" title="Excluir"><i class="fa-solid fa-trash-can"></i></button>
                </td>
            `;
            elements.categoriesTableBody.appendChild(tr);
        });
    }

    function filterProducts() {
        const searchTerm = document.getElementById('search-products').value.toLowerCase().trim();
        const filteredProducts = state.products.filter(p => 
            p.name.toLowerCase().includes(searchTerm) ||
            (p.description && p.description.toLowerCase().includes(searchTerm)) ||
            (p.categoryName && p.categoryName.toLowerCase().includes(searchTerm))
        );

        elements.productsTableBody.innerHTML = '';
        if (filteredProducts.length === 0) {
            renderEmptyRow(elements.productsTableBody, 7, "Nenhum produto encontrado.");
            return;
        }

        filteredProducts.forEach(p => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${p.name}</td>
                <td>${p.description || 'N/A'}</td>
                <td>${p.quatityStock}</td>
                <td>R$ ${p.costPrice.toFixed(2)}</td>
                <td>R$ ${p.salePrice.toFixed(2)}</td>
                <td>${p.categoryName}</td>
                <td class="text-end action-icons">
                    <button class="btn-action edit" data-id="${p.id}" title="Editar"><i class="fa-solid fa-pencil"></i></button>
                    <button class="btn-action delete" data-id="${p.id}" title="Excluir"><i class="fa-solid fa-trash-can"></i></button>
                </td>
            `;
            elements.productsTableBody.appendChild(tr);
        });
    }

    function filterMovements() {
        const searchTerm = document.getElementById('search-movements').value.toLowerCase().trim();
        
        fetchData('/stock/movements').then(movements => {
            const filteredMovements = movements.filter(mov => 
                mov.type.toLowerCase().includes(searchTerm) ||
                mov.product.name.toLowerCase().includes(searchTerm) ||
                mov.user.name.toLowerCase().includes(searchTerm) ||
                mov.id.toString().includes(searchTerm)
            );

            elements.movementsTableBody.innerHTML = '';
            if (filteredMovements.length === 0) {
                renderEmptyRow(elements.movementsTableBody, 7, "Nenhuma movimentação encontrada.");
                return;
            }

            filteredMovements.forEach(mov => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${mov.id}</td>
                    <td><span class="badge bg-${mov.type === 'ENTRADA' ? 'success' : 'danger'}">${mov.type}</span></td>
                    <td>${mov.quantity}</td>
                    <td>${mov.product.name}</td>
                    <td>${mov.user.name}</td>
                    <td>${formatDate(mov.date)}</td>
                    <td class="text-end action-icons">
                        <button class="btn-action edit" data-id="${mov.id}" title="Editar"><i class="fa-solid fa-pencil"></i></button>
                        <button class="btn-action delete" data-id="${mov.id}" title="Excluir"><i class="fa-solid fa-trash-can"></i></button>
                    </td>
                `;
                elements.movementsTableBody.appendChild(tr);
            });
        }).catch(error => {
            console.error('Erro ao filtrar movimentações:', error);
            renderEmptyRow(elements.movementsTableBody, 7, "Erro ao filtrar movimentações.");
        });
    }

    checkAuthentication();
});
