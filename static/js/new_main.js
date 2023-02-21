const incident = [
    {
        name: "Files Conversion Issues ",
        side_effect: "Comput_service",
        details: ["moving file in other server", "copying file in cluster", "<strong>any</strong> moving"],
        type: "Partial_Outage" ,
        photo: "https://learnwebcode.github.io/json-example/images/cat-2.jpg",
        date:"Jul 19, 16:19 UTC "
    },
    {
        name: "Networking Issues ",
        side_effect: "Neutron_service",
        type: "Major_Outage" ,
        photo: "https://learnwebcode.github.io/json-example/images/dog-1.jpg",
        date:" Jun 17, 16:19 UTC "
    },
    {
        name: "Origin Server Errors ",
        side_effect: "Ceph_service",
        details: ["issue1", "solving issue2", "isuue3"],
        type: "Partial_Outage" ,
        photo: "https://learnwebcode.github.io/json-example/images/cat-1.jpg",
        date:" Jun 16, 16:19 UTC "
    }
];



function age(birthYear) {
    let calculatedAge = new Date().getFullYear() - birthYear;
    if (calculatedAge == 1) {
        return "1 year old";
    } else if (calculatedAge == 0) {
        return "Baby";
    } else {
        return `${calculatedAge} years old`;
    }
}

function events(foods) {
    return `
<h4>Details</h4>
<ul class="details-list">
${foods.map(food => `<li>${food}</li>`).join("")}
</ul>
`;
}

function incidentTemplate(pet) {
    return `
    <div class="incident">
<!--    <img class="pet-photo" src="${pet.photo}">-->
    <h2 class="incident-name">${pet.name} <span class="species">(${pet.side_effect})</span></h2>
    <p style="color: brown"><strong>Type:</strong> ${pet.type}</p>
    <p align="right">${pet.date}</p>
    ${pet.details ? events(pet.details) : ""}
    </div>
  `;
}

document.getElementById("incident").innerHTML = `
  <h1 class="app-title"> latest incidents</h1>
  ${incident.map(incidentTemplate).join("")}
  <p class="footer">These ${incident.length} incidents were added recently. Check back soon for updates.</p>
`;