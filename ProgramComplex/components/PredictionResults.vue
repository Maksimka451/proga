<template>
    <div>
      <h2>Результаты предсказания:</h2>
      <ol>
        <li v-for="(prediction, index) in predictions" :key="index">
          {{ index + 1 }}: {{ prediction }}
        </li>
      </ol>
    </div>
  </template>
  
  <script>
  export default {
    props: ['predictions'],
  };
  </script>
  