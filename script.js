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
	const opcodes = unicodeData["paths"][character.codePointAt(0)];
    if (!opcodes) {
        return "Character not found.";
    }

    const inner = unicodeData["initialKeys"][opcodes[0]];
    let result = inner;

    for (let i = 1; i < opcodes.length; i++) {
        const oplist = unicodeData["operations"][opcodes[i]];
        for (let j = 0; j < oplist.length; j++) {
            result = `${oplist[j]}(${result})`
        }
    }

    result = `chr(${result})`
	return result ? result : "Generation script not found.";
}

document.getElementById("unicodeInput").addEventListener("input", function () {
	const character = this.value.trim();
	const resultElement = document.getElementById("result");
	const resultScript = document.getElementById("resultScript");
	const resultSection = document.getElementById("resultSection");

	if (character) {
		const script = lookupUnicode(character);
		resultElement.textContent = `"${String.fromCodePoint(
			character.codePointAt(0)
		)}":`;
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
		className: "toast-warning",
	}).showToast();
}
function successToast(message) {
	Toastify({
		text: message,
		duration: 3000,
		className: "toast-success",
	}).showToast();
}

document.getElementById("copyButton").addEventListener("click", function () {
	const textToCopy = document.querySelector("#resultScript").innerText;

	navigator.clipboard
		.writeText(textToCopy)
		.then(() => {
			successToast("Copied to clipboard");
		})
		.catch((err) => {
			warningToast("Error copying to clipboard");
		});
});
