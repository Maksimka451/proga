import Vue from 'vue';
import FileUploadForm from './components/FileUploadForm';
import PredictionResults from './components/PredictionResults';

new Vue({
  el: '#app',
  components: {
    FileUploadForm,
    PredictionResults,
  },
  data() {
    return {
      predictions: [],
    };
  },
  methods: {
    updatePredictions(predictions) {
      this.predictions = predictions;
    },
  },
});
