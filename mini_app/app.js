// Инициализация Telegram Web App
const tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

// Состояние
let currentCharacter = null;
const API_URL = 'http://localhost:8000'; // Заменить на реальный URL после деплоя

// DOM-элементы
const catalogScreen = document.getElementById('catalog-screen');
const chatScreen = document.getElementById('chat-screen');
const catalogDiv = document.getElementById('catalog');
const searchInput = document.getElementById('search');
const messagesDiv = document.getElementById('messages');
const msgInput = document.getElementById('msg-input');
const sendBtn = document.getElementById('send-btn');
const backBtn = document.getElementById('back-btn');
const chatAvatar = document.getElementById('chat-avatar');
const chatName = document.getElementById('chat-name');

// Загрузка каталога персонажей с API
async function loadCatalog(filter = '') {
    try {
        const res = await fetch(`${API_URL}/characters/list`);
        let characters = await res.json();
        
        if (filter) {
            characters = characters.filter(c => 
                c.name.toLowerCase().includes(filter.toLowerCase()) ||
                c.tags.toLowerCase().includes(filter.toLowerCase())
            );
        }
        
        renderCatalog(characters);
    } catch (err) {
        console.error('Ошибка загрузки:', err);
        // Если API недоступен — показываем заглушку
        renderCatalog(getFallbackCharacters().filter(c => 
            c.name.toLowerCase().includes(filter.toLowerCase())
        ));
    }
}

function getFallbackCharacters() {
    return [
        { id: "yuki", name: "Юки-онна", tags: "дух, снег, поэзия", avatar_url: "https://i.imgur.com/8M3Kt6s.png" },
        { id: "rex", name: "Рекс", tags: "киберпёс, боевой", avatar_url: "https://i.imgur.com/vJmQo9n.png" },
    ];
}

function renderCatalog(characters) {
    catalogDiv.innerHTML = '';
    characters.forEach(c => {
        const card = document.createElement('div');
        card.className = 'character-card';
        card.innerHTML = `
            <img src="${c.avatar_url || 'https://via.placeholder.com/200'}" 
                 alt="${c.name}" 
                 onerror="this.src='https://via.placeholder.com/200'">
            <div class="name">${c.name}</div>
            <div class="tags">${c.tags}</div>
        `;
        card.addEventListener('click', () => openChat(c));
        catalogDiv.appendChild(card);
    });
}

// Открытие чата
function openChat(character) {
    currentCharacter = character;
    chatAvatar.src = character.avatar_url || 'https://via.placeholder.com/200';
    chatName.textContent = character.name;
    
    messagesDiv.innerHTML = `
        <div class="msg character">
            Привет! Я ${character.name}. О чём хочешь поговорить?
        </div>
    `;
    
    catalogScreen.classList.add('hidden');
    chatScreen.classList.remove('hidden');
    msgInput.focus();
}

// Закрытие чата
function closeChat() {
    currentCharacter = null;
    chatScreen.classList.add('hidden');
    catalogScreen.classList.remove('hidden');
    loadCatalog(searchInput.value);
}

// Отправка сообщения
async function sendMessage() {
    const text = msgInput.value.trim();
    if (!text || !currentCharacter) return;
    
    // Добавляем сообщение пользователя
    addMessage('user', text);
    msgInput.value = '';
    
    // Показываем индикатор печати
    const typingMsg = addMessage('character', '...', true);
    
    try {
        // Отправляем в API
        const res = await fetch(`${API_URL}/chat/send`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: tg.initDataUnsafe?.user?.id || 0,
                character_id: currentCharacter.id,
                message: text
            })
        });
        
        const data = await res.json();
        
        // Убираем индикатор печати
        typingMsg.remove();
        
        // Добавляем ответ
        addMessage('character', data.reply);
        
    } catch (err) {
        typingMsg.remove();
        addMessage('character', '*молчание*... Не могу связаться с сервером.');
        console.error(err);
    }
}

function addMessage(role, text, isTyping = false) {
    const msg = document.createElement('div');
    msg.className = `msg ${role}`;
    if (isTyping) msg.classList.add('typing');
    msg.textContent = text;
    messagesDiv.appendChild(msg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    return msg;
}

// События
sendBtn.addEventListener('click', sendMessage);
msgInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') sendMessage();
});
backBtn.addEventListener('click', closeChat);
searchInput.addEventListener('input', (e) => loadCatalog(e.target.value));

// Старт
loadCatalog();