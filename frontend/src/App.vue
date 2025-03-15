<template>
  <div id="app">
    <h1>CV Revognizer and relevance job checker</h1>
    <nav>
      <button @click="currentView = 'CVUploads'">CVUploads</button>
      <button @click="currentView = 'JobVacancy'">JobVacancy</button>
    </nav>
    <component :is="currentView" />
  </div>
</template>

<script>
import CVUploads from "./components/CVUploads.vue";
import JobVacancy from "./components/JobVacancy.vue";

export default {
  name: "App",
  components: {
    CVUploads,
    JobVacancy,
  },
  data() {
    return {
      currentView: "CVUploads",
    };
  },
};
</script>
