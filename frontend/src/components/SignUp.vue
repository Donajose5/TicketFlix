<template>
    <div class='bd'>
<link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css"
    />
        <div class='head'>
            Sign Up
        </div>

        <div id="popup">
            <p class="alert alert-danger fade show" v-if="serror_1">
                {{ serror_1 }}
            </p>
            <p class="alert alert-danger fade show" v-if="serror_2">
                {{ serror_2 }}
            </p>
            <p class="alert alert-success fade show" role="alert" v-if="success">
                {{ success }}
            </p>
        </div>

        <div class='main'>

            <form ref="signinform" method="Post">

                <div class="field">
                    <label class="label is-large" for="email">Email</label>
                    <div class="control">
                        <input type="email" class="input is-large" id="email" v-model="email">
                    </div>
                </div><br>
                
                <div class="field">
                    <label class="label is-large" for="text">Name</label>
                    <div class="control">
                        <input type="text" class="input is-large" id="name" v-model="name">
                    </div>
                </div><br>

                <div class="field">
                    <label class="label is-large" for="password">Password</label>
                    <div class="control">
                        <input type="password" class="input is-large" id="password1" v-model="password1">
                    </div>
                </div>
                <br>

                <div class="field">
                    <label class="label is-large" for="password">Confirm Password</label>
                    <div class="control">
                        <input type="password" class="input is-large" id="password2" v-model="password2">
                    </div>
                </div>
                <br>

                <div class="control">
                    <div class="btn1" @click.prevent=" fill();
                        $emit('signup', signupData);
                    resetForm();
                    ">Register</div> <br>
                    <a @click.prevent=" $emit('changel');">Click here to Log In</a>
                </div>
            </form>

        </div>

    </div>
</template>
       
<script>
export default {
    data() {
        return {
            signupData: {
                email: null,
                name: null,
                password1: null,
                password2: null,
                error_1: "",
                error_2: "",
            },
        }
    },

    props: {
        serror_1: {
            default: "",
        },
        serror_2: {
            default: "",
        },
        success: {
            default: "",
        },
    },

    methods: {
        resetForm() {
            this.$refs.signinform.reset();
            this.signupData.email = null;
            this.signupData.name = null;
            this.signupData.password1 = null;
            this.signupData.password2 = null;
        },
        fill(){
        this.signupData.email = this.$refs.signinform.email.value;
        this.signupData.name = this.$refs.signinform.name.value;
            this.signupData.password1 = this.$refs.signinform.password1.value;
            this.signupData.password2 = this.$refs.signinform.password2.value;
        }
    },
};
</script>
