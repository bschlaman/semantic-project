window.onload = () => {

	let wordPairId;

	// get words at window load, and subsequently after each put req
	getWords().then(id => { wordPairId = id });

	const ssButtons = document.querySelectorAll(".buttons-container button");
	ssButtons.forEach(button => {
		button.onclick = _ => {
			// wordPairId might be undefined
			if (wordPairId == null) return;
			// this is dangerous, what if parseInt fails?
			putWords(wordPairId, parseInt(button.dataset.val));
			getWords().then(id => { wordPairId = id });
		}
	});

	document.addEventListener('keydown', (e) => {
		switch (e.code) {
			case "KeyA":
			case "Digit0":
			case "Numpad0": ssButtons[0].click(); break;
			case "KeyS":
			case "Digit1":
			case "Numpad1": ssButtons[1].click(); break;
			case "KeyD":
			case "Digit2":
			case "Numpad2": ssButtons[2].click(); break;
			case "KeyF":
			case "Digit3":
			case "Numpad3": ssButtons[3].click(); break;
			case "KeyG":
			case "Digit4":
			case "Numpad4": ssButtons[4].click(); break;
			default: return;
		}
	});
}

function getWords() {
	const word1 = document.querySelector(".words-container .word1");
	const word2 = document.querySelector(".words-container .word2");
	return fetch("/get_words", { method: "GET" })
		.then(res => res.json())
		.then(data => {
			console.log(data);
			word1.innerHTML = data.word1;
			word2.innerHTML = data.word2;
			return data.id;
		})
		.catch(err => {
			console.log("error occured:", err);
			return undefined;
		});
}

function putWords(wordPairId, semSimilarity) {
	if (wordPairId == null) return;
	console.log(`assigning sem_similarity: ${semSimilarity}`);
	fetch("/put_words", {
		method: "PUT",
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
			id:             wordPairId,
			sem_similarity: semSimilarity,
		}),
	});
}
