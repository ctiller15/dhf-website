// Code is very dry and repeated.
// Look into consolidating into a few methods when time permits.

const totalForms = document.querySelector("#id_relations-form-TOTAL_FORMS");
const totalReferenceForms = document.querySelector("#id_references-form-TOTAL_FORMS");

const addRelationFormBtn = document.querySelector("#add-relation-form");
const addReferenceFormBtn = document.querySelector("#add-reference-form");

const relationForm = document.getElementsByClassName("relation-form");
const referenceForm = document.getElementsByClassName("reference-form");
const characterForm = document.querySelector("#new_character_form");

let relationsFormCount = relationForm.length - 1;
let referencesFormCount = referenceForm.length - 1;

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
