document.addEventListener('DOMContentLoaded', () => {
    
    const API_PREFIX = '/api';
    let state = {
        suppliers: [],
        products: [],
        currentUser: null,
    };

    const elements = {
        supplierCount: document.getElementById('supplier-count'),
        suppliersTableBody: document.getElementById('suppliers-table-body'),
    };

    async function checkAuthentication() {
        try {
            const token = localStorage.getItem('token');
            if (!token) throw new Error('Não autenticado');

            const response = await fetch(`${API_PREFIX}/me`, {
                headers: { 'Authorization': `Bearer ${token}` }
            }); 
            if (!response.ok) throw new Error('Sessão inválida');
            
            state.currentUser = await response.json();
            await initPage();
            document.body.classList.remove('hidden');
        } catch (error) {
            console.error('Falha na autenticação:', error.message);
            localStorage.removeItem('token');
            localStorage.removeItem('refresh');
            window.location.href = '/';
        }
    }

    async function initPage() {
        await Promise.all([
            loadSuppliers(), 
            loadProducts()
        ]);
        setupEventListeners();
    }

    async function fetchData(url, options = {}) {
        const fullUrl = `${API_PREFIX}${url}`;
        const token = localStorage.getItem('token');
        
        options.headers = options.headers || {};
        if (token) options.headers['Authorization'] = `Bearer ${token}`;
        if (options.body && !options.headers['Content-Type']) {
            options.headers['Content-Type'] = 'application/json';
        }

        const response = await fetch(fullUrl, options);
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || errorData.error || 'Falha na requisição');
        }
        if (options.method === 'DELETE' || response.status === 204) return; 
        return response.json();
    }

    async function loadProducts() {
        try {
            const products = await fetchData('/products'); 
            state.products = products.map(p => ({ id: p.id, text: p.name }));
        } catch (error) {
            console.error('Erro ao carregar lista de produtos:', error);
        }
    }

    async function loadSuppliers() {
        try {
            const suppliers = await fetchData('/suppliers'); 
            state.suppliers = suppliers;
            elements.supplierCount.textContent = suppliers.length;

            elements.suppliersTableBody.innerHTML = '';
            if (suppliers.length === 0) {
                renderEmptyRow(elements.suppliersTableBody, 6, "Nenhum fornecedor cadastrado.");
                return;
            }

            suppliers.forEach(supplier => {
                const tr = document.createElement('tr');
                const addressText = `${supplier.address || ''} ${supplier.city || ''}, ${supplier.state || ''}`.trim();
                
                tr.innerHTML = `
                    <td>${supplier.name || ''}</td>
                    <td>${supplier.cnpj || ''}</td>
                    <td>${supplier.email || ''}</td>
                    <td>${supplier.phone || ''}</td>
                    <td>${addressText}</td>
                    <td class="text-end action-icons">
                        <button class="btn-action edit" data-id="${supplier.id}" title="Editar">
                            <i class="fa-solid fa-pencil"></i>
                        </button>
                        <button class="btn-action delete" data-id="${supplier.id}" title="Excluir">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    </td>
                `;
                elements.suppliersTableBody.appendChild(tr);
            });
        } catch (error) {
            console.error('Erro ao carregar fornecedores:', error);
            renderEmptyRow(elements.suppliersTableBody, 6, "Erro ao carregar fornecedores.");
        }
    }

    function renderEmptyRow(tbody, colSpan, message) {
        tbody.innerHTML = `<tr><td colspan="${colSpan}" class="text-center text-muted">${message}</td></tr>`;
    }

    function setupEventListeners() {
        document.getElementById('btn-new-supplier').addEventListener('click', () => showSupplierModal());
        
        elements.suppliersTableBody.addEventListener('click', e => {
            const btn = e.target.closest('.btn-action');
            if (!btn) return;
            const id = btn.dataset.id;
            if (btn.classList.contains('edit')) showSupplierModal(id);
            if (btn.classList.contains('delete')) showDeleteModal(id);
        });
        
        document.getElementById('logout-btn').addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('token');
            localStorage.removeItem('refresh');
            window.location.href = '/';
        });

        document.querySelector('.btn-search').addEventListener('click', (e) => {
             console.log('Buscando fornecedor...');
        });
    }

    function showDeleteModal(id) {
        Swal.fire({
            title: 'Tem certeza?',
            text: "Excluir um fornecedor pode afetar produtos e movimentações relacionadas.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sim, excluir!',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) handleDeleteSupplier(id);
        });
    }

    async function handleDeleteSupplier(id) {
        try {
            await fetchData(`/suppliers/${id}`, { method: 'DELETE' });
            Swal.fire('Excluído!', 'O fornecedor foi excluído com sucesso.', 'success');
            loadSuppliers();
        } catch (error) {
            Swal.fire('Erro!', `Não foi possível excluir o fornecedor. ${error.message}`, 'error');
        }
    }

    async function showSupplierModal(id = null) {
        const isEdit = id !== null;
        let supplier = {};
        let selectedProductIds = [];
        
        if (isEdit) {
            try {
                supplier = await fetchData(`/suppliers/${id}`);
                selectedProductIds = (supplier.products || []).map(p => p.id || p);
            } catch (error) {
                Swal.fire('Erro!', 'Não foi possível carregar os dados do fornecedor.', 'error');
                return;
            }
        }
        
        const productsOptionsHtml = state.products.map(p => 
            `<option value="${p.id}" ${selectedProductIds.includes(p.id) ? 'selected' : ''}>${p.text}</option>`
        ).join('');

        const htmlContent = `
            <form id="supplier-form">
                <div class="swal-form-group row justify-content-center align-items-center">
                    <label class="col-12">Razão Social</label>
                    <input id="swal-supplier-name" class="swal2-input" value="${supplier.name || ''}" placeholder="Ex: Tech Distribuidora">
                </div>
                <div class="swal-form-group row justify-content-center align-items-center">
                    <label class="col-12">CNPJ</label>
                    <input id="swal-supplier-cnpj" class="swal2-input" value="${supplier.cnpj || ''}" placeholder="Ex: 12.345.678/0001-99">
                </div>
                <div class="swal-form-group row justify-content-center align-items-center">
                    <label class="col-12">E-mail</label>
                    <input id="swal-supplier-email" type="email" class="swal2-input" value="${supplier.email || ''}" placeholder="Ex: contato@empresa.com">
                </div>
                <div class="swal-form-group row justify-content-center align-items-center">
                    <label class="col-12">Telefone</label>
                    <input id="swal-supplier-phone" class="swal2-input col-12" value="${supplier.phone || ''}" placeholder="Ex: 11999990001">
                </div>
                <div class="swal-form-group row justify-content-center align-items-center">
                    <label class="col-12">Endereço</label>
                    <input id="swal-supplier-address" class="swal2-input col-12" value="${supplier.address || ''}" placeholder="Rua Tecnologia, 100">
                </div>
                <div class="swal-form-group row justify-content-center align-items-center">
                    <label class="col-12">CEP</label>
                    <input id="swal-supplier-zipCode" class="swal2-input col-12" value="${supplier.zipCode || ''}" placeholder="Ex: 01001-000">
                </div>
                <div class="swal-form-group row justify-content-center align-items-center">
                    <label class="col-12">Produtos Fornecidos</label>
                    <select id="swal-supplier-products" class="form-select col-12" multiple="multiple">
                        ${productsOptionsHtml}
                    </select>
                    <small class="text-muted d-block mt-1">Selecione um ou mais produtos fornecidos.</small>
                </div>
            </form>
        `;

        Swal.fire({
            title: isEdit ? 'Editar Fornecedor' : 'Novo Fornecedor',
            html: htmlContent,
            showCancelButton: true,
            confirmButtonText: 'Salvar',
            didOpen: () => {
                $('#swal-supplier-products').select2({
                    dropdownParent: $('.swal2-container'),
                    placeholder: "Selecione produtos...",
                    allowClear: true
                });
            },
            preConfirm: () => {
                const data = {
                    name: document.getElementById('swal-supplier-name').value,
                    cnpj: document.getElementById('swal-supplier-cnpj').value,
                    email: document.getElementById('swal-supplier-email').value,
                    phone: document.getElementById('swal-supplier-phone').value,
                    address: document.getElementById('swal-supplier-address').value,
                    zipCode: document.getElementById('swal-supplier-zipCode').value,
                    products: $('#swal-supplier-products').val()?.map(id => parseInt(id, 10)) || [], 
                };
                
                if (!data.name || !data.cnpj || !data.email) {
                    Swal.showValidationMessage('Razão Social, CNPJ e E-mail são obrigatórios.');
                    return false;
                }
                return data;
            }
        }).then((result) => {
            $('#swal-supplier-products').select2('destroy'); 
            if (result.isConfirmed) handleSaveSupplier(id, result.value);
        });
    }
    
    async function handleSaveSupplier(id, data) {
        const url = id ? `/suppliers/${id}` : '/suppliers';
        const method = id ? 'PATCH' : 'POST';

        try {
            await fetchData(url, {
                method: method,
                body: JSON.stringify(data)
            });
            Swal.fire('Salvo!', 'Fornecedor salvo com sucesso.', 'success');
            loadSuppliers(); 
        } catch (error) {
            Swal.fire('Erro!', `Não foi possível salvar o fornecedor. ${error.message}`, 'error');
        }
    }

    checkAuthentication();
});
