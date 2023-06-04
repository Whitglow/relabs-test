const messageListElement = document.getElementById("messageList");
const messageForm = document.getElementById("messageForm");
const messageTextArea = document.getElementById("message");

const ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = handleMessage;

messageForm.onsubmit = (e) => {
    e.preventDefault();
    const message = messageTextArea.value;
    ws.send(JSON.stringify(message));
    messageTextArea.value = "";
};

function handleMessage(e) {
    const messages = JSON.parse(e.data);
    messageListElement.innerHTML = "";
    for (const message of messages) {
        const listItem = document.createElement("li");
        listItem.textContent = message;
        messageListElement.appendChild(listItem);
    }
}

window.addEventListener('beforeunload', async function() {
  await fetch('/clear_messages', { method: 'POST' });
});

window.addEventListener('unload', async function() {
  await fetch('/clear_messages', { method: 'POST' });
});