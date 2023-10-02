<template>

<div class="mainprofile" v-if="this.curr == 'mainprofile'"> 
<br><br>

<h1>Profile</h1>
<br>

<div id="popup">
            <p class="alert alert-danger fade show" v-if="eerror">
                {{ derror }}
            </p>
            <p class="alert alert-success fade show" role="alert" v-if="esuccess">
                {{ dsuccess }}
            </p>
</div>

<table class="profileinfo">
<tr>
<td> Name: </td>
<td> {{this.name}} </td>
</tr>
<tr>
<td> Email ID: </td>
<td> {{this.email}} </td>
</tr>
</table>
<br><br>

<button class="btn btn-success my-2 btn-lg boxbtn2" type="submit" @click="changeeditprofile()">Edit Profile</button> <br>
<!--<button class="btn btn-primary my-2 btn-lg boxbtn2" type="submit" @click="changechangepassword()">Change Password</button> <br> -->
<button class="btn btn-danger my-2 btn-lg boxbtn2" type="submit" @click="deleteaccount()">Delete Account</button>

</div>

<div class="changepass" v-if="this.curr == 'changepass'">

        <br>
        <h1> Change Password </h1>
        <br>

        <div id="popup">
            <p class="alert alert-danger fade show" v-if="eerror">
                {{ eerror }}
            </p>
            <p class="alert alert-success fade show" role="alert" v-if="esuccess">
                {{ esuccess }}
            </p>
        </div>

        <form ref="changepasswordform" method="Post">

            <div class="field">
                <label class="label is-large" for="currentpassword">Current Password</label>
                <div class="control">
                    <input type="password" class="input is-large" id="currentpassword" >
                </div>
            </div><br>
            
            <div class="field">
                <label class="label is-large" for="newpassword1">New Password</label>
                <div class="control">
                    <input type="password" class="input is-large" id="newpassword1" >
                </div>
            </div><br>
            
            <div class="field">
                <label class="label is-large" for="newpassword2">Confirm new Password</label>
                <div class="control">
                    <input type="password" class="input is-large" id="newpassword2" >
                </div>
            </div>
            <br>
            
            <div class="control">
                <div class="btn1" @click="changepassword()">Change Password</div> <br>
                <a @click="changemainprofile()">Go Back</a>
            </div>
            

        </form>

    </div>


<div class="editprofile" v-if="this.curr == 'editprofile'">

        <br>
        <h1> Edit Profile </h1>
        <br>

        <div id="popup">
            <p class="alert alert-danger fade show" v-if="eerror">
                {{ eerror }}
            </p>
            <p class="alert alert-success fade show" role="alert" v-if="esuccess">
                {{ esuccess }}
            </p>
        </div>

        <form ref="editprofileform" method="Post">

            <div class="field">
                <label class="label is-large" for="name">Name</label>
                <div class="control">
                    <input type="text" class="input is-large" id="name" v-bind:value="this.name">
                </div>
            </div><br>
            
            <div class="field">
                <label class="label is-large" for="email">Email ID</label>
                <div class="control">
                    <input type="text" class="input is-large" id="email" v-bind:value="this.email">
                </div>
            </div><br>

            <div class="control">
                <div class="btn1" @click="editprofile()">Edit Profile</div> <br>
                <a @click="changemainprofile()">Go Back</a>
            </div>

        </form>

    </div>

</template>


<script>

export default {
    name: "ProfilePage",
    components: {
    },
    data() {
        return {
            name: null,
            email: null,
            auth_token: null,
            curr: null,
            eerror: null,
            esuccess: null,
            derror: null,
            dsuccess: null,
        };
    },

    props: [
    'user_id',
    'password',
    'userbookings',
    ],

    async created() {
        this.auth_token = sessionStorage.getItem("auth-token");
        this.email = sessionStorage.getItem("email");
        this.name = sessionStorage.getItem("name");

        if (!this.auth_token) {
            alert("Please Login to see your dashboard.");
            this.$router.push("/");
        }

        this.curr = "mainprofile";
    },

    methods: {

        async changemainprofile() {
            await this.$router.go();
            await window.location.reload();
            this.curr = 'mainprofile';
        },

        async changeeditprofile() {
            this.curr = 'editprofile';
        },
        
        async changechangepassword() {
            this.curr = 'changepass';
        },

        async editprofile() {
            console.log('edit profile');


            if (!this.$refs.editprofileform.name.value) {
                this.eerror = "Name must not be empty.";
            }
            else if (!this.$refs.editprofileform.email.value) {
                this.eerror = "Email must not be empty.";
            }
            else if (!this.emailValidation(this.$refs.editprofileform.email.value)) {
                this.eerror = "Enter a valid email ID.";
            }
            else {

                try {
                    const res = await fetch("http://127.0.0.1:5000/api/user/" + this.user_id, {
                        mode: "cors",
                        method: "PUT",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authentication-Token": `${this.auth_token}`,
                        },
                        body: JSON.stringify({
                            name: this.$refs.editprofileform.name.value,
                            email: this.$refs.editprofileform.email.value,
                            password: this.password,
                        }),
                    });

                    console.log(res);

                    if (res.ok) {
                        console.log("profile edited");
                        this.eerror = null;
                        this.esuccess = "Profile has successfully been edited.";
                        sessionStorage.setItem("email", this.$refs.editprofileform.email.value);
                        sessionStorage.setItem("name", this.$refs.editprofileform.name.value);
                        this.name = this.$refs.editprofileform.name.value;
                        this.email = this.$refs.editprofileform.email.value;
                    }
                } catch (error) {
                    console.log("Profile not edited", error);
                }
            }
        },

        async deleteaccount() {
            if (confirm("Are you sure you want to delete this Account?")) {
                console.log("delete account");
                try {
                
                console.log("deleetetete");
                for(let booking of this.userbookings){
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
                }
                
                const res = await fetch("http://127.0.0.1:5000/api/user/" + this.user_id, {
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
                        console.log("Account deleted");
                        this.derror = null;
                        this.dsuccess = "Account has successfully been deleted.";
            sessionStorage.clear();
            localStorage.clear();
            this.$router.push("/");
                    } else if (res.status === 400) {
                        this.derror = "Account could not be deleted.";
                    }
                    
                } catch (error) {
                    console.log("Account not deleted", error);
                }
            }
        },
        
        
        async changepassword() {
            console.log('edit profile');


            if (!this.$refs.changepasswordform.currentpassword.value) {
                this.eerror = "Current Password must not be empty.";
            }
            else if (!this.passConfirmation(this.$refs.changepasswordform.currentpassword.value, this.password)) {
                this.eerror = "Password is incorrect";
            }
            else if (!this.$refs.changepasswordform.newpassword1.value) {
                this.eerror = "Passwords must not be empty.";
            }
            else if (!this.$refs.changepasswordform.newpassword2.value) {
                this.eerror = "Passwords must not be empty.";
            }
            else if (!this.passValidation(this.$refs.changepasswordform.newpassword1.value)) {
                this.eerror = "Passwords requires at least 8 characters";
            }
            else if (!this.passConfirmation(this.$refs.changepasswordform.newpassword1.value, this.$refs.changepasswordform.newpassword2.value)) {
                this.eerror = "The passwords must match.";
            }
            else {

                try {
                    const res = await fetch("http://127.0.0.1:5000/api/user/" + this.user_id, {
                        mode: "cors",
                        method: "PUT",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authentication-Token": `${this.auth_token}`,
                        },
                        body: JSON.stringify({
                            name: this.$refs.editprofileform.name.value,
                            email: this.$refs.editprofileform.email.value,
                            password: this.$refs.changepasswordform.currentpassword.value,
                        }),
                    });

                    console.log(res);

                    if (res.ok) {
                        console.log("profile edited");
                        this.eerror = null;
                        this.esuccess = "Password has successfully been changed.";
                    }
                } catch (error) {
                    console.log("Password not changed", error);
                }
            }
        },
        
        emailValidation: function (email) {
            var result = /[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+/;
            return result.test(email);
        },

        passValidation: function (passs) {
            var result = /.{8,}/;
            return result.test(passs);
        },

        passConfirmation: function (passs1, passs2) {
            if (passs1 == passs2) {
                return true;
            }
            return false;
        },



    },
};
</script>

<style>
* {
    text-align: center;
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

table{
margin-left: auto;
margin-right: auto;
}

.profileinfo{
font-size:25px;
}

td {
    padding-left: 15px;
    padding-right: 15px;
}

.boxbtn2 {
    width: 200px;
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



