<template>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" />

    <br><br>
    <h1>Movies</h1><br>

    <div class='mainmovie' v-if="this.curr == 'mainmovie'">

        <button class="btn btn-primary my-2 btn-lg add" type="submit" @click="changeaddmovie()">Add a new Movie</button>


        <div class="no" v-if="this.movies == true">
            No Movies available
        </div>

        <div v-else>
            <div v-for="movie of movies" :key="movie.movie_id" class='movieclass'>
                <div class='container'>
                    <div class='row'>
                        <div class='col'>
                            <img :src="movie.poster" alt="Show image">
                        </div>
                        <div class='col moviedetails'>
                            <div class='moviebody'>
                                <h2>{{ movie.name }}</h2> <br>
                                <b> Rating: {{movie.rating}} </b><br>
                                {{ movie.description }}<br>
                                Duration: {{movie.duration}} minutes<br>
                                Tags: {{ movie.tags }} <br>
                            </div>
                        </div>
                        <div class='col edbtns'>
                            <button class="btn btn-success my-2 btn-lg boxbtn" type="submit"
                                @click="changeeditmovie(movie)">Edit</button>
                            <button class="btn btn-danger my-2 btn-lg boxbtn" type="submit"
                                @click="deletemovie(movie.movie_id)">Delete</button>
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

    <div class='addmovie' v-if="this.curr == 'addmovie'">

        <div id="popup">
            <p class="alert alert-danger fade show" v-if="aerror">
                {{ aerror }}
            </p>
            <p class="alert alert-success fade show" role="alert" v-if="asuccess">
                {{ asuccess }}
            </p>
        </div>

        <form ref="addmovieform" method="Post">

            <div class="field">
                <label class="label is-large" for="name">Movie Name</label>
                <div class="control">
                    <input type="text" class="input is-large" id="name" v-model="mname">
                </div>
            </div><br>

            <div class="field">
                <label class="label is-large" for="poster">Poster</label>
                <div class="control">
                    <input type="text" class="input is-large" id="poster" v-model="poster">
                </div>
            </div>
            <br>
            
            <div class="field">
                <label class="label is-large" for="description">Description</label>
                <div class="control">
                    <input type="text" class="input is-large" id="description" v-model="description">
                </div>
            </div>
            <br>

            <div class="field">
                <label class="label is-large" for="duration">Duration</label>
                <div class="control">
                    <input type="number" class="input is-large" id="duration" v-model="duration">
                </div>
            </div>
            <br>
            
            <div class="field">
                <label class="label is-large" for="rating">Rating</label>
                <div class="control">
                    <input type="number" class="input is-large" id="rating" v-model="rating" min="0" max="10" step="0.1">
                </div>
            </div>
            <br>
            
            <div class="field">
                <label class="label is-large" for="tags">Tags</label>
                <div class="control">
                    <input type="text" class="input is-large" id="tags" v-model="tags">
                </div>
            </div>
            <br>

            <div class="control">
                <div class="btn1" @click="addmovie()">Add Movie</div> <br>
                <a @click="changemainmovie()">Go Back</a>
            </div>

        </form>
    </div>


    <div class='editmovie' v-if="this.curr == 'editmovie'">

        <div id="popup">
            <p class="alert alert-danger fade show" v-if="eerror">
                {{ eerror }}
            </p>
            <p class="alert alert-success fade show" role="alert" v-if="esuccess">
                {{ esuccess }}
            </p>
        </div>

        <form ref="editmovieform" method="Post">
        
            <div class="field">
                <label class="label is-large" for="name">Movie Name</label>
                <div class="control">
                    <input type="text" class="input is-large" id="name" v-bind:value="this.emovie.name" v-on:input="$emit('input', $event.target.value)">
                </div>
            </div><br>

            <div class="field">
                <label class="label is-large" for="poster">Poster</label>
                <div class="control">
                    <input type="text" class="input is-large" id="poster" v-bind:value="this.emovie.poster" v-on:input="$emit('input', $event.target.value)">
                </div>
            </div>
            <br>
            
            <div class="field">
                <label class="label is-large" for="description">Description</label>
                <div class="control">
                    <input type="text" class="input is-large" id="description" v-bind:value="this.emovie.description" v-on:input="$emit('input', $event.target.value)">
                </div>
            </div>
            <br>

            <div class="field">
                <label class="label is-large" for="duration">Duration</label>
                <div class="control">
                    <input type="number" class="input is-large" id="duration" v-bind:value="this.emovie.duration" v-on:input="$emit('input', $event.target.value)">
                </div>
            </div>
            <br>
            
            <div class="field">
                <label class="label is-large" for="rating">Rating</label>
                <div class="control">
                    <input type="number" class="input is-large" id="rating" min="0" max="10" step="0.1" v-bind:value="this.emovie.rating" v-on:input="$emit('input', $event.target.value)">
                </div>
            </div>
            <br>
                  
            <div class="field">
                <label class="label is-large" for="tags">Tags</label>
                <div class="control">
                    <input type="text" class="input is-large" id="tags" v-bind:value="this.emovie.tags" v-on:input="$emit('input', $event.target.value)">
                </div>
            </div>
            <br>

            <div class="control">
                <div class="btn1" @click="editmovie()">Edit Movie</div> <br>
                <a @click="changemainmovie()">Go Back</a>
            </div>

        </form>
    </div>
</template>


<script>

export default {
    name: "MoviePage",
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
            emovie: null,
        };
    },

    props: [
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

        this.curr = "mainmovie";

    },

    methods: {

        async changeaddmovie() {
            this.curr = 'addmovie';
        },

        async changemainmovie() {
            this.curr = 'mainmovie';
            this.$router.go();
            window.location.reload();
        },

        async changeeditmovie(em) {
            this.curr = 'editmovie';
            this.emovie = em;
        },

        async addmovie() {
        
        console.log("add movie ");

            if (!this.$refs.addmovieform.name.value) {
                this.aerror = "Movie Name must not be empty.";
            }
            else if (!this.$refs.addmovieform.duration.value) {
                this.aerror = "Duration must not be empty.";
            }
            else if (this.$refs.addmovieform.duration.value <= 0) {
                this.aerror = "Duration must be greater than 0.";
            }
            else if (!this.$refs.addmovieform.rating.value) {
                this.aerror = "Rating must not be empty.";
            }
            else if (this.$refs.addmovieform.rating.value < 0) {
                this.aerror = "Rating must be greater than or equal to 0.";
            }
            else if (this.$refs.addmovieform.rating.value > 10) {
                this.aerror = "Rating must be less than or equal to 10.";
            }
            else {

                try {
                    const res = await fetch("http://127.0.0.1:5000/api/movie", {
                        mode: "cors",
                        method: "POST",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authentication-Token": `${this.auth_token}`,
                        },
                        body: JSON.stringify({
                            name: this.$refs.addmovieform.name.value,
                            poster: this.$refs.addmovieform.poster.value,
                            description: this.$refs.addmovieform.description.value,
                            duration: this.$refs.addmovieform.duration.value,
                            rating: this.$refs.addmovieform.rating.value,
                            tags: this.$refs.addmovieform.tags.value,
                        }),
                    });

                    console.log(res);

                    if (res.ok) {
                        console.log("movie added");
                        this.aerror = null;
                        this.asuccess = "Movie has successfully been added.";
                    } 
                } catch (error) {
                    console.log("Movie not added", error);
                }

            }

        },

        async editmovie() {
            console.log('edit form');
            if (!this.$refs.editmovieform.name.value) {
                this.eerror = "Movie Name must not be empty.";
            }
            else if (!this.$refs.editmovieform.duration.value) {
                this.eerror = "Duration must not be empty.";
            }
            else if (this.$refs.editmovieform.duration.value <= 0) {
                this.eerror = "Duration must be greater than 0.";
            }
            else if (!this.$refs.editmovieform.rating.value) {
                this.eerror = "Rating must not be empty.";
            }
            else if (this.$refs.editmovieform.rating.value < 0) {
                this.eerror = "Rating must be greater than or equal to 0.";
            }
            else if (this.$refs.editmovieform.rating.value > 10) {
                this.eerror = "Rating must be less than or equal to 10.";
            }
            else {

                try {
                    const res = await fetch("http://127.0.0.1:5000/api/movie/" + this.emovie.movie_id, {
                        mode: "cors",
                        method: "PUT",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authentication-Token": `${this.auth_token}`,
                        },
                        body: JSON.stringify({
                            name: this.$refs.editmovieform.name.value,
                            poster: this.$refs.editmovieform.poster.value,
                            description: this.$refs.editmovieform.description.value,
                            duration: this.$refs.editmovieform.duration.value,
                            rating: this.$refs.editmovieform.rating.value,
                            tags: this.$refs.editmovieform.tags.value,
                        }),
                    });

                    console.log(res);

                    if (res.ok) {
                        console.log("movie edited");
                        this.emovie.name = this.$refs.editmovieform.name.value;
                        this.emovie.poster = this.$refs.editmovieform.poster.value;
                        this.emovie.description = this.$refs.editmovieform.description.value;
                        this.emovie.duration = this.$refs.editmovieform.duration.value;
                        this.emovie.rating = this.$refs.editmovieform.rating.value;
                        this.emovie.tags = this.$refs.editmovieform.tags.value;
                        this.eerror = null;
                        this.esuccess = "Movie has successfully been edited.";
                    }
                } catch (error) {
                    console.log("Movie not edited.", error);
                }

            }
        },

        async deletemovie(mid) {
            if (confirm("Are you sure you want to delete this movie?")) {
                try {
                    const res = await fetch("http://127.0.0.1:5000/api/movie/" + mid, {
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
                        console.log("movie deleted");
                        this.derror = null;
                        this.dsuccess = "Movie has successfully been deleted.";
                        this.$router.go();
                        window.location.reload();
                    } else if (res.status === 400) {
                        this.derror = "Movie could not be deleted.";
                    }
                } catch (error) {
                    console.log("Movie not deleted", error);
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

.movieclass {
    border-style: solid;
    border-color: black;
    border-radius: 3px;
    border-width: 1px;
    padding: 30px;
    width: 60%;
    margin-left: auto;
    margin-right: auto;
    margin-top: 20px;
    margin-bottom: 15px;
}

.moviehead {
    text-align: left;
    font-size: 45px;
    vertical-align: middle;
    display: inline-block;
}

.moviebody {
    font-size: 20px;

}

.boxbtn {
    width: 100px;
    margin: 10px;
}

.moviedetails {

}

img {
width: 250px;
height: auto;
}

.edbtns {
width: 10px;
}
</style>



