
var global_r;

class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            fileInput: document.querySelector('#fileInput'), // Added the file input element
        }

        this.state = false;
        this.messages = [{ name: "Sam", message: "Hi, welcome to personality Test" }];
    }

    display() {
        const { openButton, chatBox, sendButton, fileInput } = this.args;
        // openButton.addEventListener('click', () => this.toggleState(chatBox));
        sendButton.addEventListener('click', () => this.onSendButton(chatBox));
        fileInput.addEventListener('change', () => this.onFileSelect(chatBox)); // Listen for file input change

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({ key }) => {
            if (key == "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }


    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 =  textField.value
        if(text1 === ""){
            return;
        }
    
        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);
    
        // Check if the last message from Sam is the trigger message
        const lastMessageFromSam = this.getLastMessageFromSam();
        console.log(lastMessageFromSam);
        if (lastMessageFromSam === "Plesase Enter the text to detect your personality") {
            this.sendUserTextToTextProcess(text1, chatbox);
        } else {
            // Send the message as usual
            this.sendUserTextToServer(text1, chatbox);
        }
    
        textField.value = '';
    }

    retrieveQuestions(chatbox) {
        fetch('http://127.0.0.1:5000/questions5', {
            method: 'GET',
            mode: 'cors'
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Display the retrieved questions to the user
            this.displayQuestions(data, chatbox);
        })
        .catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox);
        });
    }
    
    // Helper function to get the last message from Sam
    getLastMessageFromSam() {
        const reversedMessages = this.messages.slice().reverse();
        for (const message of reversedMessages) {
            if (message.name === "Sam") {
                return message.message;
            }
        }
        return "";
    }

    displayQuestions(questionsData, chatbox) {
        let msg = { name: "Sam", message: "Please answer the following questions" };
        this.messages.push(msg);

        // Add each question as a message
        questionsData.questions.forEach((question, index) => {
            let questionMsg = { name: "Sam", message: `${index + 1}. ${question.question}` };
            this.messages.push(questionMsg);
        });
        const html = '<div class="questions">' + questionsData.questions.map((question, index) => {
            return `
                <div class="question">
                    <p>${index + 1}. ${question.question}</p>
                    ${question.options.map((option, optionIndex) => {
                        return `
                            <input type="radio" name="question${index}" id="option${index}-${optionIndex}" value="${option[0]}">
                            <label for="option${index}-${optionIndex}">${option[0]}</label><br>
                        `;
                    }).join('')}
                </div>
            `;
        }).join('') + '</div>';
    
        // Add a submit button to the chatbox
        const submitButton = document.createElement('button');
        submitButton.classList.add('submit__button');
        submitButton.textContent = 'Submit Answers';
    
        // Display the questions and the submit button to the user
        const chatMessages = chatbox.querySelector('div.chatbox__messages');
        document.querySelector("div.submitquestions").appendChild(submitButton);
        // chatMessages.appendChild(submitButton);
        chatMessages.innerHTML = html + chatMessages.innerHTML;
        
    
        // Attach an event listener to the submit button to capture user's answers
        submitButton.addEventListener('click', () => this.captureUserAnswers(questionsData, chatbox));
    }
    
    captureUserAnswers(questionsData, chatbox) {
        // Capture user's answers here
        const answers = [];
        questionsData.questions.forEach((question, index) => {
            const selectedOption = chatbox.querySelector(`input[name="question${index}"]:checked`);
            if (selectedOption) {
                answers.push({ question: question.question, answer: selectedOption.value });
            }
        });

        // Add user answers as messages
        answers.forEach((answer, index) => {
            let answerMsg = { name: "User", message: `Answer to question ${index + 1}: ${answer.answer}` };
            this.messages.push(answerMsg);
        });
        document.querySelector("div.submitquestions").innerHTML=""
        questionsData.questions.forEach((question, index) => {
            const selectedOption = chatbox.querySelector(`input[name="question${index}"]:checked`);
            if (selectedOption) {
                answers.push({ question: question.question, answer: selectedOption.value });
            }
        });
    
        // Send the answers to the server using a POST request
        fetch('/processanswers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ answers }),
        })
        .then(response => response.json())
        .then(data => {
            // Display the result to the user (customize as needed)
            const resultMessage = `Personality Prediction: ${data.result}`;
            
            let msg2 = { name: "Sam", message: resultMessage };
            this.messages.push(msg2);
            this.updateChatText(chatbox);
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle errors as needed
        });
    }
    
    

    
    // Send the user's text to the textprocess route
    sendUserTextToTextProcess(userText, chatbox) {
        fetch('http://127.0.0.1:5000/textprocess', {
            method: 'POST',
            body: JSON.stringify({ message: userText }),
            mode: 'cors',
            headers: {
                'Content-Type' : 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            let msg2 = { name: "Sam", message: data.result };
            this.messages.push(msg2);
            this.updateChatText(chatbox);
        })
        .catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox);
        });
    }
    
    // Send the user's text to the server (for messages other than the trigger message)
    sendUserTextToServer(userText, chatbox) {
        fetch('http://127.0.0.1:5000/predict1', {
            method: 'POST',
            body: JSON.stringify({ message: userText }),
            mode: 'cors',
            headers: {
                'Content-Type' : 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            let msg2 = { name: "Sam", message: data.answer };
            this.messages.push(msg2);
            this.updateChatText(chatbox);
            const lastMessageFromSam = this.getLastMessageFromSam();
            console.log(lastMessageFromSam === "please answer the following questions")
            if (lastMessageFromSam === "please answer the following questions") {
                this.retrieveQuestions(chatbox);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox);
        });
    }
    

    onFileSelect(chatbox) {
        const fileInput = this.args.fileInput;
        const file = fileInput.files[0];
        if (!file) return;
        let msg2 = { name: "Sam", message: "Received file Input, Running Prediction Query" }; // Access the "answer" field
        this.messages.push(msg2);
        this.updateChatText(chatbox);

        const formData = new FormData();
        formData.append('file', file);
    
        fetch('http://127.0.0.1:5000/runfile', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data); // Access the data here
            global_r = data;
    
            // You can use 'data' to update your chatbox or perform other operations
            let msg = { name: "Sam", message: data.result };
            this.messages.push(msg);
            this.updateChatText(chatbox);
            fileInput.value = ''; // Clear the file input
        })
        .catch(error => {
            console.error('Error:', error);
            this.updateChatText(chatbox);
            fileInput.value = ''; // Clear the file input
        });
    }
    

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function (item) {
            if (item.name === "Sam") {
                html += '<div class="messages__item messages__item--visitor"> ' + item.message + ' </div>';
            } else {
                html += '<div class="messages__item messages__item--operator"> ' + item.message + ' </div>';
            }
        });

        var chatmessage = chatbox.querySelector('div.chatbox__messages');
        chatmessage.innerHTML = html;
    }

}

const chatbox = new Chatbox();
chatbox.display();