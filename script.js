let unicodeData = null;

const inverseCharmap = {
	A: "000000",
	B: "000001",
	C: "000010",
	D: "000011",
	E: "000100",
	F: "000101",
	G: "000110",
	H: "000111",
	I: "001000",
	J: "001001",
	K: "001010",
	L: "001011",
	M: "001100",
	N: "001101",
	O: "001110",
	P: "001111",
	Q: "010000",
	R: "010001",
	S: "010010",
	T: "010011",
	U: "010100",
	V: "010101",
	W: "010110",
	X: "010111",
	Y: "011000",
	Z: "011001",
	a: "011010",
	b: "011011",
	c: "011100",
	d: "011101",
	e: "011110",
	f: "011111",
	g: "100000",
	h: "100001",
	i: "100010",
	j: "100011",
	k: "100100",
	l: "100101",
	m: "100110",
	n: "100111",
	o: "101000",
	p: "101001",
	q: "101010",
	r: "101011",
	s: "101100",
	t: "101101",
	u: "101110",
	v: "101111",
	w: "110000",
	x: "110001",
	y: "110010",
	z: "110011",
	0: "110100",
	1: "110101",
	2: "110110",
	3: "110111",
	4: "111000",
	5: "111001",
	6: "111010",
	7: "111011",
	8: "111100",
	9: "111101",
	"+": "111110",
	"/": "111111",
};

const inverseSemiCharmap = {
	"000": "0",
	"001": "1",
	"010": "2",
	"011": "3",
	"100": "4",
	"101": "5",
	"110": "6",
    "111": "",
};

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

		const paths = {};
		const splitPaths = json["paths"].split(",");
		let index = 0;

		for (let i = 0; i < splitPaths.length; i++) { // splitPaths.length
			const value = splitPaths[i];

			if (!isNaN(parseInt(value))) {
				index += parseInt(value);
			} else {
                let newValue = ""
                newValue += value.charAt(0);

                for (let j = 1; j < value.length; j++) {
                    const inverse = inverseCharmap[value[j]];
                    const left = inverse.slice(0, 3);
                    const right = inverse.slice(3, 6);
                    newValue += inverseSemiCharmap[left] + inverseSemiCharmap[right];
                }
                
                paths[index.toString()] = newValue;

				index += 1;
			}
		}

		json["paths"] = paths;

		unicodeData = json;

        console.log("Data loaded")
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

	const inner = unicodeData["initialKeys"][opcodes.charAt(0)];
	let result = inner;

	const outer = opcodes.split("");
	outer.shift();

	for (let i = 0; i < outer.length; i++) {
		const oplist = unicodeData["operations"][outer[i]];
		for (let j = 0; j < oplist.length; j++) {
			result = `${oplist[j]}(${result})`;
		}
	}

	result = `chr(${result})`;
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
