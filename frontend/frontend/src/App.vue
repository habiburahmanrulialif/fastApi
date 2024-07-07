<!-- src/App.vue -->
<template>
  <div id="app">
    <RatingPopup v-if="showRatingPopup" :itemId="1" :showPopup="showRatingPopup" @rating-submitted="handleRatingSubmitted" @not-authenticated="handleNotAuthenticated" />
    <Login v-if="showLogin" @authenticated="handleAuthenticated" />
    <button @click="openRatingPopup">Open Rating Popup</button>
  </div>
</template>

<script>
import RatingPopup from './components/RatingPopup.vue';
import Login from './components/Login.vue';

export default {
  components: {
    RatingPopup,
    Login
  },
  data() {
    return {
      showRatingPopup: false,
      showLogin: false,
      isAuthenticated: !!localStorage.getItem('access_token')
    };
  },
  methods: {
    openRatingPopup() {
      if (this.isAuthenticated) {
        this.showRatingPopup = true;
      } else {
        this.showLogin = true;
      }
    },
    handleRatingSubmitted() {
      this.showRatingPopup = false;
      alert('Thank you for your rating!');
    },
    handleNotAuthenticated() {
      this.showRatingPopup = false;
      this.showLogin = true;
    },
    handleAuthenticated() {
      this.showLogin = false;
      this.isAuthenticated = true;
      this.showRatingPopup = true;
    }
  }
};
</script>

<style>
#app {
  text-align: center;
  margin-top: 50px;
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
