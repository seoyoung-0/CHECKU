// http://127.0.0.1:8000/users/main/subscribe/6/
var categories = document.getElementsByClassName("category");
var category_ids = document.getElementsByClassName("category-id");
var category_entire = document.querySelector(".category-entire");
var base_url = "http://127.0.0.1:8000/users/main/subscribe/";
var category_is_seleceted = [];

for (let i = 0; i < categories.length; i++) {
  category_is_seleceted.push(false);
}

for (let i = 0; i < categories.length; i++) {
  categories[i].addEventListener("click", () => {
    notice_num = category_ids[i].innerHTML.trim();
    axios
      .get(base_url + notice_num)
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });

    categories[i].classList.toggle("category-selected");

    // if (category_is_seleceted[i] == false) {
    //   categories[i].classList.add("category-selected");
    //   category_is_seleceted[i] = true;
    // } else {
    //   categories[i].classList.remove("category-selected");
    //   category_is_seleceted[i] = false;
    // }
  });
}

category_entire.addEventListener("click", () => {
  for (let i = 0; i < categories.length; i++) {
    categories[i].classList.toggle("category-selected", true);
  }
});
