document.addEventListener('DOMContentLoaded', () => {
    const API_PREFIX = '/api';

    let state = {
        users: [],
        currentUser: null,
    };

    const elements = {
        userCount: document.getElementById('user-count'),
        usersTableBody: document.getElementById('users-table-body'),
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

            if (state.currentUser.role !== 'ADMIN') {
                Swal.fire({
                    title: 'Acesso Negado',
                    text: 'Apenas administradores podem acessar esta página.',
                    icon: 'error',
                    confirmButtonText: 'Voltar ao Dashboard'
                }).then(() => {
                    window.location.href = '/dashboard';
                });
                return;
            }

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
        await loadUsers();
        setupEventListeners();
    }

    async function fetchData(url, options = {}) {
        const token = localStorage.getItem('token');
        const headers = options.headers || {};

        if (token) headers['Authorization'] = `Bearer ${token}`;
        if (options.body && !headers['Content-Type']) headers['Content-Type'] = 'application/json';

        const response = await fetch(`${API_PREFIX}${url}`, { ...options, headers });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || errorData.error || 'Falha na requisição');
        }

        if (options.method === 'DELETE' || response.status === 204) return;
        return response.json();
    }

    async function loadUsers() {
        try {
            const users = await fetchData('/users');
            state.users = users;
            elements.userCount.textContent = users.length;

            elements.usersTableBody.innerHTML = '';
            if (users.length === 0) {
                renderEmptyRow("Nenhum usuário encontrado.");
                return;
            }

            users.forEach(user => {
                const tr = document.createElement('tr');
                const isCurrentUser = user.id === state.currentUser.id;

                const adminIcon = user.role === 'ADMIN'
                    ? '<i class="fa-solid fa-circle-check admin-icon yes" title="Administrador"></i>'
                    : '<i class="fa-solid fa-circle-xmark admin-icon no" title="Colaborador"></i>';

                const username = user.email.split('@')[0];

                tr.innerHTML = `
                    <td>${username}</td>
                    <td>${user.email}</td>
                    <td>${user.name}</td>
                    <td class="text-center">${adminIcon}</td>
                    <td class="text-end action-icons">
                        <button class="btn-action edit" data-id="${user.id}" title="Editar">
                            <i class="fa-solid fa-pencil"></i>
                        </button>
                        <button class="btn-action delete" data-id="${user.id}" title="Excluir" ${isCurrentUser ? 'disabled' : ''}>
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    </td>
                `;
                elements.usersTableBody.appendChild(tr);
            });
        } catch (error) {
            console.error('Erro ao carregar usuários:', error);
            renderEmptyRow("Erro ao carregar usuários.");
        }
    }

    function renderEmptyRow(message) {
        elements.usersTableBody.innerHTML = `
            <tr><td colspan="5" class="text-center text-muted">${message}</td></tr>`;
    }

    function setupEventListeners() {
        document.getElementById('btn-new-user').addEventListener('click', () => showUserModal());

        elements.usersTableBody.addEventListener('click', e => {
            const btn = e.target.closest('.btn-action');
            if (!btn) return;
            const id = btn.dataset.id;
            if (btn.classList.contains('edit')) showUserModal(id);
            if (btn.classList.contains('delete')) showDeleteModal(id);
        });

        // Busca de Usuários
        const searchUsersInput = document.getElementById('search-users');
        const searchUsersBtn = searchUsersInput.nextElementSibling;
        
        searchUsersBtn.addEventListener('click', () => filterUsers());
        searchUsersInput.addEventListener('keyup', (e) => {
            if (e.key === 'Enter') filterUsers();
        });
        searchUsersInput.addEventListener('input', () => {
            if (searchUsersInput.value === '') filterUsers();
        });

        document.getElementById('logout-btn').addEventListener('click', e => {
            e.preventDefault();
            localStorage.removeItem('token');
            localStorage.removeItem('refresh');
            window.location.href = '/';
        });
    }

    function showDeleteModal(id) {
        Swal.fire({
            title: 'Tem certeza?',
            text: 'Você não poderá reverter esta ação!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sim, excluir!',
            cancelButtonText: 'Cancelar'
        }).then(result => {
            if (result.isConfirmed) handleDelete(id);
        });
    }

    async function handleDelete(id) {
        if (id == state.currentUser.id) {
            Swal.fire('Erro!', 'Você não pode excluir sua própria conta.', 'error');
            return;
        }

        try {
            await fetchData(`/users/${id}`, { method: 'DELETE' });
            Swal.fire('Excluído!', 'O usuário foi removido com sucesso.', 'success');
            loadUsers();
        } catch (error) {
            Swal.fire('Erro!', error.message, 'error');
        }
    }

    async function showUserModal(id = null) {
        const isEdit = !!id;
        let user = {};

        if (isEdit) {
            try {
                user = await fetchData(`/users/${id}`);
            } catch {
                Swal.fire('Erro', 'Não foi possível carregar os dados do usuário.', 'error');
                return;
            }
        }

        const passwordField = !isEdit
            ? `<div class="row justify-content-center align-items-center">
                   <label for="swal-user-pass" class="col-12">Senha</label>
                   <input id="swal-user-pass" type="password" class="swal2-input col-12" placeholder="Mínimo 6 caracteres">
               </div>`
            : '';

        Swal.fire({
            title: isEdit ? 'Editar Usuário' : 'Novo Usuário',
            html: `
                <div class="row justify-content-center aling-items-center">
                    <label class="col-12">Nome Completo</label>
                    <input id="swal-user-name" class="swal2-input col-12" value="${user.name || ''}">
                </div>
                <div class="row justify-content-center aling-items-center">
                    <label class="col-12">E-mail</label>
                    <input id="swal-user-email" class="swal2-input col-12" type="email" value="${user.email || ''}">
                </div>
                <div class="row justify-content-center aling-items-center">
                    <label class="col-12">Cargo</label>
                    <input id="swal-user-job" class="swal2-input col-12" value="${user.jobTitle || ''}">
                </div>
                ${passwordField}
                <div class="row justify-content-center aling-items-center">
                    <label class="col-12">Nível de Acesso</label>
                    <select id="swal-user-role" class="swal2-select col-12">
                        <option value="COLLABORATOR" ${user.role === 'COLLABORATOR' ? 'selected' : ''}>Colaborador</option>
                        <option value="ADMIN" ${user.role === 'ADMIN' ? 'selected' : ''}>Administrador</option>
                    </select>
                </div>
            `,
            showCancelButton: true,
            confirmButtonText: 'Salvar',
            preConfirm: () => {
                const data = {
                    name: document.getElementById('swal-user-name').value.trim(),
                    email: document.getElementById('swal-user-email').value.trim(),
                    jobTitle: document.getElementById('swal-user-job').value.trim() || null,
                    role: document.getElementById('swal-user-role').value,
                };
                if (!data.name || !data.email)
                    return Swal.showValidationMessage('Nome e E-mail são obrigatórios.');
                if (!isEdit) {
                    const pass = document.getElementById('swal-user-pass').value;
                    if (!pass || pass.length < 6)
                        return Swal.showValidationMessage('Senha mínima de 6 caracteres.');
                    data.password = pass;
                }
                return data;
            }
        }).then(result => {
            if (result.isConfirmed) handleSaveUser(id, result.value);
        });
    }

    async function handleSaveUser(id, data) {
        const method = id ? 'PATCH' : 'POST';
        const url = id ? `/users/${id}` : '/users';
        try {
            await fetchData(url, { method, body: JSON.stringify(data) });
            Swal.fire('Sucesso!', 'Usuário salvo com sucesso.', 'success');
            loadUsers();
        } catch (error) {
            Swal.fire('Erro!', error.message, 'error');
        }
    }

    function filterUsers() {
        const searchTerm = document.getElementById('search-users').value.toLowerCase().trim();
        const filteredUsers = state.users.filter(user => {
            const username = user.email.split('@')[0];
            return user.name.toLowerCase().includes(searchTerm) ||
                   user.email.toLowerCase().includes(searchTerm) ||
                   username.toLowerCase().includes(searchTerm);
        });

        elements.usersTableBody.innerHTML = '';
        if (filteredUsers.length === 0) {
            renderEmptyRow("Nenhum usuário encontrado.");
            return;
        }

        filteredUsers.forEach(user => {
            const tr = document.createElement('tr');
            const isCurrentUser = user.id === state.currentUser.id;

            const adminIcon = user.role === 'ADMIN'
                ? '<i class="fa-solid fa-circle-check admin-icon yes" title="Administrador"></i>'
                : '<i class="fa-solid fa-circle-xmark admin-icon no" title="Colaborador"></i>';

            const username = user.email.split('@')[0];

            tr.innerHTML = `
                <td>${username}</td>
                <td>${user.email}</td>
                <td>${user.name}</td>
                <td class="text-center">${adminIcon}</td>
                <td class="text-end action-icons">
                    <button class="btn-action edit" data-id="${user.id}" title="Editar">
                        <i class="fa-solid fa-pencil"></i>
                    </button>
                    <button class="btn-action delete" data-id="${user.id}" title="Excluir" ${isCurrentUser ? 'disabled' : ''}>
                        <i class="fa-solid fa-trash-can"></i>
                    </button>
                </td>
            `;
            elements.usersTableBody.appendChild(tr);
        });
    }

    checkAuthentication();
});
