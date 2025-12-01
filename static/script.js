function addMessage(text, sender) {
    const chatbox = document.getElementById("chatbox");
    const bubble = document.createElement("div");

    bubble.className = sender === "user" ? "userMsg" : "botMsg";
    bubble.textContent = text;

    chatbox.appendChild(bubble);
    chatbox.scrollTop = chatbox.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById("userInput");
    const text = input.value.trim();
    if (!text) return;

    input.value = "";
    addMessage(text, "user");

    // Calculator trigger
    if (text.toLowerCase().includes("calculator")) {
        openCalculator();
        return;
    }

    document.getElementById("typingIndicator").style.display = "block";

    const res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: text })
    });

    const data = await res.json();
    document.getElementById("typingIndicator").style.display = "none";

    if (data.reply === "__open_calculator__") {
        openCalculator();
        return;
    }

    addMessage(data.reply, "bot");
}

/* ======== CALCULATOR ======== */

function openCalculator() {
    const modal = document.getElementById("calcModal");
    modal.style.display = "flex";
    buildCalculator();
}

document.getElementById("closeCalc").onclick = () => {
    document.getElementById("calcModal").style.display = "none";
};

let calcExpr = "";

function buildCalculator() {
    const buttons = document.getElementById("calcButtons");
    buttons.innerHTML = "";

    const keys = ["7","8","9","/","4","5","6","*","1","2","3","-","0",".","=","+"];

    keys.forEach(k => {
        let btn = document.createElement("button");
        btn.className = "calcBtn";
        btn.textContent = k;

        btn.onclick = () => {
            const disp = document.getElementById("calcDisplay");

            if (k === "=") {
                try {
                    calcExpr = eval(calcExpr).toString();
                    disp.value = calcExpr;
                } catch {
                    disp.value = "Error";
                    calcExpr = "";
                }
            } else {
                calcExpr += k;
                disp.value = calcExpr;
            }
        };

        buttons.appendChild(btn);
    });
}

/* ======== Voice input ======== */

function startVoice() {
    let recog = new webkitSpeechRecognition();
    recog.lang = "en-US";
    recog.start();

    recog.onresult = function(e) {
        let text = e.results[0][0].transcript;
        document.getElementById("userInput").value = text;
        sendMessage();
    };
}
