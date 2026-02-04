const nameInput = document.getElementById('item-name');
const descInput = document.getElementById('item-desc');
const addBtn = document.getElementById('add-btn');
const itemList = document.getElementById('item-list');

const API_URL = '/items';

// Fetch and display items on load
async function fetchItems() {
    try {
        const response = await fetch(API_URL);
        const items = await response.json();
        renderList(items);
    } catch (error) {
        console.error('Error fetching items:', error);
    }
}

function renderList(items) {
    itemList.innerHTML = '';
    items.forEach(item => {
        const li = document.createElement('li');
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'item-content';
        
        const nameSpan = document.createElement('span');
        nameSpan.className = 'item-name';
        nameSpan.textContent = item.name;
        
        const descSpan = document.createElement('span');
        descSpan.className = 'item-desc';
        descSpan.textContent = item.description || 'No description';
        
        contentDiv.appendChild(nameSpan);
        contentDiv.appendChild(descSpan);
        
                const deleteBtn = document.createElement('button');
        
                deleteBtn.className = 'delete-btn';
        
                deleteBtn.textContent = 'Delete';
        
                deleteBtn.onclick = () => deleteItem(item.id);
        
        
        
                const updateBtn = document.createElement('button');
        
                updateBtn.className = 'update-btn';
        
                updateBtn.textContent = 'Update';
        
                updateBtn.onclick = () => updateItem(item.id, item.name, item.description);
        
        
        
                li.appendChild(contentDiv);
        
                li.appendChild(updateBtn);
        
                li.appendChild(deleteBtn);
        
                itemList.appendChild(li);
        
            });
        
        }
        
        
        
        async function addItem() {
        
            const name = nameInput.value.trim();
        
            const description = descInput.value.trim();
        
        
        
            if (!name) {
        
                alert('Please enter an item name.');
        
                return;
        
            }
        
        
        
            try {
        
                const response = await fetch(API_URL, {
        
                    method: 'POST',
        
                    headers: {
        
                        'Content-Type': 'application/json'
        
                    },
        
                    body: JSON.stringify({ name, description })
        
                });
        
        
        
                if (response.ok) {
        
                    nameInput.value = '';
        
                    descInput.value = '';
        
                    fetchItems(); // Refresh list
        
                } else {
        
                    console.error('Failed to add item');
        
                }
        
            } catch (error) {
        
                console.error('Error adding item:', error);
        
            }
        
        }
        
        
        
        async function deleteItem(id) {
        
            if (!confirm('Are you sure you want to delete this item?')) return;
        
        
        
            try {
        
                const response = await fetch(`${API_URL}/${id}`, {
        
                    method: 'DELETE'
        
                });
        
        
        
                if (response.ok) {
        
                    fetchItems(); // Refresh list
        
                } else {
        
                    console.error('Failed to delete item');
        
                }
        
            } catch (error) {
        
                console.error('Error deleting item:', error);
        
            }
        
        }
        
        
        
        async function updateItem(id, currentName, currentDescription) {
        
            const name = prompt('Enter new name:', currentName);
        
            const description = prompt('Enter new description:', currentDescription);
        
        
        
            if (!name) {
        
                alert('Please enter an item name.');
        
                return;
        
            }
        
        
        
            try {
        
                const response = await fetch(`${API_URL}/${id}`, {
        
                    method: 'PUT',
        
                    headers: {
        
                        'Content-Type': 'application/json'
        
                    },
        
                    body: JSON.stringify({ name, description })
        
                });
        
        
        
                if (response.ok) {
        
                    fetchItems(); // Refresh list
        
                } else {
        
                    console.error('Failed to update item');
        
                }
        
            } catch (error) {
        
                console.error('Error updating item:', error);
        
            }
        
        }
        
        
        
        addBtn.addEventListener('click', addItem);
        
        
        
        // Initial fetch
        
        fetchItems();
        
        