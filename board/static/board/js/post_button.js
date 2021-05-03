async function gameState(btnSate) {
    var btnAdded = document.getElementById('btn-must-added');
    if (btnSate) {
        btnAdded.style.display = 'inline-block';
    } else {
        btnAdded.style.display = 'none';
    }
}

async function sendForm(url, game_id, method) {
    let gama_data = {
        game_id: game_id
    };

    await fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify(gama_data)
    });
}

function changeMe(btnSate, game_id) {
    btnName = document.getElementById('btn-must');
    if (btnSate) {
        btnName.innerHTML = 'MUST';
        sendForm(url, game_id, 'DELETE');
        btnSate = false;
    } else {
        btnName.innerHTML = 'REMOVE';
        sendForm(url, game_id, 'POST');
        btnSate = true;
    }
}
