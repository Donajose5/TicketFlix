<template>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" />

    <br><br>
    <h1>Summary</h1><br>

    <div class='summary' v-if="this.curr == 'summary'">
    
        <div class="no" v-if="this.venues == true">
            No venues available
        </div>

        <div v-else>
            <h3> Venues </h3>
            <div v-for="venue of venues" :key="venue.venue_id" class='summaryclass'>
                <div class='container'>
                    Summary of {{venue.name}}
                </div>
            </div>
        </div>
        <br><br>

        <div class="no" v-if="this.movies == true">
            No movies available
        </div>

        <div v-else>
            <h3> Movies </h3>
            <div v-for="movie of movies" :key="movie.venuemovie_id" class='summaryclass'>
                <div class='container'>
                    Summary of {{movie.name}}
                </div>
            </div>
        </div>
        

    </div>

</template>


<script>

export default {
    name: "AdminSummary",
    components: {
    },
    data() {
        return {
            name: null,
            email: null,
            auth_token: null,
            curr: null,
        };
    },

    props: [
        'venues',
        'movies',
    ],

    async created() {
        this.auth_token = sessionStorage.getItem("auth-token");
        this.email = sessionStorage.getItem("email");
        this.name = sessionStorage.getItem("name");

        if (!this.auth_token) {
            alert("Please Login to see your dashboard.");
            this.$router.push("/");
        }

        this.curr = "summary";
        
        /*
        try {
        
              const res = await fetch("http://127.0.0.1:5000/api/download/" + booking.booking_id, {
                        mode: "cors",
                        method: "GET",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authentication-Token": `${this.auth_token}`,
                        },
                    });

                    console.log(res);

                    if (res.ok) {
                        console.log("downloaded");
                    }
                } catch (error) {
                    console.log("download error", error);
                }
        */

    },

    methods: {
    },
};
</script>

<style>
* {
    text-align: center;
}

.head {
    padding: 4%;
    font-size: 60px;
}

.main {
    padding: 1%;
}

.btn1 {
    text-align: center;
    font-size: 20px;
    -webkit-text-decoration: None;
    text-decoration: None;
    background-color: #75C2F6;
    height: 5%;
    width: 20%;
    padding: 20px;
    margin: auto;
}

.btn1:hover {
    background-color: #4997cb;
}

.no {
    padding-top: 5%;
    font-size: 30px;
}

.summaryclass {
    border-style: solid;
    border-color: black;
    border-radius: 3px;
    border-width: 1px;
    padding: 30px;
    width: 40%;
    margin-left: auto;
    margin-right: auto;
    margin-top: 20px;
    margin-bottom: 15px;
}

</style>



