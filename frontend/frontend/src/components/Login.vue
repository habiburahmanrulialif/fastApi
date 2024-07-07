<!-- src/components/Login.vue -->
<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit">Login</button>
    </form>
    <p>username for testing : test</p>
    <p>password for testing : test123</p>
    <p>For accesing api you can got to<a href="http://127.0.0.1:8000/docs" target="_blank" rel="noopener noreferrer">http://127.0.0.1:8000/docs</a>. There you can acces api directly</p>
    <p>You can clear the table for futher testing on <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noopener noreferrer">http://127.0.0.1:8000/docs</a></p>
  </div>
</template>

<script>
import axios from '../axiosConfig';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        const params = new URLSearchParams();
        params.append('grant_type', '');
        params.append('username', this.username);
        params.append('password', this.password);
        params.append('scope', '');
        params.append('client_id', '');
        params.append('client_secret', '');

        const response = await axios.post('/token', params.toString(), {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        });
        const { access_token, token_type } = response.data;
        
        // Store the access token securely
        localStorage.setItem('access_token', access_token);
        
        // Emit authenticated event to parent component (App.vue)
        this.$emit('authenticated');
      } catch (error) {
        console.error('Login error:', error);
        // Handle login error (show error message, reset form, etc.)
      }
    }
  }
};
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.form-group {
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
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
