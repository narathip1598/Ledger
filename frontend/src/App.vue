<template>
  <div id="app">
    <div class="nav-bar">
      <router-link to="/login" class="nav-button">Login</router-link>
      <router-link to="/register" class="nav-button">Register</router-link>
    </div>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style scoped>
#app {
  font-family: Arial, sans-serif;
  margin-top: 20px;
}

.nav-bar {
  display: flex;
  justify-content: flex-end;
  margin: 10px 20px;
}

.nav-button {
  margin-left: 15px;
  padding: 8px 15px;
  background-color: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  cursor: pointer;
}

.nav-button:hover {
  background-color: #2980b9;
}
</style>
