
// loading screen disappear 
document.addEventListener("DOMContentLoaded", function () {
    let loadingwrap = document.getElementById("loading-wrap");
    setTimeout(function () {
        loadingwrap.style.display = "none";
    }, 1500);
});

// taking server link and declaring the animals array
const MY_SERVER = 'http://127.0.0.1:5000';
let animals = [];

// show the entire array object from the server
async function show() {

    let response = await fetch(`${MY_SERVER}/get_animals`);
    response = await response.json();
    animals = response.animals
    // console.log(animals);
    localStorage.setItem('Animals', JSON.stringify(animals))
    display.innerHTML = animals.map(animal =>
        `<div class="animalContainer card" style="width: 18rem;">
                <img src="./images/${animal.type.toLowerCase()}.webp" height=200px class="card-img-top" alt="${animal.type}">
                <h5 class="card-title">${animal.AnimalName}</h5>
                <p>Type: ${animal.type}</p> <p>Age: ${animal.age}</p>  
            <button onclick="deleteAnimal(${animal.id})">Delete</button>    
            <button onclick="updateAnimal(${animal.id})">Update</button>
            </div>`).join('');

}

// adding new animals
async function addAnimal() {
    fetch(`${MY_SERVER}/add_animal`, {
        method: 'POST',
        body: JSON.stringify({
            animalName: animalName.value,
            type: animalType.value,
            age: animalAge.value
        }),
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
        },
    })
        .then((response) => response.json())
        .then((json) => console.log(json));
    show();
}

async function deleteAnimal(id) {
    await fetch(`${MY_SERVER}/delete_animal/${id}`, {
        method: 'DELETE',
    });
    console.log();
    show();
}

async function updateAnimal(id) {
    fetch(`${MY_SERVER}/edit_animal/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            animalName: animalName.value,
            type: animalType.value,
            age: animalAge.value
        }),
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
        },
    })
        .then((response) => response.json())
        .then((json) => console.log(json));
    show();
}
document.addEventListener("DOMContentLoaded", function() {
    show();
});