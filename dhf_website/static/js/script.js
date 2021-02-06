const totalForms = document.querySelector("#id_form-TOTAL_FORMS");
console.log(totalForms);

const addRelationFormBtn = document.querySelector("#add-relation-form");
const submitbutton = document.querySelector('[type="submit"]');

const relationForm = document.getElementsByClassName("relation-form");
const characterForm = document.querySelector("#new_character_form");

let relationFormCount = relationForm.length - 1;

addRelationFormBtn.addEventListener("click", (evt) => {
	evt.preventDefault();

	const newRelationForm = relationForm[0].cloneNode(true);
	const newRelationFormSummary = relationForm[1].cloneNode(true);

	const formRegex = RegExp(`form-(\\d){1}-`, 'g');
	relationFormCount++;

	newRelationForm.innerHtml = newRelationForm.innerHTML.replace(formRegex, `form${relationFormCount}-`);

	characterForm.insertBefore(newRelationForm, addRelationFormBtn);
	characterForm.insertBefore(newRelationFormSummary, addRelationFormBtn);

	totalForms.setAttribute('value', `${relationFormCount + 1}`);
});

console.log(addRelationFormBtn);

console.log('Hello world!');
