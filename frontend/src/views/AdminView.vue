<template>

<AdminNavbar @changevenue="changevenue()" @changeshow="changeshow()" @changemovie="changemovie()" @changesummary="changesummary()"></AdminNavbar>


<component :is="currentComponent" :venues="venues" :shows="shows" :movies="movies" :bookings="bookings"></component>

</template>


<script>

import AdminNavbar from "@/components/AdminNavbar.vue";
import VenuePage from "@/components/VenuePage.vue";
import ShowPage from "@/components/ShowPage.vue";
import MoviePage from "@/components/MoviePage.vue";
import AdminSummary from "@/components/AdminSummary.vue";

export default {
  name: "AdminView",
  components: {
    AdminNavbar,
    VenuePage,
    ShowPage,
    MoviePage,
    AdminSummary,
  },
  data() {
    return {
      name: null,
      email: null,
      auth_token: null,
      currentComponent: null,
      venues: null,
      movies: null,
      shows: null,
      bookings: null,
    };
  },
  async created() {
    this.auth_token = sessionStorage.getItem("auth-token");
    this.email = sessionStorage.getItem("email");
    this.name = sessionStorage.getItem("name");
    
    if (!this.auth_token) {
      alert("Please Login to see your dashboard.");
      this.$router.push("/");
    }
    
    this.currentComponent = 'VenuePage';
    
    return fetch("http://127.0.0.1:5000/api/user", {
      method: "GET",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Authentication-Token": `${this.auth_token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("admin home page");
        console.log(data);
        this.venues = data['venues'];
        this.movies = data['movies'];
        this.shows = data['shows'];
        this.bookings = data['bookings'];
      })
      .catch((error) => console.log("err", error));
  },
  
  methods: {
  
  async changevenue(){
  this.currentComponent = 'VenuePage';
  },
  
  async changeshow(){
  this.currentComponent = 'ShowPage';
  },
  
  async changemovie(){
  this.currentComponent = 'MoviePage';
  },
  
  async changesummary(){
  this.currentComponent = 'AdminSummary';
  },
  },
};
</script>

