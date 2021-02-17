// Code is very dry and repeated.
// Look into consolidating into a few methods when time permits.
const webPrefix = window.location.href.split('/').slice(0, 3).join('/');

const characterSeriesInput = document.querySelector('#id_character_series');
const characterSeriesIdInput = document.querySelector('#id_character_series_id');

const totalForms = document.querySelector("#id_relations-form-TOTAL_FORMS");
const totalReferenceForms = document.querySelector("#id_references-form-TOTAL_FORMS");

const addRelationFormBtn = document.querySelector("#add-relation-form");
const addReferenceFormBtn = document.querySelector("#add-reference-form");

const relationForm = document.getElementsByClassName("relation-form");
const referenceForm = document.getElementsByClassName("reference-form");
const characterForm = document.querySelector("#new_character_form");

let relationsFormCount = relationForm.length - 1;
let referencesFormCount = referenceForm.length - 1;

const createAutocompleteRow = (formField, formIdField, text, id) => {
	const newDiv = document.createElement("div");

	const textContent = document.createTextNode(text);

	newDiv.appendChild(textContent);
	console.log('Adding event listener!');
	newDiv.addEventListener('click', (event) => {
		formField.value = text;
		formIdField.value = id;
		console.log(formField);
		console.log('Clicked!', id);
	});
	console.log(newDiv);

	return newDiv;
}

let seriesAutocompleteSuggest = [];

function debounce (callback, wait) {
	let timeout;
	return function() {
		clearTimeout(timeout);
		timeout = setTimeout(() => callback.apply(this, arguments), wait)
	}
}

const handleKeypress = debounce(async (str) => {

	const autocompleteRequest = `${webPrefix}/autocomplete/series?search_text=${str}`;
	
	const response = await fetch(autocompleteRequest, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		}
		}
	).then(result => {
		return result.json();
	})

	// doing too many things. Break out into separate functions.
	seriesAutocompleteSuggest = [...response.series].map(m => createAutocompleteRow(characterSeriesInput, characterSeriesIdInput, m.name, m.id));
	const autocompleteList = document.createElement('div');

	seriesAutocompleteSuggest.forEach((item) => {
		autocompleteList.appendChild(item);	
	});

	// instead of clobbering the div entirely, just replace the content.
	if(characterSeriesInput.nextSibling) {
		characterSeriesInput.nextSibling.innerHTML = '';
		characterSeriesInput.parentNode.insertBefore(autocompleteList, characterSeriesInput.nextSibling);
	} else {
		characterSeriesInput.parentNode.insertBefore(autocompleteList, characterSeriesInput.nextSibling);
	}

}, 500);

characterSeriesInput.addEventListener("input", (event) => { 
	handleKeypress(event.target.value);
});

addReferenceFormBtn.addEventListener("click", (evt) => {
	evt.preventDefault();

	const newReferenceForm = referenceForm[0].cloneNode(true);
	const formRegex = RegExp(`form-(\\d){1}-`, 'g');
	referencesFormCount++;

	newReferenceForm.innerHTML = newReferenceForm.innerHTML.replace(formRegex, `form-${referencesFormCount}-`);

	characterForm.insertBefore(newReferenceForm, addReferenceFormBtn);

	totalReferenceForms.setAttribute('value', `${referencesFormCount + 1}`);
});

addRelationFormBtn.addEventListener("click", (evt) => {
	evt.preventDefault();

	const newRelationForm = relationForm[0].cloneNode(true);

	const formRegex = RegExp(`form-(\\d){1}-`, 'g');
	relationsFormCount++;

	newRelationForm.innerHTML = newRelationForm.innerHTML.replace(formRegex, `form-${relationsFormCount}-`);

	characterForm.insertBefore(newRelationForm, addRelationFormBtn);

	totalForms.setAttribute('value', `${relationsFormCount + 1}`);
});

characterForm.addEventListener("click", (evt) => {
	if (evt.target.classList.contains("delete-relation-form") && (relationsFormCount > 0)){
		evt.preventDefault();
		evt.target.parentElement.remove();
		relationsFormCount--;
		totalForms.setAttribute('value', `${relationsFormCount + 1}`);
		updateRelationsForms();
	} else if (evt.target.classList.contains("delete-reference-form") && (referencesFormCount > 0)){
		evt.preventDefault();
		evt.target.parentElement.remove();
		referencesFormCount--;
		totalReferenceForms.setAttribute('value', `${referencesFormCount + 1}`);
		updateReferencesForms();
	}
});

const updateRelationsForms = () => {
	let count = 0;
	for (let form of relationForm) {
		const formRegex = RegExp(`form-(\\d){1}-`, 'g');
		form.innerHTML = form.innerHTML.replace(formRegex, `form-${count++}-`);
	}
}

const updateReferencesForms = () => {
	let count = 0;
	for (let form of referenceForm) {
		const formRegex = RegExp(`form-(\\d){1}-`, 'g');
		form.innerHTML = form.innerHTML.replace(formRegex, `form-${count++}-`);
	}
}
