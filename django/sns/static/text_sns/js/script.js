window.addEventListener("DOMContentLoaded", (event) => {
  var likeBtn = document.getElementById("good_btn");
  likeBtn.addEventListener('click', (event) => {
    var obj_id = document.getElementById("obj_id").innerText;
    var url = `/text_sns/good/${obj_id}/`;  // Django と連携
    var csrfToken = getCookie("csrftoken");
    var data = {};

    fetch(url, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(data),
    })
    .then(Response => Response.json())
    .then(data => { // 受け取ったデータ
      if (data["message"] === "create") {
        var likeCount = document.getElementById("good_count");
        likeCount.innerText = (Number(likeCount.innerText)+1).toString();
      } else if (data["message"] === "delete") {
        var likeCount = document.getElementById("good_count");
        likeCount.innerText = (Number(likeCount.innerText)-1).toString();
      }
    })
    .catch((error) => {
      console.log(error);
    });
  }, false);
}, false);

function getCookie(name) {
  if (document.cookie && document.cookie !== "") {
    for (var cookie of document.cookie.split(';')) {
      var [key, value] = cookie.trim().split("=");
      if (key === name) {
        return decodeURIComponent(value);
      }
    }
  }
  return null;
}
