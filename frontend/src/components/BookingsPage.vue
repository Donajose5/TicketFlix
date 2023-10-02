<template>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" />


    <div class='mainbooking' v-if="this.curr == 'mainbooking'">

        <br>
        <h1>Booking</h1><br><br>

        <div class="no" v-if="this.userbookings == true">
            No bookings available
        </div>

        <div v-else>

            <div id="popup">
                <p class="alert alert-danger fade show" v-if="eerror">
                    {{ eerror }}
                </p>
                <p class="alert alert-success fade show" role="alert" v-if="esuccess">
                    {{ esuccess }}
                </p>
            </div>

            <table class="table">
                <thead>
                    <tr>
                        <td> Booking ID </td>
                        <td> Movie </td>
                        <td> Venue </td>
                        <td> Location </td>
                        <td> Date </td>
                        <td> Time </td>
                        <td> Quantity </td>
                        <td> Total Price </td>
                        <td> Status </td>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="booking of userbookings" :key="booking.booking_id" class='displaybooking'>
                        <td> {{ booking.booking_id }}</td>
                        <td> {{ booking.movie_name }} </td>
                        <td> {{ booking.venue_name }} </td>
                        <td> {{ booking.venue_location }} </td>
                        <td> {{ booking.show_date }} </td>
                        <td> {{ booking.show_time }} </td>
                        <td> {{ booking.quantity }} </td>
                        <td> {{ booking.total_price }} </td>
                        <td> {{ booking.status }} </td>
                        <td class="btns" v-if="booking.status == 'Unconfirmed'">
                            <button class="btn btn-success my-2 btn-lg boxbtn" type="submit"
                                @click="changeeditbooking(booking)">Edit</button>
                        </td>
                        <td class="btns" v-if="booking.status == 'Unconfirmed'">
                            <button class="btn btn-primary my-2 btn-lg boxbtn" type="submit"
                                @click="confirm(booking)">Confirm</button>
                        </td>

                        <td v-if="booking.status == 'Confirmed'" colspan=2>
                            <!--<a v-if="booking.status == 'Confirmed'" @click="downloadticket(booking)">Download ticket here</a>-->
                        </td>

                        <td class="btns">
                            <button class="btn btn-danger my-2 btn-lg boxbtn" type="submit"
                                @click="deletebooking(booking)">Delete</button>
                        </td>

                    </tr>


                </tbody>
            </table>
            <a @click="changemainbooking()">Go Back</a>

        </div>
    </div>


    <div class="editbooking" v-if="this.curr == 'editbooking'">

        <br>
        <h1> Edit Booking </h1>
        <br>

        <div id="popup">
            <p class="alert alert-danger fade show" v-if="eerror">
                {{ eerror }}
            </p>
            <p class="alert alert-success fade show" role="alert" v-if="esuccess">
                {{ esuccess }}
            </p>
        </div>

        <form ref="editshowform" method="Post">

            <table class="formtable">
                <tr>
                    <td>Movie:</td>
                    <td>{{ ebooking.movie_name }}</td>
                </tr><br>

                <tr>
                    <td>Venue:</td>
                    <td>{{ ebooking.venue_name }}</td>
                </tr><br>

                <tr>
                    <td>Location:</td>
                    <td>{{ ebooking.venue_location }}</td>
                </tr><br>

                <tr>
                    <td>Date and Time:</td>
                    <td>{{ ebooking.show_date }}, {{ ebooking.show_time }}</td>
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
                        v-bind:max="this.ebooking.seats_available">
                </div>
            </div>
            <br>

            Price: {{ pricecalc }} <br><br>

            <div class="control">
                <div class="btn1" @click="editbooking()">Book</div> <br>
                <a @click="changemainbooking()">Go Back</a>
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
    var dateTime = year + '-' + month + '-' + day + ' ' + hour + ':' + minute ;
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
            quantity: null,
        };
    },

    props: [
        'movies',
        'venues',
        'shows',
        'display',
        'userbookings'
    ],
    computed: {

        pricecalc: function () {
            if ((this.ebooking.seats_available + this.ebooking.quantity) < this.quantity) {
                return '-';
            }
            return (this.quantity * this.ebooking.price)
        },

        remainingseats: function () {
            if ((this.ebooking.seats_available + this.ebooking.quantity) < this.quantity) {
                return '-';
            }
            return (this.ebooking.seats_available + this.ebooking.quantity - this.quantity)
        }
    },

    async created() {
        this.auth_token = sessionStorage.getItem("auth-token");
        this.email = sessionStorage.getItem("email");
        this.name = sessionStorage.getItem("name");

        if (!this.auth_token) {
            alert("Please Login to see your dashboard.");
            this.$router.push("/");
        }

        this.curr = "mainbooking";

        console.log(this.userbookings);

    },

    methods: {

        async changemainbooking() {
            await this.$router.go();
            await window.location.reload();
            this.curr = 'mainbooking';
        },

        async changeeditbooking(eb) {
            this.curr = 'editbooking';
            this.ebooking = eb;
            this.quantity = eb.quantity;
        },

        async editbooking() {
            console.log('edit booking');

            let currdate = getDateTime();
            console.log(currdate);

            if (!this.$refs.editshowform.quantity.value) {
                this.aerror = "Quantity must not be empty.";
            }
            else if (this.$refs.editshowform.quantity.value < 1) {
                this.aerror = "Quantity should be greated than 0.";
            }
            else if (this.$refs.editshowform.quantity.value > (this.ebooking.seats_available + this.ebooking.quantity)) {
                this.aerror = "Quantity should be less than the available tickets";
            }
            else {

                try {

                    const ress = await fetch("http://127.0.0.1:5000/api/show/" + this.ebooking.show_id, {
                        mode: "cors",
                        method: "PUT",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authentication-Token": `${this.auth_token}`,
                        },
                        body: JSON.stringify({
                            venue_id: this.ebooking.venue_id,
                            movie_id: this.ebooking.movie_id,
                            datetime: this.ebooking.show_datetime,
                            seats_available: (this.ebooking.seats_available + this.ebooking.quantity - this.quantity),
                            price: this.ebooking.price,
                        }),
                    });

                    console.log(ress);

                    if (ress.ok) {
                        console.log("show edited");
                    }


                    const res = await fetch("http://127.0.0.1:5000/api/booking/" + this.ebooking.booking_id, {
                        mode: "cors",
                        method: "PUT",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authentication-Token": `${this.auth_token}`,
                        },
                        body: JSON.stringify({
                            show_id: this.ebooking.show_id,
                            datetime: currdate,
                            quantity: this.quantity,
                            total_price: (this.ebooking.price * this.quantity),
                            status: this.ebooking.status,
                        }),
                    });

                    console.log(res);

                    if (res.ok) {
                        console.log("booking edited");
                        this.eerror = null;
                        this.esuccess = "Booking has successfully been edited.";
                    }
                } catch (error) {
                    console.log("Booking not edited", error);
                }
            }
        },

        async deletebooking(booking) {
            if (confirm("Are you sure you want to delete this booking?")) {
                console.log("delete booking");
                try {

                    const ress = await fetch("http://127.0.0.1:5000/api/show/" + booking.show_id, {
                        mode: "cors",
                        method: "PUT",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authentication-Token": `${this.auth_token}`,
                        },
                        body: JSON.stringify({
                            venue_id: booking.venue_id,
                            movie_id: booking.movie_id,
                            datetime: booking.show_datetime,
                            seats_available: (booking.seats_available + booking.quantity),
                            price: booking.price,
                        }),
                    });

                    console.log(ress);

                    if (ress.ok) {
                        console.log("show edited");
                    }


                    const res = await fetch("http://127.0.0.1:5000/api/booking/" + booking.booking_id, {
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
                        console.log("Booking deleted");
                        this.derror = null;
                        this.dsuccess = "Booking has successfully been deleted.";
                        this.$router.go();
                        window.location.reload();
                    } else if (res.status === 400) {
                        this.derror = "Booking could not be deleted.";
                    }
                } catch (error) {
                    console.log("Booking not deleted", error);
                }
            }
        },


        async confirm(booking) {
            console.log(booking);
            if (confirm("Do you want to confirm your booking?")) {
                try {
                    const res = await fetch("http://127.0.0.1:5000/api/booking/" + booking.booking_id, {
                        mode: "cors",
                        method: "PUT",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authentication-Token": `${this.auth_token}`,
                        },
                        body: JSON.stringify({
                            show_id: booking.show_id,
                            datetime: booking.booking_datetime,
                            quantity: booking.quantity,
                            total_price: booking.total_price,
                            status: "Confirmed",
                        }),
                    });

                    console.log(res);

                    if (res.ok) {
                        console.log("booking edited confirmed");

                        const ress = await fetch("http://127.0.0.1:5000/api/download/" + booking.booking_id, {
                            mode: "cors",
                            method: "GET",
                            headers: {
                                "Access-Control-Allow-Origin": "*",
                                "Content-Type": "application/json",
                                "Authentication-Token": `${this.auth_token}`,
                            },
                        });

                        console.log(ress);
                        if (ress.ok) {

                            this.eerror = null;
                            this.esuccess = "Booking has successfully been confirmed. Ticket has been sent your mail";
                        }
                    }
                } catch (error) {
                    console.log("Booking not confirmed", error);
                }
            }
        },

        async downloadticket(booking) {
            console.log("Download ticket");
            console.log(booking);
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

thead td {
    font-size: 20px;
    font-weight: bold;
}

tbody td {
    padding: 30px;
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

.btns {
    width: 100px;
}
</style>



