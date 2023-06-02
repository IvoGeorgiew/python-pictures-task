document.addEventListener("mousemove", function (event) {
  const coordinatesDiv = document.getElementById("coordinatesDiv");

  const coordinates = {
    x: event.clientX,
    y: event.clientY,
  };

  coordinatesDiv.innerText = `X: ${coordinates.x}, Y: ${coordinates.y}`;
});

document.addEventListener("click", function (event) {
  if (event.button === 0) {
    const data = {
      x: event.clientX,
      y: event.clientY,
    };

    fetch("http://localhost:8000/coordinates", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (response.ok) {
          console.log("Coordinates sent successfully!");
        } else {
          console.error("Failed to send coordinates.");
        }
      })
      .catch((error) => {
        console.error("An error occurred:", error);
      });
  }
});
