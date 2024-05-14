<template>
    <div>
      <input type="file" @change="handleFileUpload" accept=".csv">
      <button @click="submitFile">Предсказать</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      handleFileUpload(event) {
        this.file = event.target.files[0];
      },
      async submitFile() {
        const formData = new FormData();
        formData.append('file', this.file);
        try {
          const response = await fetch('/predict/', {
            method: 'POST',
            body: formData,
          });
          const data = await response.json();
          this.$emit('predictions-updated', data.predictions);
        } catch (error) {
          console.error('Error predicting:', error);
        }
      },
    },
    data() {
      return {
        file: null,
      };
    },
  };
  </script>
  