<template>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" />

    <br><br>
    <h1>Available Venues</h1><br><br>

    <div class="no" v-if="this.venue == true">
        No Venues available
    </div>

    <div v-else>
    
     <div id="popup">
                <p class="alert alert-success fade show" role="alert" v-if="esuccess">
                    {{ esuccess }}
                </p>
            </div>

        <table class="table">
            <thead>
                <tr>
                    <td> Venue ID </td>
                    <td> Name </td>
                    <td> Location </td>
                    <td> Capacity </td>
                    <td> Number of Shows </td>
                    <td></td>
                </tr>
            </thead>

            <tbody>
                <tr v-for="venue of venues" :key="venue.venue_id">
                    <td> {{ venue.venue_id }} </td>
                    <td> {{ venue.name }} </td>
                    <td> {{ venue.location }} </td>
                    <td> {{ venue.capacity }} </td>
                    <td> {{ venue.nshows }} </td>
                    <td>
                        <button class="btn btn-success my-2 btn-lg" type="submit"
                            @click="downloadvenuedetails(venue)">Download Details</button>
                    </td>
                </tr>
            </tbody>
        </table>

    </div>
</template>



<script>
export default {
    name: "UserVenue",
    components: {
    },
    data() {
        return {
            name: null,
            email: null,
            auth_token: null,
            fields: null,
            esuccess: null,
        };
    },

    props: [
        'venues',
    ],
    computed: {

    },

    async created() {
        this.auth_token = sessionStorage.getItem("auth-token");
        this.email = sessionStorage.getItem("email");
        this.name = sessionStorage.getItem("name");

        if (!this.auth_token) {
            alert("Please Login to see your dashboard.");
            this.$router.push("/");
        }

    },

    methods: {

        async downloadvenuedetails(venue) {

            console.log(venue);
            this.fields = ['venue_id', 'name', 'location', 'capacity', 'nshows'];

            let fn = "venue_"+venue.venue_id+".csv";
            console.log(fn);

            try {
                const res = await fetch("http://127.0.0.1:5000/api/export/" + venue.venue_id, {
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
                    this.esuccess = "The exported file has been sent to your mail.";
                }
            } catch (error) {
                console.log("download error", error);
            }
            

        },

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

input {
    text-align: center;
    font-size: 20px;
    height: 15px;
    width: 20%;
    padding: 20px;
    margin: auto;
}

a {
    font-size: 20px;
}

.alert {
    width: 20%;
    margin: auto;
}

.no {
    padding-top: 5%;
    font-size: 30px;
}

thead td {
    font-size: 20px;
    font-weight: bold;
}

tbody td {
    padding: 30px;
}

.boxbtn {
    width: 200px;
    margin: 10px;
}

.formtable {
    margin-left: auto;
    margin-right: auto;
}
</style>



