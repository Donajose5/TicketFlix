<template>
    <component :is="currentComponent" @changel="changel()" @changes="changes()" @signup="(signupData = $event), register()"
        @login="(loginData = $event), login()" :serror_1="signupData.error_1" :serror_2="signupData.error_2"
        :lerror_1="loginData.error_1" :lerror_2="loginData.error_2" :success="signupData.success"></component>
</template>
    
<script>
import StartPage from "@/components/StartPage.vue";
import LogIn from "@/components/LogIn.vue";
import SignUp from "@/components/SignUp.vue";

export default {
    name: "StartView",
    components: {
        StartPage,
        LogIn,
        SignUp,
    },

    data() {
        return {
            currentComponent: "StartPage",
            signupData: {
                email: null,
                name: null,
                password1: null,
                password2: null,
                error_1: "",
                error_2: "",
                success: "",
            },
            loginData: {
                email: null,
                password: null,
                error_1: "",
                error_2: "",
                auth: null,
                is_authenticated: false,
            },
            name: null,
            role_id: null,
        };
    },

    async created() {
        sessionStorage.clear();
        localStorage.clear();
    },

    async updated() {
        sessionStorage.clear();
        localStorage.clear();
    },


    methods: {

        async register() {
            console.log(this.signupData);
            this.signupData.error_1 = null;
            this.signupData.error_2 = null;
            this.signupData.success = null;
            if (
                this.emailValidation(this.signupData.email) &&
                this.passValidation(this.signupData.password1) &&
                this.passConfirmation(
                    this.signupData.password1,
                    this.signupData.password2
                )
            ) {
                try {
                    const res = await fetch("http://127.0.0.1:5000/api/user", {
                        mode: "cors",
                        method: "POST",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            email: this.signupData.email,
                            name: this.signupData.name,
                            password1: this.signupData.password1,
                        }),
                    });

                    console.log(res);

                    if (res.ok) {
                        console.log("registered");
                        this.signupData.success =
                            "Registered succesfully! Log in to continue.";
                    } else if (res.status === 400) {
                        this.signupData.error_1 = "Email already exists!! Try again.";
                    } else {
                        this.signupData.error_1 = "Registration Failed!! Try again.";
                        throw new Error("Registration failed");
                    }
                } catch (error) {
                    console.log("Registration Failed: ", error);
                }
            } else if (!this.emailValidation(this.signupData.email)) {
                this.signupData.error_1 = "Please enter a valid email";
            } else if (!this.passValidation(this.signupData.password1)) {
                this.signupData.error_1 = "Password requires atleast 8 characters.";
            } else if (!this.passConfirmation(this.signupData.password1, this.signupData.password2)) {
                this.signupData.error_1 = "The passwords need to match.";
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

        async login() {
            console.log("login");
            this.loginData.error_2 = null;
            this.loginData.error_1 = null;
            try {
                fetch("http://127.0.0.1:5000/login?include_auth_token", {
                    mode: "cors",
                    method: "POST",
                    headers: {
                        "Access-Control-Allow-Origin": "*",
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        email: this.loginData.email,
                        password: this.loginData.password,
                        is_authenticated: true,
                    }),
                })
                    .then((resp) => resp.json())
                    .then(async (data) => {
                        const { response } = data;
                        if (response.errors) {
                            if (response.errors[1]) {
                                this.loginData.error_1 = response.errors[1];
                            }
                            this.loginData.error_2 = response.errors[0];
                            console.log(this.loginData.error_1, this.loginData.error_2);
                        } else {

                            this.loginData.auth = response.user.authentication_token;
                            sessionStorage.setItem("auth-token", this.loginData.auth);

                            await fetch("http://127.0.0.1:5000/api/user", {
                                mode: "cors",
                                method: "GET",
                                headers: {
                                    "Access-Control-Allow-Origin": "*",
                                    "Content-Type": "application/json",
                                    "Authentication-Token": `${this.loginData.auth}`,
                                },
                            })
                                .then((response) => response.json())
                                .then((data) => {
                                    this.name = data["name"];
                                    this.role_id = data["role"];
                                })
                                .catch((error) => console.log("1st", error));

                            sessionStorage.setItem("email", this.loginData.email);
                            sessionStorage.setItem("name", this.name);
                            sessionStorage.setItem("role_id", this.role_id);
                            
                            if (this.role_id == 1) {
                            console.log("admin");
                                this.$router.push("admin");
                            }
                            else {
                                this.$router.push("home");
                            }
                        }
                    })
                    .catch((error) => {
                        console.log("some error occured", error);
                    });
            } catch (error) {
                console.log("Error. Could not log in.", error);
            }
        },

        async changel() {
            this.currentComponent = 'LogIn';
        },

        async changes() {
            this.currentComponent = 'SignUp';
        },
    },
};
</script>
