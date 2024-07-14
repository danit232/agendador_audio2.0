function handleFormSubmit(event, chat_id) {
    event.preventDefault();
    sendMessage(chat_id);
}

function inicializarChat(chat_id) {
    console.log("Inicializando eventos del chat...");

    const promptForm = findElementByClassAndDataChatNumber('chat-form', chat_id);
    console.log("Formulario encontrado:", promptForm);
    if (promptForm) {
        promptForm.addEventListener("submit", (event) => handleFormSubmit(event, chat_id));

        promptForm.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();
                sendMessage(chat_id);
            }
        });
    } else {
        console.error("El formulario 'promptForm' no se encontró en el DOM.");
    }

    const clearButton = document.querySelector(`.btn-clear[data-chat-number="${chat_id}"]`);
    console.log("Botón de limpieza encontrado:", clearButton);
    if (clearButton) {
        clearButton.addEventListener("click", () => resetConversation(chat_id));
    } else {
        console.error("El botón 'btn-clear' no se encontró en el DOM.");
    }
}

function cargarChat(id, training_prompt) {
    const url = `chat-container-${id}.html`
    var chat_id = id;

    conversations[chat_id] = [
        { role: "system", content: training_prompt }
    ];

    const chatContainer = findElementByClassAndDataChatNumber('chat-box', chat_id);

    fetch(url)
        .then(response => response.text())
        .then(html => {
            chatContainer.innerHTML = html;

            addDataChatNumber(chatContainer, chat_id);

            inicializarChat(chat_id);

            const foundElement = findElementByClassAndDataChatNumber('chat-messages', chat_id);
            if (foundElement) {
                console.log('Elemento encontrado:', foundElement);
            } else {
                console.log('Elemento no encontrado.');
            }
            renderConversationHistory(chat_id);

            // Add toggle functionality here
            const toggleHistoryBtn = document.getElementById('toggleHistory');
            const chatHistory = document.getElementById('chatHistory');

            console.log("Toggle button:", toggleHistoryBtn);
            console.log("Chat history:", chatHistory);

            if (toggleHistoryBtn && chatHistory) {
                toggleHistoryBtn.addEventListener('click', function() {
                    console.log("Toggle button clicked");
                    chatHistory.classList.toggle('show');
                    
                    if (chatHistory.classList.contains('show')) {
                        chatHistory.style.display = 'block';
                        setTimeout(() => chatHistory.classList.add('show'), 500);
                        toggleHistoryBtn.textContent = 'Ocultar historial';
                    } else {
                        chatHistory.classList.remove('show');
                        setTimeout(() => chatHistory.style.display = 'none', 500);
                        toggleHistoryBtn.textContent = 'Mostrar historial';
                    }
                });
            } else {
                console.error("Toggle button or chat history not found");
            }
        })
        .catch(error => console.error('Error al cargar el chat:', error));
}

document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM fully loaded");

    cargarChat('1', training_prompt);
    cargarChat('2', training_prompt);
});
function addDataChatNumber(container, chat_id) {
    const elements = container.querySelectorAll('*');
    elements.forEach(element => {
        element.setAttribute('data-chat-number', chat_id);
    });
}

function renderConversationHistory(chat_id) {
    function speakText(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'es-US';
    
            const voices = speechSynthesis.getVoices();
            const selectedVoice = voices.find(voice => voice.name === 'es-US-Neural2-A');
            if (selectedVoice) {
                utterance.voice = selectedVoice;
            }
    
            const profileBubble = document.getElementById('profileBubble');

            utterance.onstart = function(event) {
                profileBubble.classList.add('speaking');
            };

            utterance.onend = function(event) {
                profileBubble.classList.remove('speaking');
            };

            speechSynthesis.speak(utterance);
        } else {
            console.log('Text-to-speech not supported in this browser.');
        }
    }
    
    const voices = speechSynthesis.getVoices();
    voices.forEach(voice => {
        console.log(voice.name, voice.lang);
    });

    document.getElementById(`sendButton`).addEventListener('click', function () {
        sendMessage(chat_id);
    });

    const btnToggle = document.getElementById(`btnToggle`);
    const textArea = findElementByClassAndDataChatNumber('form-control', chat_id);
    const userWaveContainer = document.querySelector('.user-wave-container');


    const recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.lang = 'es-ES';
    recognition.interimResults = false;

    let isRecording = false;
    let finalTranscript = '';
    let silenceTimer;
    const silenceThreshold = 3000; // 1.5 segundos de silencio
    const sendDelay = 500; // 0.5 segundos de espera antes de enviar


    btnToggle.addEventListener('click', () => {
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
    });

    function startRecording() {
        recognition.start();
        btnToggle.classList.add('active');
        userWaveContainer.classList.add('speaking');
        isRecording = true;
        finalTranscript = '';
    }


    function stopRecording() {
        recognition.stop();
        btnToggle.classList.remove('active');
        userWaveContainer.classList.remove('speaking');
        isRecording = false;
        
        // Esperar un poco antes de enviar el mensaje
        setTimeout(() => {
            textArea.value = finalTranscript.trim();
            if (textArea.value) {
                sendMessage(chat_id);
            }
        }, sendDelay);
    }

    function resetSilenceTimer() {
        clearTimeout(silenceTimer);
        silenceTimer = setTimeout(() => {
            if (isRecording) {
                stopRecording();
            }
        }, silenceThreshold);
    }

    recognition.onresult = (event) => {
        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
            } else {
                interimTranscript += transcript;
            }
        }
        textArea.value = finalTranscript + interimTranscript;
        resetSilenceTimer();
    };


    recognition.onaudiostart = () => {
        resetSilenceTimer();
    };

    recognition.onaudioend = () => {
        clearTimeout(silenceTimer);
    };

    recognition.onend = () => {
        if (isRecording) {
            recognition.start();
        } else {
            setTimeout(() => {
                if (textArea.value.trim()) {
                    sendMessage(chat_id);
                }
            }, sendDelay);
        }
    };


    let conversationElement = findElementByClassAndDataChatNumber('chat-messages', chat_id);
    if (conversationElement) {
        conversationElement.innerHTML = '';
    } else {
        console.error("El elemento 'apiResponse' no se encontró en el DOM.");
    }

    conversations[chat_id].filter(message => message.role !== "system").forEach((message, index, array) => {
        let messageElement = document.createElement("div");
        messageElement.classList.add('message-bubble');
        messageElement.classList.add(message.role === "user" ? "user" : "assistant");

        if (message.content.startsWith("escribiendo")) {
            messageElement.classList.add("writing");
        }

        messageElement.innerText = message.content;
        conversationElement.appendChild(messageElement);

        if (index === array.length - 1 && message.role === "assistant" && !message.content.startsWith("escribiendo")) {
            speakText(message.content);
        }
    });

    let lastMessageElement = conversationElement.lastChild;
    if (lastMessageElement) {
        lastMessageElement.scrollIntoView({ behavior: 'smooth' });
    }
}

function resetConversation(chat_id) {
    findElementByClassAndDataChatNumber('form-control', chat_id).value = '';
    findElementByClassAndDataChatNumber('chat-messages', chat_id).innerHTML = '';
    conversations[chat_id] = [{ role: "system", content: training_prompt }];
    renderConversationHistory(chat_id);
}

function sendMessage(chat_id) {
    let userPrompt = findElementByClassAndDataChatNumber('form-control', chat_id).value.trim();
    if (userPrompt === '') return;

    conversations[chat_id].push({ role: "user", content: userPrompt });
    renderConversationHistory(chat_id);

    let dots = "";
    let writingIndex = conversations[chat_id].length;
    conversations[chat_id].push({ role: "assistant", content: `escribiendo${dots}` });
    renderConversationHistory(chat_id);

    let writingInterval = setInterval(() => {
        dots = dots.length < 3 ? dots + "." : "";
        conversations[chat_id][writingIndex] = { role: "assistant", content: `escribiendo${dots}` };
        renderConversationHistory(chat_id);
    }, 500);

    findElementByClassAndDataChatNumber('form-control', chat_id).value = '';

    let dataToSend = {
        messages: conversations[chat_id].slice(0, -1)
    };

    fetch(URL_BASE, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'Psico-API-Key': '94705224-bhvg-4745-mac7-f15c455858f4'
        },
        body: JSON.stringify(dataToSend)
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(writingInterval);
        conversations[chat_id].splice(writingIndex, 1);
        if (!conversations[chat_id].find(m => m.content === data.response)) {
            conversations[chat_id].push({ role: "assistant", content: data.response });
        }
        renderConversationHistory(chat_id);
    })
    .catch((error) => {
        clearInterval(writingInterval);
        console.error('Error:', error);
        conversations[chat_id].splice(writingIndex, 1);
        conversations[chat_id].push({ role: "assistant", content: `Error: ${error}` });
        renderConversationHistory(chat_id);
    });
}

function findElementByClassAndDataChatNumber(className, dataChatNumber) {
    const selector = `.${className}[data-chat-number="${dataChatNumber}"]`;
    const element = document.querySelector(selector);
    return element;
}

var conversations = {};
const URL_BASE = "http://127.0.0.1:8000/chatgpt";
const training_prompt = `Eres Emilio Einstein, una mezcla entre un matemático puro y Albert`;

document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM fully loaded");

    cargarChat('1', training_prompt);
    cargarChat('2', training_prompt);
});