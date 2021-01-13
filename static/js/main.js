// http://127.0.0.1:8000/users/main/subscribe/6/
var categories = document.getElementsByClassName("category");
var category_ids = document.getElementsByClassName("category-id");
var base_url = "http://127.0.0.1:8000/users/main/subscribe/";

for (var i = 0; i < categories.length; i++) {
  categories[i].addEventListener("click", (event) => {
    console.log(event.target.value);
  });
}

console.log(category_ids[0].outerText.trim());
