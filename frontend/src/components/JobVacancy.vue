<template>
  <div>
    <h2>Job Vacancy</h2>
    <form @submit.prevent="createJob">
      <div>
        <label>Job Title:</label>
        <input v-model="job.job_title" required />
      </div>
      <div>
        <label>Description:</label>
        <textarea v-model="job.description" required></textarea>
      </div>
      <button type="submit">Create Job</button>
    </form>

    <button @click="fetchJobs">Refresh Job List</button>
    <div v-if="jobs.length">
      <h3>Daftar Job Vacancy</h3>
      <ul>
        <li v-for="jobItem in jobs" :key="jobItem._id">
          <strong>{{ jobItem.job_title }}</strong> - {{ jobItem.description }}
          <br />
          Similarity:
          {{ jobItem.similarity ? jobItem.similarity.toFixed(2) + "%" : "N/A" }}
        </li>
      </ul>
    </div>

    <div>
      <h3>Similarity Update</h3>
      <textarea
        v-model="cvText"
        placeholder="Masukkan hasil OCR CV di sini"
      ></textarea>
      <button @click="updateSimilarity">Update Similarity</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "JobVacancy",
  data() {
    return {
      job: {
        job_title: "",
        description: "",
      },
      jobs: [],
      cvText: "",
    };
  },
  methods: {
    async createJob() {
      try {
        await axios.post("http://localhost:8000/job/", this.job);
        this.job.job_title = "";
        this.job.description = "";
        this.fetchJobs();
      } catch (error) {
        console.error(error);
      }
    },
    async fetchJobs() {
      try {
        const response = await axios.get("http://localhost:8000/job/");
        this.jobs = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async updateSimilarity() {
      if (!this.cvText) {
        alert("Masukkan hasil OCR CV terlebih dahulu.");
        return;
      }
      try {
        const response = await axios.post(
          "http://localhost:8000/job/update_similarity",
          { cv_text: this.cvText }
        );
        alert(response.data.message);
        this.fetchJobs();
      } catch (error) {
        console.error(error);
      }
    },
  },
  mounted() {
    this.fetchJobs();
    const storedOCR = localStorage.getItem("ocrText");
    if (storedOCR) {
      this.cvText = storedOCR;
    }
  },
};
</script>
