// // DOM element which needs to enter fullscreen mode
// var element = document.querySelector("#entire_body");

// element
//   .requestFullscreen()
//   .then(function () {
//     // element has entered fullscreen mode successfully
//   })
//   .catch(function (error) {
//     // element could not enter fullscreen mode
//     // error message
//     console.log(error.message);
//   });
window.location.assign("#quiz_area");
var g_submit_url = null;

const submit_question = (value) => {
  let url = "quiz/submit";
  // g_submit_url = submit_url;

  // if (!submit_url) {
  //   url = g_submit_url;
  // }
  // console.log(value);
  var xhr = new XMLHttpRequest();
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(
    JSON.stringify({
      value: value,
    })
  );
  xhr.onreadystatechange = function () {
    // If the request completed, close the extension popup
    if (xhr.readyState == 4)
      if (xhr.status == 200) {
        let json_data = xhr.responseText;
        json_data = JSON.parse(json_data);
        // console.log(json_data);
        if (json_data["redirect"]) {
          window.location.assign("/dashboard");
          return;
        }
        let question = json_data["qs"];
        let ansd_len = json_data["ansd_len"];
        let q_len = json_data["q_len"];
        let answers = json_data["ans"];
        // console.log(answers);
        setTimeout(function () {
          display_new_qestion(question, ansd_len, q_len, answers);
        }, 100);
      }
  };
};

const display_new_qestion = (q, ansd_len, q_len, answers) => {
  let q_label = document.getElementById("question");

  let answered = document.getElementById("answered");
  let total_question = document.getElementById("total_question");
  let button_div = document.getElementById("button_area");
  button_div.innerHTML = "";

  q_label.innerText = q;
  answered.innerText = ansd_len;
  total_question.innerText = q_len;
  for (let i = 0; i < answers.length; i++) {
    // console.log(answers[i]);
    if (answers[i]) {
      let button = create_button(answers[i]);
      button_div.appendChild(button);
    }
  }
};

const create_button = (data) => {
  let button = document.createElement("input");
  button.value = data;
  button.type = "submit";
  button.addEventListener("click", function () {
    submit_question(data);
  });
  button.classList = "btn btn-info mb-3 rounded-card";
  return button;
};
