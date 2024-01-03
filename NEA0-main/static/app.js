class Chatbox {
  constructor() {
    this.args = {
      openButton: document.querySelector(".chatbox__button"),
      chatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector(".send__button"),
    };
    this.state = false;
    this.messages = [];
  }

  display() {
    const { openButton, chatBox, sendButton } = this.args;

    this.prompt(chatBox);

    openButton.addEventListener("click", () => this.toggleState(chatBox));

    sendButton.addEventListener("click", () => this.onSendButton(chatBox));

    const node = chatBox.querySelector("input");
    node.addEventListener("keyup", ({ key }) => {
      if (key === "Enter") {
        this.onSendButton(chatBox);
      }
    });
  }

  prompt(chatbox) {
    this.messages.push({
      name: "Bot",
      message: "I am the Chatbot, and I can help answer your simple queries.",
    });
    this.updateChatText(chatbox);
  }

  toggleState(chatbox) {
    this.state = !this.state;
    // show or hides the box
    if (this.state) {
      chatbox.classList.add("chatbox--active");
    } else {
      chatbox.classList.remove("chatbox--active");
    }
  }

  onSendButton(chatbox) {
    var textField = chatbox.querySelector("input");
    let text1 = textField.value;
    if (text1 === "") {
      return;
    }

    let msg1 = { name: "User", message: text1 };
    this.messages.push(msg1);

    if (localStorage.getItem("save_response") == "true") {
      document.querySelector(".send__button").innerHTML = "updating...";
      textField.disabled = true;
      fetch("/save_response", {
        method: "POST",
        body: JSON.stringify({
          answer: text1,
          user_input: localStorage.getItem("user_input"),
        }),
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((r) => r.json())
        .then((r) => {
          localStorage.removeItem("user_input");
          localStorage.removeItem("save_response");

          let msg2 = { name: "Bot", message: r.answer };
          this.messages.push(msg2);
          this.updateChatText(chatbox);
          textField.value = "";
          textField.placeholder = "Write a message...";
          document.querySelector(".send__button").innerHTML = "Send";
          textField.disabled = false;
        });
    } else {
      fetch("/predict", {
        method: "POST",
        body: JSON.stringify({ message: text1 }),
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((r) => r.json())
        .then((r) => {
          if (r.answer && r.answer.status == "unknown") {
            let msg2 = { name: "Bot", message: r.answer.message };
            this.messages.push(msg2);
            this.updateChatText(chatbox);
            textField.value = "";
            textField.placeholder = "Your response";

            //   store the user_input and a flag to indicate that next post should go to saving response

            localStorage.setItem("user_input", r.answer.input);
            localStorage.setItem("save_response", "true");
          } else {
            let msg2 = { name: "Bot", message: r.answer };
            this.messages.push(msg2);
            this.updateChatText(chatbox);
            textField.value = "";
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          this.updateChatText(chatbox);
          textField.value = "";
        });
    }
  }

  updateChatText(chatbox) {
    var html = "";
    this.messages
      .slice()
      .reverse()
      .forEach(function (item, index) {
        if (item.name === "Bot") {
          html +=
            '<div class="messages__item messages__item--visitor">' +
            item.message +
            "</div>";
        } else {
          html +=
            '<div class="messages__item messages__item--operator">' +
            item.message +
            "</div>";
        }
      });
    const chatmessage = chatbox.querySelector(".chatbox__messages");
    chatmessage.innerHTML = html;
  }
}

const chatbox = new Chatbox();
chatbox.display();
