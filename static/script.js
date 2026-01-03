const fetchBtn = document.getElementById('fetch-btn');
const messageContainer = document.getElementById('message-container');

fetchBtn.addEventListener('click', async () => {
    try {
        const response = await fetch('/api');
        const data = await response.json();
        messageContainer.textContent = data.message;
    } catch (error) {
        console.error('Error fetching message:', error);
        messageContainer.textContent = 'Error fetching message.';
    }
});