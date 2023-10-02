<template>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" />

    <br><br>
    <h1>Venues</h1><br>

    <div class='mainvenue' v-if="this.curr == 'mainvenue'">

        <button class="btn btn-primary my-2 btn-lg add" type="submit" @click="changeaddvenue()">Add a new Venue</button>


        <div class="no" v-if="this.venues == true">
            No venues available
        </div>

        <div v-else>
            <div v-for="venue of venues" :key="venue.venue_id" class='venueclass'>
                <div class='container'>
                    <div class='row'>
                        <div class='col'>
                            <div class='venuehead'>{{ venue.name }}</div>
                        </div>
                        <div class='col'>
                            <div class='venuebody'>
                                Location: {{ venue.location }} <br>
                                Capacity: {{ venue.capacity }}
                            </div>
                        </div>
                        <div class='col'>
                            <button class="btn btn-success my-2 btn-lg boxbtn" type="submit"
                                @click="changeeditvenue(venue)">Edit</button>
                            <button class="btn btn-danger my-2 btn-lg boxbtn" type="submit"
                                @click="deletevenue(venue.venue_id)">Delete</button>
                        </div>
                    </div>
                </div>
            </div>
            <div id="popup">
                <p class="alert alert-danger fade show" v-if="derror">
                    {{ derror }}
                </p>
                <p class="alert alert-success fade show" role="alert" v-if="dsuccess">
                    {{ dsuccess }}
                </p>
            </div>
        </div>

    </div>

    <div class='addvenue' v-if="this.curr == 'addvenue'">

        <div id="popup">
            <p class="alert alert-danger fade show" v-if="aerror">
                {{ aerror }}
            </p>
            <p class="alert alert-success fade show" role="alert" v-if="asuccess">
                {{ asuccess }}
            </p>
        </div>

        <form ref="addvenueform" method="Post">

            <div class="field">
                <label class="label is-large" for="vname">Venue Name</label>
                <div class="control">
                    <input type="text" class="input is-large" id="vname" v-model="vname">
                </div>
            </div><br>

            <div class="field">
                <label class="label is-large" for="location">Location</label>
                <div class="control">
                    <input type="text" class="input is-large" id="location" v-model="location">
                </div>
            </div>
            <br>

            <div class="field">
                <label class="label is-large" for="capacity">Capacity</label>
                <div class="control">
                    <input type="number" class="input is-large" id="capacity" v-model="capacity">
                </div>
            </div>
            <br>

            <div class="control">
                <div class="btn1" @click="addvenue()">Add Venue</div> <br>
                <a @click="changemainvenue()">Go Back</a>
            </div>

        </form>
    </div>


    <div class='editvenue' v-if="this.curr == 'editvenue'">

        <div id="popup">
            <p class="alert alert-danger fade show" v-if="eerror">
                {{ eerror }}
            </p>
            <p class="alert alert-success fade show" role="alert" v-if="esuccess">
                {{ esuccess }}
            </p>
        </div>

        <form ref="editvenueform" method="Post">

            <div class="field">
                <label class="label is-large" for="vname">Venue Name</label>
                <div class="control">
                    <input type="text" class="input is-large" id="vname" v-bind:value="this.evenue.name"
                        v-on:input="$emit('input', $event.target.value)">
                </div>
            </div><br>

            <div class="field">
                <label class="label is-large" for="location">Location</label>
                <div class="control">
                    <input type="text" class="input is-large" id="location" v-bind:value="this.evenue.location"
                        v-on:input="$emit('input', $event.target.value)">
                </div>
            </div>
            <br>

            <div class="field">
                <label class="label is-large" for="capacity">Capacity</label>
                <div class="control">
                    <input type="number" class="input is-large" id="capacity" v-bind:value="this.evenue.capacity"
                        v-on:input="$emit('input', $event.target.value)">
                </div>
            </div>
            <br>

            <div class="control">
                <div class="btn1" @click="editvenue()">Edit Venue</div> <br>
                <a @click="changemainvenue()">Go Back</a>
            </div>

        </form>
    </div>
</template>


<script>

export default {
    name: "VenuePage",
    components: {
    },
    data() {
        return {
            name: null,
            email: null,
            auth_token: null,
            curr: null,
            aerror: null,
            asuccess: null,
            eerror: null,
            esuccess: null,
            derror: null,
            dsuccess: null,
            evenue: null,
        };
    },

    props: [
        'venues',
    ],

    async created() {
        this.auth_token = sessionStorage.getItem("auth-token");
        this.email = sessionStorage.getItem("email");
        this.name = sessionStorage.getItem("name");

        if (!this.auth_token) {
            alert("Please Login to see your dashboard.");
            this.$router.push("/");
        }

        this.curr = "mainvenue";

    },

    methods: {

        async changeaddvenue() {
            this.curr = 'addvenue';
        },

        async changemainvenue() {
            this.curr = 'mainvenue';
            this.$router.go();
            window.location.reload();
        },

        async changeeditvenue(ev) {
            this.curr = 'editvenue';
            this.evenue = ev;
        },

        async addvenue() {

            if (!this.$refs.addvenueform.vname.value) {
                this.aerror = "Venue Name must not be empty.";
            }
            else if (!this.$refs.addvenueform.location.value) {
                this.aerror = "Location must not be empty.";
            }
            else if (!this.$refs.addvenueform.capacity.value) {
                this.aerror = "Capacity must not be empty.";
            }
            else if (this.$refs.addvenueform.capacity.value <= 0) {
                this.aerror = "Capacity must be greater than 0.";
            }
            else {

                try {
                    const res = await fetch("http://127.0.0.1:5000/api/venue", {
                        mode: "cors",
                        method: "POST",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authentication-Token": `${this.auth_token}`,
                        },
                        body: JSON.stringify({
                            vname: this.$refs.addvenueform.vname.value,
                            location: this.$refs.addvenueform.location.value,
                            capacity: this.$refs.addvenueform.capacity.value,
                        }),
                    });

                    console.log(res);

                    if (res.ok) {
                        console.log("venue added");
                        this.aerror = null;
                        this.asuccess = "Venue has successfully been added.";
                    } else if (res.status === 400) {
                        this.aerror = "Venue name already exists.";
                    }
                } catch (error) {
                    console.log("Venue not added", error);
                }

            }

        },

        async editvenue() {
            console.log('edit form');
            if (!this.$refs.editvenueform.vname.value) {
                this.eerror = "Venue Name must not be empty.";
            }
            else if (!this.$refs.editvenueform.location.value) {
                this.eerror = "Location must not be empty.";
            }
            else if (!this.$refs.editvenueform.capacity.value) {
                this.eerror = "Capacity must not be empty.";
            }
            else if (this.$refs.editvenueform.capacity.value <= 0) {
                this.eerror = "Capacity must be greater than 0.";
            }
            else {

                try {
                    const res = await fetch("http://127.0.0.1:5000/api/venue/" + this.evenue.venue_id, {
                        mode: "cors",
                        method: "PUT",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authentication-Token": `${this.auth_token}`,
                        },
                        body: JSON.stringify({
                            vname: this.$refs.editvenueform.vname.value,
                            location: this.$refs.editvenueform.location.value,
                            capacity: this.$refs.editvenueform.capacity.value,
                        }),
                    });

                    console.log(res);

                    if (res.ok) {
                        console.log("venue edited");
                        this.evenue.name = this.$refs.editvenueform.vname.value;
                        this.evenue.location = this.$refs.editvenueform.location.value;
                        this.evenue.capacity = this.$refs.editvenueform.capacity.value;
                        this.eerror = null;
                        this.esuccess = "Venue has successfully been edited.";
                    } else if (res.status === 400) {
                        this.eerror = "Venue name already exists.";
                    }
                } catch (error) {
                    console.log("Venue not edited.", error);
                }

            }
        },

        async deletevenue(vid) {
            if (confirm("Are you sure you want to delete this venue?")) {
                try {
                    const res = await fetch("http://127.0.0.1:5000/api/venue/" + vid, {
                        mode: "cors",
                        method: "DELETE",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authentication-Token": `${this.auth_token}`,
                        },
                    });

                    console.log(res);

                    if (res.ok) {
                        console.log("venue deleted");
                        this.derror = null;
                        this.dsuccess = "Venue has successfully been deleted.";
                        this.$router.go();
                        window.location.reload();
                    } else if (res.status === 400) {
                        this.derror = "Venue could not be deleted.";
                    }
                } catch (error) {
                    console.log("Venue not deleted", error);
                }
            }
        }


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

label {
    font-size: 20px;
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

.venueclass {
    border-style: solid;
    border-color: black;
    border-radius: 3px;
    border-width: 1px;
    padding: 30px;
    width: 50%;
    margin-left: auto;
    margin-right: auto;
    margin-top: 20px;
    margin-bottom: 15px;
}

.venuehead {
    text-align: left;
    font-size: 45px;
    vertical-align: middle;
    display: inline-block;
}

.venuebody {
    font-size: 20px;

}

.boxbtn {
    width: 100px;
    margin: 10px;
}</style>



