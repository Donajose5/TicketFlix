<template>
    <div class='bd'>
<link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css"
    />
        <div class='head'>
            Log In
        </div>

        <div id="popup">
            <p class="alert alert-danger alert-dismissible fade show" v-if="lerror_1">
                {{ lerror_1 }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </p>
            <p class="alert alert-danger alert-dismissible fade show" v-if="lerror_2">
                {{ lerror_2 }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </p>
        </div>

        <div class='main'>

            <form ref="loginform" method="Post">

                <div class="field">
                    <label class="label is-large" for="email">Email</label>
                    <div class="control">
                        <input type="email" class="input is-large" id="email" v-model="email">
                    </div>
                </div><br>

                <div class="field">
                    <label class="label is-large" for="password">Password</label>
                    <div class="control">
                        <input type="password" class="input is-large" id="password" v-model="password">
                    </div>
                </div>
                <br>

                <div class="control">
                    <div class="btn1" @click.prevent="fill(); $emit('login', loginData)">Login</div> <br>
                    <a @click.prevent=" $emit('changes');">Click here to Register</a>
                </div>

            </form>
        </div>


    </div>
</template>
    
<script>
export default {
    name: "LogIn",
    data() {
        return {
            loginData: {
                email: null,
                password: null,
                error_1: "",
                error_2: "",
                auth: null,
                is_authenticated: false,
            },
        };
    },
    props: {
        lerror_1: {
            default: "",
        },
        lerror_2: {
            default: "",
        },
        success: {
            default: "",
        },
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
        fill(){
        this.loginData.email = this.$refs.loginform.email.value;
            this.loginData.password = this.$refs.loginform.password.value;
        }
    },
};
</script>
