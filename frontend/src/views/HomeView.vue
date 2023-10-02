<template>
    <div class='home'>

        <UserNavbar @changebookings="changebookings()" @changeprofile="changeprofile()" @changeuservenue="changeuservenue()" @changeusershow="changeusershow()"
            @searchfunc="(searchquery = $event), searchfunc()"></UserNavbar>

        <component :is="currentComponent" :venues="venues" :shows="shows" :movies="movies" :bookings="bookings"
            :display="display" :userbookings="userbookings" :user_id="user_id" :password="password"></component>

    </div>
</template>
    
    
<script>

import UserNavbar from "@/components/UserNavbar.vue";
import UserShow from "@/components/UserShow.vue";
import BookingsPage from "@/components/BookingsPage.vue";
import ProfilePage from "@/components/ProfilePage.vue";
import SearchPage from "@/components/SearchPage.vue";
import UserVenue from "@/components/UserVenue.vue";

export default {
    name: "HomeView",
    components: {
        UserNavbar,
        UserShow,
        SearchPage,
        BookingsPage,
        ProfilePage,
        UserVenue,
    },
    data() {
        return {
            name: null,
            email: null,
            user_id: null,
            password: null,
            auth_token: null,
            currentComponent: null,
            searchquery: null,
            venues: null,
            movies: null,
            shows: null,
            bookings: null,
            display: null,
            userbookings: null
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

        this.currentComponent = 'UserShow';

        await fetch("http://127.0.0.1:5000/api/user", {
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
                console.log("user home page");
                this.user_id = data['user_id'];
                this.password = data['password'];
                this.venues = data['venues'];
                this.movies = data['movies'];
                this.shows = data['shows'];
                this.bookings = data['bookings'];
            })
            .catch((error) => console.log("err", error));

        await fetch("http://127.0.0.1:5000/api/show", {
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
                this.display = data['display_shows'];
            })
            .catch((error) => console.log("err", error));

        return fetch("http://127.0.0.1:5000/api/booking", {
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
                this.userbookings = data['bookings'];
            })
            .catch((error) => console.log("err", error));
    },

    methods: {

        async changebookings() {
            this.currentComponent = 'BookingsPage';
        },

        async changeprofile() {
            this.currentComponent = 'ProfilePage';
        },
        async changeuservenue() {
            this.currentComponent = 'UserVenue';
        },
        async changeusershow() {
            this.currentComponent = 'UserShow';
        },

        async searchfunc() {
            console.log("Search function");
            console.log(this.searchquery);
            //this.currentComponent = 'SearchPage';
            this.currentComponent = 'UserShow';

            await fetch("http://127.0.0.1:5000/api/searching/" + this.searchquery, {
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
                    this.display = data['display_shows'];
                })
                .catch((error) => console.log("err", error));


        }
    },

};
</script>
    
