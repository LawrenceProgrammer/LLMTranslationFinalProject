// Attach an event listener to the send button to trigger `sendMessage` when clicked
document.getElementById('send-button').addEventListener('click', sendMessage);

// Attach an event listener to the input field to trigger `sendMessage` when the Enter key is pressed
document.getElementById('user-input').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') sendMessage();
});

// Asynchronous function to handle sending user input and fetching the translation
async function sendMessage() {
  // Get the trimmed value of the user input
  const userInput = document.getElementById('user-input').value.trim();

  // If the input is empty, do nothing
  if (userInput === '') return;

  // Retrieve the selected LLM, source language, and target language from the dropdowns
  const llm = document.getElementById('llm-select').value;
  const translateFrom = document.getElementById('translate-from').value;
  const translateTo = document.getElementById('translate-to').value;

  // Add the user's input message to the chat window with the selected translation settings
  addMessage(`Using ${llm}, translating from ${translateFrom} to ${translateTo}: "${userInput}"`, 'user');

  // Clear the input field after the message is sent
  document.getElementById('user-input').value = '';

  try {
    // Build the query string with the translation settings and the user input
    const queryParams = new URLSearchParams({
      source: translateFrom,      // Source language
      destination: translateTo,  // Target language
      sentence: userInput,       // Sentence to translate
      llm: llm,                  // Selected LLM
    });

    // Make a GET request to the translation API endpoint with the query parameters
    const response = await fetch(`http://127.0.0.1:8000/translate?${queryParams}`, {
      method: 'GET', // HTTP GET request
      headers: {
        'Content-Type': 'application/json' // Ensure JSON content type for the request
      },
    });

    // If the response is not successful, throw an error
    if (!response.ok) {
      throw new Error('Error in translation API');
    }

    // Parse the JSON response from the API
    const data = await response.json();
    const translation = data.translation; // Extract the translation result

    // Add the translation result to the chat window as a bot message
    addMessage(translation, 'bot');
  } catch (error) {
    // Handle any errors by showing an error message in the chat window
    addMessage('Error: Unable to process the translation.', 'bot');
  }
}

// Function to add a message to the chat window
function addMessage(message, sender) {
  const chatWindow = document.getElementById('chat-window'); // Get the chat window element
  const messageDiv = document.createElement('div'); // Create a new div for the message
  messageDiv.classList.add('chat-message', sender === 'user' ? 'user-message' : 'bot-message'); // Add CSS classes based on the sender (user or bot)
  messageDiv.textContent = message; // Set the text content of the message
  chatWindow.appendChild(messageDiv); // Append the message div to the chat window
  chatWindow.appendChild(document.createElement('br')); // Add a line break for spacing
  chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to the bottom of the chat window to show the new message
}
