// Code is very dry and repeated.
// Look into consolidating into a few methods when time permits.
const webPrefix = window.location.href.split('/').slice(0, 3).join('/');

const seriesAutocompleteRequestUrl = `${webPrefix}/autocomplete/series?search_text=`;
const characterAutocompleteRequestUrl = `${webPrefix}/autocomplete/character?search_text=`;

const characterSeriesInput = document.querySelector('#id_character_series');
const characterSeriesIdInput = document.querySelector('#id_character_series_id');

const totalForms = document.querySelector("#id_relations-form-TOTAL_FORMS");
const totalReferenceForms = document.querySelector("#id_references-form-TOTAL_FORMS");

const addRelationFormBtn = document.querySelector("#add-relation-form");
const addReferenceFormBtn = document.querySelector("#add-reference-form");

const relationForm = document.getElementsByClassName("relation-form");
const referenceForm = document.getElementsByClassName("reference-form");
const characterForm = document.querySelector("#new_character_form") || document.querySelector("#update_character_form");

let relationsFormCount = relationForm.length - 1;
let referencesFormCount = referenceForm.length - 1;

const relationFormInput = relationForm[0].querySelector('#id_relations-form-0-character_name');
const relationFormIdInput = relationForm[0].querySelector('#id_relations-form-0-character_id');

// Dry. Fix later.
relationFormInput.addEventListener('input', (e) => {handleKeypress(e.target.value, relationFormInput, relationFormIdInput, characterAutocompleteRequestUrl, 'character')});

const createAutocompleteRow = (formField, formIdField, text, id) => {
	const newDiv = document.createElement("div");

	const textContent = document.createTextNode(text);

	newDiv.appendChild(textContent);
	newDiv.addEventListener('click', (event) => {
		formField.value = text;
		formIdField.value = id;
	});

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


const handleKeypress = debounce(async (str, inputElement, hiddenIdElement, requestUrl, type) => {

	const autocompleteRequest = `${requestUrl}${str}`;
	
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
	let autocompleteSuggest;
	if(type === 'series') {
		autocompleteSuggest = [...response.series].map(m => createAutocompleteRow(inputElement, hiddenIdElement, m.name, m.id));
	} else if (type === 'character') {
		autocompleteSuggest = [...response.character].map(m => createAutocompleteRow(inputElement, hiddenIdElement, m.name, m.id));
	}
	const autocompleteList = document.createElement('div');
	autocompleteList.classList.add('autocomplete');

	autocompleteSuggest.forEach((item) => {
		autocompleteList.appendChild(item);	
	});

	// instead of clobbering the div entirely, just replace the content.
	if(inputElement.nextSibling) {
		inputElement.nextSibling.innerHTML = '';
		inputElement.parentNode.insertBefore(autocompleteList, inputElement.nextSibling);
	} else {
		inputElement.parentNode.insertBefore(autocompleteList, inputElement.nextSibling);
	}

}, 500);

characterSeriesInput.addEventListener("input", (event) => { 
	handleKeypress(event.target.value, characterSeriesInput, characterSeriesIdInput, seriesAutocompleteRequestUrl, 'series');
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

	const newFormInput = newRelationForm.querySelector(`#id_relations-form-${relationsFormCount}-character_name`);
	const newFormHiddenIdInput = newRelationForm.querySelector(`#id_relations-form-${relationsFormCount}-character_id`);

	newFormInput.addEventListener('input', (e) => {handleKeypress(e.target.value, newFormInput, newFormHiddenIdInput, characterAutocompleteRequestUrl, 'character')});

	characterForm.insertBefore(newRelationForm, addRelationFormBtn);

	totalForms.setAttribute('value', `${relationsFormCount + 1}`);
});

const deleteRelationElement = (button) => {
	if(relationsFormCount > 0){
		button.parentElement.parentElement.remove();
		relationsFormCount--;
		totalForms.setAttribute('value', `${relationsFormCount + 1}`);
		updateRelationsForms();
	}
}

const deleteReferenceElement = (button) => {
	if(referencesFormCount > 0){
		button.parentElement.remove();
		referencesFormCount--;
		totalReferenceForms.setAttribute('value', `${referencesFormCount + 1}`);
		updateReferencesForms();
	}
}

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

const previewImage = (input) => {
	if(input.files && input.files[0]) {
		const reader = new FileReader();

		reader.onload = (e) => {
			document.querySelector('#character-upload-thumb').setAttribute('src', e.target.result);
		}

		reader.readAsDataURL(input.files[0]);
	}

}
