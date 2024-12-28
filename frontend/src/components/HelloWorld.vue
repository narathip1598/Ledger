<template>
  <div>
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
import API from '@/services/api';

export default {
  data() {
    return {
      message: ''
    };
  },
  mounted() {
    API.get('/')
      .then(response => {
        this.message = response.data.message;
      })
      .catch(error => {
        console.log(error);
      });
  }
};
</script>

<style scoped>
</style>
