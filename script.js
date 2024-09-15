let unicodeData = null;

async function loadJSON() {
	try {
		const response = await fetch("output.json", {
			headers: {
				Accept: "application/json",
			},
		});

		if (!response.ok) {
			throw new Error("Failed to fetch the compressed JSON");
		}

		const json = await response.json();

        unicodeData = json;
	} catch (error) {
		document.getElementById("result").textContent =
			"Error loading JSON: " + error.message;
	}
}

loadJSON();

function lookupUnicode(character) {
	console.log(character);
	const result = unicodeData[character.codePointAt(0)].toString();
	console.log(character.charCodeAt(0));
	console.log(result);
	return result ? result : "Generation script not found.";
}

document.getElementById("unicodeInput").addEventListener("input", function () {
	const character = this.value.trim();
	const resultElement = document.getElementById("result");
	const resultScript = document.getElementById("resultScript");
    const resultSection = document.getElementById("resultSection");

	if (character) {
		const script = lookupUnicode(character);
		resultElement.textContent = `"${String.fromCodePoint(character.codePointAt(0))}":`;
		resultScript.textContent = script;
		resultScript.style.display = "block";
        resultSection.style.display = "block";
	} else {
		resultElement.textContent = "";
		resultScript.textContent = "";
		resultScript.style.display = "none";
        resultSection.style.display = "none";
	}
});

function warningToast(message) {
    Toastify({
        text: message,
        duration: 3000,
        className: 'toast-warning'
    }).showToast();
}
function successToast(message) {
    Toastify({
        text: message,
        duration: 3000,
        className: 'toast-success'
    }).showToast();
}

document.getElementById("copyButton").addEventListener("click", function () {
    const textToCopy = document.querySelector('#resultScript').innerText;
    
    navigator.clipboard.writeText(textToCopy).then(() => {
        successToast('Copied to clipboard');
    }).catch(err => {
        warningToast('Error copying to clipboard');
    });
});