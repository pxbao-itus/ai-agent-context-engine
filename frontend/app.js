document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const queryForm = document.getElementById('query-form');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const logList = document.getElementById('log-list');

    // Modal elements
    const modalOverlay = document.getElementById('modal-overlay');
    const modalTitle = document.getElementById('modal-title');
    const modalContent = document.getElementById('modal-content');
    const closeModal = document.getElementById('close-modal');

    function addMessage(text, isUser = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isUser ? 'user-msg' : 'ai-msg'}`;

        // Handle markdown-like line breaks
        const formattedText = text.replace(/\n\n/g, '<br><br>').replace(/\n/g, '<br>');

        msgDiv.innerHTML = `
            <div class="msg-content">
                ${formattedText}
            </div>
        `;

        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addLog(logObj) {
        // Remove empty state
        const empty = logList.querySelector('.empty-state');
        if (empty) empty.remove();

        const logDiv = document.createElement('div');
        logDiv.className = `log-entry ${logObj.step.toLowerCase()}`;

        const time = new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });

        logDiv.innerHTML = `
            <span class="log-header">[${time}] ${logObj.step.toUpperCase()}</span>
            ${logObj.message}
            ${logObj.detail ? '<div style="font-size: 0.65rem; color: #94a3b8; margin-top: 4px;">📂 Click to view detail</div>' : ''}
        `;

        if (logObj.detail) {
            logDiv.onclick = () => showModal(logObj.step, logObj.detail);
        }

        logList.appendChild(logDiv);
        logList.scrollTop = logList.scrollHeight;
    }

    function showModal(step, content) {
        modalTitle.innerText = `${step} Details`;
        modalContent.innerText = content;
        modalOverlay.classList.remove('hidden');
    }

    function hideModal() {
        modalOverlay.classList.add('hidden');
    }

    closeModal.onclick = hideModal;
    modalOverlay.onclick = (e) => { if (e.target === modalOverlay) hideModal(); };

    async function handleQuery(e) {
        e.preventDefault();
        const query = userInput.value.trim();
        if (!query) return;

        userInput.value = '';
        userInput.disabled = true;
        sendBtn.disabled = true;

        addMessage(query, true);

        try {
            const response = await fetch('/api/v1/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });

            const data = await response.json();

            if (response.ok) {
                // Display all logs returned from the engine
                data.logs.forEach((log, index) => {
                    setTimeout(() => addLog(log), index * 400);
                });

                setTimeout(() => {
                    addMessage(data.answer);
                }, (data.logs.length + 1) * 400);
            } else {
                addMessage(`Error: ${data.detail || 'Failed to get response'}`, false);
            }
        } catch (err) {
            addMessage(`Critical Error: ${err.message}`, false);
        } finally {
            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus();
        }
    }

    queryForm.addEventListener('submit', handleQuery);
});
