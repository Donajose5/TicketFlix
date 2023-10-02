<template>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" />

    <br><br>
    <h1>Showings</h1><br>

    <div class='mainshow' v-if="this.curr == 'mainshow'">

        <button class="btn btn-primary my-2 btn-lg add" type="submit" @click="changeaddshow()">Add a new Show</button>


        <div class="no" v-if="this.shows == true">
            No Shows available
        </div>

        <div v-else>
            <div v-for="show of shows" :key="show.show_id" class='showclass'>
                <div class='container'>
                    <div class='row'>
                        <div class='col'>
                            <div class='showbody'>
                                <h2> {{ show.movie_name }} </h2>
                                Venue: {{ show.venue_name }} <br>
                                Date: {{ show.date }} {{show.time}} <br>
                                Seats Available: {{ show.seats_available }} <br>
                                Price: Rs. {{ show.price }}
                            </div>
                        </div>
                        <div class='col edbtns'>
                            <button class="btn btn-success my-2 btn-lg boxbtn" type="submit"
                                @click="changeeditshow(show)">Edit</button>
                            <button class="btn btn-danger my-2 btn-lg boxbtn" type="submit"
                                @click="deleteshow(show.show_id)">Delete</button>
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

    <div class='addshow' v-if="this.curr == 'addshow'">

        <div id="popup">
            <p class="alert alert-danger fade show" v-if="aerror">
                {{ aerror }}
            </p>
            <p class="alert alert-success fade show" role="alert" v-if="asuccess">
                {{ asuccess }}
            </p>
        </div>

        <form ref="addshowform" method="Post">
        
        <div class="formselect">
            <div class="field">
                <label class="label is-large" for="selectmovie">Select Movie</label>
                <div class="control">
                    <select class="form-select" id="selectmovie" v-model="showmovie">
                        <option v-for="movie in movies" :key="movie.movie_id" :value="movie.movie_id">{{ movie.name }}
                        </option>
                    </select>
                </div>
            </div><br>

            <div class="field">
                <label class="label is-large" for="selectvenue">Select Venue</label>
                <div class="control">
                    <select class="form-select" id="selectvenue" v-model="showvenue">
                        <option v-for="venue in venues" :key="venue.venue_id" :value="venue.venue_id">{{ venue.name }}
                        </option>
                    </select>
                </div>
            </div><br>
            </div>

            <div class="field">
                <label class="label is-large" for="datetime">Date and Time</label>
                <div class="control">
                    <input type="datetime-local" id="datetime" name="datetime">
                </div>
            </div>
            <br>

            <div class="field">
                <label class="label is-large" for="price">Price</label>
                <div class="control">
                    <input type="number" class="input is-large" id="price" v-model="price" min="0.01" step="0.01">
                </div>
            </div>
            <br>

            <div class="control">
                <div class="btn1" @click="addshow()">Add Show</div> <br>
                <a @click="changemainshow()">Go Back</a>
            </div>

        </form>
    </div>


    <div class='editshow' v-if="this.curr == 'editshow'">

        <div id="popup">
            <p class="alert alert-danger fade show" v-if="eerror">
                {{ eerror }}
            </p>
            <p class="alert alert-success fade show" role="alert" v-if="esuccess">
                {{ esuccess }}
            </p>
        </div>

        <form ref="editshowform" method="Post">

            
            <div class="formselect">
            <div class="field">
                <label class="label is-large" for="selectmovie">Select Movie</label>
                <div class="control">
                    <select class="form-select" id="selectmovie" >
                        <option :key="this.eshow.movie_id" v-bind:value="this.eshow.movie_id" v-on:input="$emit('input', $event.target.value)" disabled selected hidden> {{this.eshow.movie_name}} </option>
                        <option v-for="movie in movies" :key="movie.movie_id" :value="movie.movie_id">{{ movie.name }}
                        </option>
                    </select>
                </div>
            </div><br>

            <div class="field">
                <label class="label is-large" for="selectvenue">Select Venue</label>
                <div class="control">
                    <select class="form-select" id="selectvenue" v-bind:value="this.eshow.venue_id" v-on:input="$emit('input', $event.target.value)">
                        <option :key="this.eshow.venue_id" v-bind:value="this.eshow.venue_name" v-on:input="$emit('input', $event.target.value)" disabled selected hidden> {{this.eshow.venue_name}} </option>
                        <option v-for="venue in venues" :key="venue.venue_id" :value="venue.venue_id">{{ venue.name }}
                        </option>
                    </select>
                </div>
            </div><br>
            </div>

            <div class="field">
                <label class="label is-large" for="datetime">Date and Time</label>
                <div class="control">
                    <input type="datetime-local" id="datetime" name="datetime" v-bind:value="this.eshow.datetime" v-on:input="$emit('input', $event.target.value)">
                </div>
            </div>
            <br>

            <div class="field">
                <label class="label is-large" for="price">Price</label>
                <div class="control">
                    <input type="number" class="input is-large" id="price" min="0.01" step="0.01" v-bind:value="this.eshow.price" v-on:input="$emit('input', $event.target.value)">
                </div>
            </div>
            <br>
            
            
            <div class="control">
                <div class="btn1" @click="editshow()">Edit Show</div> <br>
                <a @click="changemainshow()">Go Back</a>
            </div>

        </form>
    </div>
</template>


<script>

export default {
    name: "ShowPage",
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
            eshow: null,
        };
    },

    props: [
        'movies',
        'venues',
        'shows'
    ],

    async created() {
        this.auth_token = sessionStorage.getItem("auth-token");
        this.email = sessionStorage.getItem("email");
        this.name = sessionStorage.getItem("name");

        if (!this.auth_token) {
            alert("Please Login to see your dashboard.");
            this.$router.push("/");
        }

        this.curr = "mainshow";

    },

    methods: {

        async changeaddshow() {
            this.curr = 'addshow';
        },

        async changemainshow() {
            await this.$router.go();
            await window.location.reload();
            this.curr = 'mainshow';
            this.currentComponent = 'ShowPage';
            console.log(this.currentComponent);
        },

        async changeeditshow(es) {
            this.curr = 'editshow';
            this.eshow = es;
        },

        async addshow() {

            console.log("add show ");
            let currdate = new Date().toJSON();
            console.log(currdate);
            
            if (!this.$refs.addshowform.selectmovie.value) {
                this.aerror = "Movie Name must not be empty.";
            }
            else if (!this.$refs.addshowform.selectvenue.value) {
                this.aerror = "Venue must not be empty.";
            }
            else if (!this.$refs.addshowform.datetime.value) {
                this.aerror = "Date and time must not be empty.";
            }
            else if (!this.$refs.addshowform.price.value) {
                this.aerror = "Price must not be empty.";
            }
            else if (this.$refs.addshowform.datetime.value < currdate) {
                this.aerror = "Date and time is incorrect.";
            }
            else if (this.$refs.addshowform.price.value <= 0) {
                this.aerror = "Price should be greated than 0";
            }
            else {

                try {
                    const res = await fetch("http://127.0.0.1:5000/api/show", {
                        mode: "cors",
                        method: "POST",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authentication-Token": `${this.auth_token}`,
                        },
                        body: JSON.stringify({
                            venue_id: this.$refs.addshowform.selectvenue.value,
                            movie_id: this.$refs.addshowform.selectmovie.value,
                            datetime: this.$refs.addshowform.datetime.value,
                            price: this.$refs.addshowform.price.value,
                        }),
                    });

                    console.log(res);

                    if (res.ok) {
                        console.log("show added");
                        this.aerror = null;
                        this.asuccess = "Show has successfully been added.";
                    } 
                } catch (error) {
                    console.log("Show not added", error);
                }
            }
        },

        async editshow() {
            console.log('edit show');
            
            let currdate = new Date().toJSON();
            console.log(currdate);
            
            if (!this.$refs.editshowform.selectmovie.value) {
                this.aerror = "Movie Name must not be empty.";
            }
            else if (!this.$refs.editshowform.selectvenue.value) {
                this.aerror = "Venue must not be empty.";
            }
            else if (!this.$refs.editshowform.datetime.value) {
                this.aerror = "Date and time must not be empty.";
            }
            else if (!this.$refs.editshowform.price.value) {
                this.aerror = "Price must not be empty.";
            }
            else if (this.$refs.editshowform.datetime.value < currdate) {
                this.aerror = "Date and time is incorrect.";
            }
            else if (this.$refs.editshowform.price.value <= 0) {
                this.aerror = "Price should be greated than 0";
            }
            else {

                try {
                    const res = await fetch("http://127.0.0.1:5000/api/show/"+this.eshow.show_id, {
                        mode: "cors",
                        method: "PUT",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authentication-Token": `${this.auth_token}`,
                        },
                        body: JSON.stringify({
                            venue_id: this.$refs.editshowform.selectvenue.value,
                            movie_id: this.$refs.editshowform.selectmovie.value,
                            datetime: this.$refs.editshowform.datetime.value,
                            seats_available: this.eshow.seats_available,
                            price: this.$refs.editshowform.price.value,
                        }),
                    });

                    console.log(res);

                    if (res.ok) {
                        console.log("show edited");
                        this.eerror = null;
                        this.esuccess = "Show has successfully been added.";
                    } 
                } catch (error) {
                    console.log("Show not edited", error);
                }
            }
        },

        async deleteshow(sid) {
            if (confirm("Are you sure you want to delete this movie?")) {
                console.log("delete show");
                try {
                    const res = await fetch("http://127.0.0.1:5000/api/show/" + sid, {
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
                        console.log("Show deleted");
                        this.derror = null;
                        this.dsuccess = "Show has successfully been deleted.";
                        this.$router.go();
                        window.location.reload();
                    } else if (res.status === 400) {
                        this.derror = "Show could not be deleted.";
                    }
                } catch (error) {
                    console.log("Show not deleted", error);
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

.formselect {
width: 20%;
margin-left: auto;
margin-right: auto;
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

.showclass {
    border-style: solid;
    border-color: black;
    border-radius: 3px;
    border-width: 1px;
    padding: 30px;
    width: 35%;
    margin-left: auto;
    margin-right: auto;
    margin-top: 20px;
    margin-bottom: 15px;
}

.showhead {
    text-align: left;
    font-size: 45px;
    vertical-align: middle;
    display: inline-block;
}

.showbody {
    font-size: 20px;

}

.boxbtn {
    width: 100px;
    margin: 10px;
}
</style>



