<template>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" />


    <div class='mainshow' v-if="this.curr == 'mainshow'">
        <br><br>
        <h1>Showings</h1><br><br>

        <div class="no" v-if="this.display == true">
            No Shows available
        </div>

        <div v-else>

            <table class="table">
                <thead>
                    <tr>
                        <td></td>
                        <td class='moviend'> Movie </td>
                        <td> Rating </td>
                        <td> Tags </td>
                        <td> Venue </td>
                        <td> Location </td>
                        <td> Date </td>
                        <td> Time </td>
                        <td> Price </td>
                        <td> Available Tickets </td>
                        <td></td>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="show of display" :key="show.show_id" class='displayshow'>
                        <td v-if="show.seats_available > 0"><img :src="show.poster" alt="Show image"></td>
                        <td class='moviend' v-if="show.seats_available > 0">
                            <h3>{{ show.movie_name }}</h3> <br>{{ show.description }}
                        </td>
                        <td v-if="show.seats_available > 0"> {{ show.rating }} </td>
                        <td v-if="show.seats_available > 0"> {{ show.tags }} </td>
                        <td v-if="show.seats_available > 0"> {{ show.venue_name }} </td>
                        <td v-if="show.seats_available > 0"> {{ show.venue_location }} </td>
                        <td v-if="show.seats_available > 0"> {{ show.date }} </td>
                        <td v-if="show.seats_available > 0"> {{ show.time }} </td>
                        <td v-if="show.seats_available > 0"> {{ show.price }} </td>
                        <td v-if="show.seats_available > 0"> {{ show.seats_available }} </td>
                        <td v-if="show.seats_available > 0">
                            <button class="btn btn-success my-2 btn-lg boxbtn" type="submit"
                                @click="changeaddbooking(show)">Book</button>
                        </td>
                    </tr>
                </tbody>
            </table>

        </div>

    </div>

    <div class='addbooking' v-if="this.curr == 'addbooking'">


        <br>
        <h1> Book Tickets </h1> <br>

        <div id="popup">
            <p class="alert alert-danger fade show" v-if="aerror">
                {{ aerror }}
            </p>
            <p class="alert alert-success fade show" role="alert" v-if="asuccess">
                {{ asuccess }}
            </p>
        </div>


        <form ref="addbookingform" method="Post">

            <table class="formtable">
                <tr>
                    <td>Movie:</td>
                    <td>{{ bshow.movie_name }}</td>
                </tr><br>

                <tr>
                    <td>Venue:</td>
                    <td>{{ bshow.venue_name }}</td>
                </tr><br>

                <tr>
                    <td>Location:</td>
                    <td>{{ bshow.venue_location }}</td>
                </tr><br>

                <tr>
                    <td>Date and Time:</td>
                    <td>{{ bshow.date }}, {{ bshow.time }}</td>
                </tr><br>

                <tr>
                    <td>Tickets Available:</td>
                    <td>{{ remainingseats }}</td>
                </tr><br>
            </table>



            <div class="field">
                <label class="label is-large" for="quantity">Quantity</label>
                <div class="control">
                    <input type="number" class="input is-large" id="quantity" v-model="quantity" min="1"
                        v-bind:max="this.bshow.seats_available">
                </div>
            </div>
            <br>

            Price: {{ pricecalc }} <br><br>

            <div class="control">
                <div class="btn1" @click="addbooking()">Book</div> <br>
                <a @click="changemainshow()">Go Back</a>
            </div>


        </form>
    </div>
</template>


<script>

function getDateTime() {
    var now = new Date();
    var year = now.getFullYear();
    var month = now.getMonth() + 1;
    var day = now.getDate();
    var hour = now.getHours();
    var minute = now.getMinutes();
    var second = now.getSeconds();
    if (month.toString().length == 1) {
        month = '0' + month;
    }
    if (day.toString().length == 1) {
        day = '0' + day;
    }
    if (hour.toString().length == 1) {
        hour = '0' + hour;
    }
    if (minute.toString().length == 1) {
        minute = '0' + minute;
    }
    if (second.toString().length == 1) {
        second = '0' + second;
    }
    var dateTime = year + '-' + month + '-' + day + ' ' + hour + ':' + minute;
    return dateTime;
}

export default {
    name: "UserShow",
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
            ebooking: null,
            bshow: null,
            quantity: null,
            tprice: null
        };
    },

    props: [
        'movies',
        'venues',
        'shows',
        'display'
    ],
    computed: {

        pricecalc: function () {
            if (this.bshow.seats_available < this.quantity) {
                return '-';
            }
            return (this.quantity * this.bshow.price)
        },

        remainingseats: function () {
            if (this.bshow.seats_available < this.quantity) {
                return '-';
            }
            return (this.bshow.seats_available - this.quantity)
        },
    },

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




        async changemainshow() {
            await this.$router.go();
            await window.location.reload();
            this.curr = 'mainshow';
        },

        async changeaddbooking(bs) {
            this.curr = 'addbooking';
            this.bshow = bs;

        },

        async checkshow(show) {
            if (show.seats_available > 0) {
                let currdate = getDateTime();
                let curr_date = currdate.substring(0, 10);
                let curr_time = currdate.substring(11, 16)
                console.log(curr_date);
                console.log(curr_time);
                console.log(show.date);
                console.log(show.time);
                /*
                const d1 = Date.parse(curr_date);
                const d2 = Date.parse(show.date);
                
                if(d1<d2)
                {    return true;
                }
                
                if (curr_date < show.date){
                    return true;
                }
                else if(curr_date == show.date) {
                    if(curr_time <= show.time) {
                        return true;
                    }
                }
                */
            }
            return false;
        },

        async addbooking() {

            console.log("add booking ");
            let currdate = getDateTime();
            console.log(currdate);

            console.log(this.bshow);

            if (!this.$refs.addbookingform.quantity.value) {
                this.aerror = "Quantity must not be empty.";
            }
            else if (this.$refs.addbookingform.quantity.value < 1) {
                this.aerror = "Quantity should be greated than 0.";
            }
            else if (this.$refs.addbookingform.quantity.value > this.bshow.seats_available) {
                this.aerror = "Quantity should be less than the available tickets";
            }
            else {

                try {
                    const ress = await fetch("http://127.0.0.1:5000/api/show/" + this.bshow.show_id, {
                        mode: "cors",
                        method: "PUT",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authentication-Token": `${this.auth_token}`,
                        },
                        body: JSON.stringify({
                            venue_id: this.bshow.venue_id,
                            movie_id: this.bshow.movie_id,
                            datetime: this.bshow.datetime,
                            seats_available: (this.bshow.seats_available - this.$refs.addbookingform.quantity.value),
                            price: this.bshow.price,
                            status: "unconfirmed",
                        }),
                    });

                    console.log(ress);

                    if (ress.ok) {
                        console.log("show edited");
                    }


                    const res = await fetch("http://127.0.0.1:5000/api/booking", {
                        mode: "cors",
                        method: "POST",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authentication-Token": `${this.auth_token}`,
                        },
                        body: JSON.stringify({
                            show_id: this.bshow.show_id,
                            datetime: currdate,
                            quantity: this.$refs.addbookingform.quantity.value,
                            total_price: (this.$refs.addbookingform.quantity.value * this.bshow.price),
                            status: "Unconfirmed"
                        }),
                    });

                    console.log(res);

                    if (res.ok) {
                        console.log("booking added");
                        this.aerror = null;
                        this.asuccess = "Booking has successfully been added.";
                        this.changemainshow();
                    }
                } catch (error) {
                    console.log("Booking not added", error);
                }
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

form {
    font-size: 20px;
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

.moviend {
    width: 300px;
}

thead td {
    font-size: 20px;
    font-weight: bold;
}

tbody td {
    padding: 30px;
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

img {
    width: 200px;
    height: auto;
}

.formtable {
    margin-left: auto;
    margin-right: auto;
}
</style>




