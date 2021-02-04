const getLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition, function (err) {
      console.log(`Error ${err.code}: ${err.message}`);
    });
  } else {
    console.log("geolocation is not supported");
  }
};

const showPosition = (position) => {
  fetch(
    `http://api.positionstack.com/v1/reverse?access_key=59d1e31a2c86b24426f703dcaec2ab61&query=${position.coords.latitude},${position.coords.longitude}`
  )
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      data.data.map((location) => {
        let displayLocation = document.getElementById("location");
        if (
          location.label ==
          `${"351" || "330" || "314"} Imam Haron Road, Cape Town, South Africa`
        ) {
          displayLocation.innerText = "LifeChoices Office";
        } else {
          displayLocation.innerText = location.label;
        }
      });
    });
};

getLocation();
