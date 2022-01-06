function newTripModalToggle() {
  const body = document.querySelector("body");
  const modal = document.querySelector(".modal");
  modal.classList.toggle("opacity-0");
  modal.classList.toggle("pointer-events-none");
  body.classList.toggle("modal-active");
  selectLastField();
}

function selectLastField() {
  const sorted = Array.from(Object.keys(tripList)).sort(function (a, b) {
    return a - b;
  });
  document.getElementById(`location:${sorted[sorted.length - 1]}`).focus();
}

const tripList = {};
var currIndex = 0;

function generateNewLocationRow() {
  const row = document.createElement("div");
  row.className = "flex flex-row space-between my-1";
  row.id = `trip-row:${currIndex}`;
  const input = document.createElement("input");
  input.dataset.index = currIndex;
  input.addEventListener("keyup", inputChange);
  input.id = `location:${currIndex}`;
  input.className =
    "mx-1 px-1 border-b-2 border-gray-500 flex-grow location-input";
  const remove = document.createElement("button");
  remove.className =
    "mx-1 bg-red-500 text-sm rounded px-4 text-white py-2 remove-button";
  remove.addEventListener("click", removeRow);
  remove.id = `remove-row:${currIndex}`;
  remove.textContent = "-";
  remove.dataset.index = currIndex;
  const add = document.createElement("button");
  add.className =
    "mx-1 bg-blue-500 text-sm rounded px-4 text-white py-2 add-button";
  add.addEventListener("click", addNextRow);
  add.id = `add-row:${currIndex}`;
  add.textContent = "Add";
  add.dataset.index = currIndex;
  tripList[currIndex] = "";

  currIndex++;

  row.appendChild(input);
  row.appendChild(remove);
  row.appendChild(add);

  return row;
}

function inputChange(event) {
  // console.log(event);
  if (event.code === "Enter") {
    addNextRow();
    selectLastField();
  } else {
    const index = event.target.dataset.index;
    tripList[index] = event.target.value;
  }
}

function addNextRow() {
  console.log("Adding new row");
  const newLocs = document.getElementById("newTripLocations");
  const row = generateNewLocationRow();
  console.log(row);
  newLocs.appendChild(row);
  return row.dataset.index;
}

function removeRow() {
  const index = event.target.dataset.index;
  delete tripList[index];
  document.getElementById(`trip-row:${index}`).remove();
}

function planTrip() {
  const places = [];
  const sortedKeys = Object.keys(tripList).sort(function (a, b) {
    return a - b;
  });
  for (var i = 0; i < sortedKeys.length; i++) {
    if (tripList[i] !== "") {
      places.push(tripList[i]);
    }
  }
  fetch("/trip_plan", {
    method: "POST",
    body: JSON.stringify(places),
  })
    .then((res) => res.json())
    .then((res) => {
      if (res.success === true) {
        window.location = `/trip/${res.trip_id}`;
      }
    });
}

window.onload = () => {
  addNextRow();
};
