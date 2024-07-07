<template>
  <div v-if="showPopup" class="rating-popup">
    <h2 style="color: black;">How would you rate your satisfaction with out product?</h2>
    <div class="stars">
      <div v-for="star in 5" :key="star" class="star-container">
        <span @click="rate(star)" :class="{ filled: star <= rating }">&#9733;</span>
        <span class="star-number">{{ star }}</span>
        <span v-if="star === 1" class="star-label">Very dissatisfied</span>
        <span v-if="star === 5" class="star-label">Very satisfied</span>
      </div>
    </div>
    <button @click="submitRating">Submit Rating</button>
    <p style="color: black;">For accesing api you can got to<a href="http://127.0.0.1:8000/docs" target="_blank" rel="noopener noreferrer">http://127.0.0.1:8000/docs</a>. There you can acces api directly</p>
    <p style="color: black;">You can clear the table for futher testing on <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noopener noreferrer">http://127.0.0.1:8000/docs</a></p>
  </div>
</template>

<script>
import axios from '../axiosConfig';

export default {
  props: {
    itemId: {
      type: Number,
      required: true
    },
    showPopup: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      rating: 0
    };
  },
  methods: {
    rate(star) {
      this.rating = star;
    },
    async submitRating() {
      try {
        const response = await axios.post('/feedback', {
          item_id: this.itemId,
          rating: this.rating
        });
        console.log('Rating submitted:', response.data);
        this.$emit('rating-submitted');
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.$emit('not-authenticated');
        } else {
          console.error('Error submitting rating:', error);
          // Handle other errors (e.g., show error message to the user)
        }
      }
    }
  }
};
</script>

<style scoped>
.rating-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  background: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  z-index: 1000;
  text-align: center; /* Center align content */
}

.stars {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.star-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 5px; /* Adjust margin between star containers */
}

.stars span {
  font-size: 2em;
  cursor: pointer;
  color: #ccc;
}

.stars span.filled {
  color: gold;
}

.star-number {
  font-size: 1.2em;
  margin-top: 5px;
}

.star-label {
  font-size: 0.8em;
  margin-top: 2px;

}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #45a049;
}
</style>
