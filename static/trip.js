function add_stop() {
  const location = document.getElementById("newStop").value;
  const buttons = Array.from(document.getElementsByTagName("button"));
  loading = true;
  buttons.forEach((element) => {
    element.classList.add("animate-pulse");
    element.disabled = true;
  });
  fetch(`/add_stop/${trip_id}`, {
    method: "POST",
    body: location,
  })
    .then((res) => res.json())
    .then((res) => {
      window.location.reload();
    });
}

function key_press() {
  if (event.code === "Enter" && !loading) {
    add_stop();
  }
}

window.onload = () => {
  document.getElementById("newStop").addEventListener("keydown", key_press);
};
