<template>
  <div>
    <h1>Quiz Questions</h1>
    <div v-if="questions.length > 0">
      <div v-for="(question, qIndex) in questions" :key="question.id" class="question">
        <h2>{{ qIndex + 1 }}. {{ question.question_text }}</h2>
        <ul>
          <li v-for="choice in question.choices" :key="choice.id"
            :class="{ selected: selectedChoices[question.id] === choice.id }"
            @click="selectChoice(question.id, choice.id)">
            {{ choice.choice_text }}
          </li>
        </ul>
      </div>
      <button class="submit-button" @click="submitAnswers">Submit</button>
    </div>
    <div v-else>
      <p>Loading questions...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      questions: [], // To store questions and their choices
      selectedChoices: {} // To track selected choices by question ID
    };
  },
  mounted() {
    this.updateTitle(); // Set the page title
    this.fetchQuestions();
  },
  methods: {
    updateTitle() {
      document.title = "Quiz Page"; // Set your desired title here
    },
    async fetchQuestions() {
      try {
        const response = await axios.get('http://localhost:8000/questions'); // Replace with your backend URL
        this.questions = response.data; // Assumes the response structure matches your model
      } catch (error) {
        console.error('Error fetching questions:', error);
      }
    },
    selectChoice(questionId, choiceId) {
      // Directly update the reactive object
      this.selectedChoices[questionId] = choiceId;
    },
    submitAnswers() {
      // Convert the selectedChoices object into an array of objects
      const payload = Object.entries(this.selectedChoices).map(([questionId, choiceId]) => ({
        question_id: parseInt(questionId), // Ensure question_id is an integer
        choice_id: choiceId // choice_id should already be an integer
      }));

      // Send the transformed payload to the backend
      axios.post('http://localhost:8000/check-answers', payload)
        .then(response => {
          console.log('Answers checked successfully:', response.data);
          const results = response.data.results;

          // Display results for the user
          let message = "Here are your results:\n";
          results.forEach(result => {
            message += `Question ${result.question_id}: Selected: "${result.selected_choice}", Correct: "${result.correct_choice}", Correct Answer: ${result.is_correct ? 'Yes' : 'No'}\n`;
          });

          alert(message); // Display results in an alert, or modify to use a UI component
        })
        .catch(error => {
          console.error('Error checking answers:', error);
          alert('There was an error checking your answers. Please try again.');
        });
    }
  }
};
</script>


<style scoped>
/* Styling remains unchanged from the earlier example */
div {
  font-family: 'Arial', sans-serif;
  color: #333;
  line-height: 1.6;
}

h1 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 20px;
  text-align: center;
}

.question {
  background-color: #f9f9f9;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #34495e;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  background-color: #ffffff;
  border: 1px solid #dcdcdc;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 8px;
  transition: background-color 0.3s, transform 0.2s;
  cursor: pointer;
}

li:hover {
  background-color: #e8f7ff;
  transform: scale(1.02);
}

li.selected {
  background-color: #3498db;
  color: #fff;
  border-color: #2980b9;
}

.submit-button {
  display: block;
  margin: 20px auto;
  padding: 10px 20px;
  font-size: 1.2rem;
  font-weight: bold;
  color: #fff;
  background-color: #3498db;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.submit-button:hover {
  background-color: #2980b9;
  transform: scale(1.05);
}

.submit-button:active {
  background-color: #1c5981;
}

p {
  font-size: 1.2rem;
  color: #7f8c8d;
  text-align: center;
}

@media (max-width: 600px) {
  h1 {
    font-size: 1.5rem;
  }

  h2 {
    font-size: 1.2rem;
  }

  li {
    font-size: 1rem;
    padding: 8px;
  }

  .submit-button {
    font-size: 1rem;
    padding: 8px 16px;
  }
}
</style>
