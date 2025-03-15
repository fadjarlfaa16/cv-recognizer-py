<template>
  <div>
    <h2>Upload your CV</h2>
    <input type="file" @change="onFileChange" accept="application/pdf" />
    <button @click="uploadCV" :disabled="loading">Upload</button>
    <div v-if="loading">
      <p>Loading... (Processing your CV)</p>
    </div>
    <div v-if="message">
      <p>{{ message }}</p>
    </div>
    <div v-if="extractedText">
      <h3>OCR Result:</h3>
      <pre>{{ extractedText }}</pre>
    </div>
    <div v-if="openrouterResponse">
      <h3>Response OpenRouter API:</h3>
      <pre>{{ openrouterResponse }}</pre>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CVUploads",
  data() {
    return {
      file: null,
      loading: false,
      message: "",
      extractedText: "",
      openrouterResponse: "",
    };
  },
  methods: {
    onFileChange(e) {
      this.file = e.target.files[0];
      console.log("Choosen file:", this.file);
    },
    async uploadCV() {
      if (!this.file) {
        alert("Select your CV first.");
        return;
      }
      console.log("Uploading your file:", this.file);
      this.loading = true;
      this.message = "";
      this.extractedText = "";
      this.openrouterResponse = "";
      const formData = new FormData();
      formData.append("file", this.file);
      try {
        const response = await axios.post(
          "http://localhost:8000/cv/upload",
          formData,
          {
            headers: { "Content-Type": "multipart/form-data" },
          }
        );
        console.log("Backend Response:", response.data);
        this.message = response.data.message;
        this.extractedText = response.data.extracted_text;
        this.openrouterResponse = response.data.openrouter_response;

        // Simpan hasil OCR ke localStorage
        localStorage.setItem("ocrText", this.extractedText);
      } catch (error) {
        console.error("Error while Upload:", error);
        this.message = "Error occured while uploading file.";
      }
      this.loading = false;
    },
  },
};
</script>
