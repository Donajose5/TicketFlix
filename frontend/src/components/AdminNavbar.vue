<template>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">
    <nav class="navbar navbar-dark bg-dark">
        <div class="navbar-brando">Hello, {{ this.current_name }}</div>

        <ul class="ulist ms-auto">
            <li>
                <a class="nav-link" @click.prevent=" $emit('changevenue');"> Venues </a>
            </li>
            <li>
                <a class="nav-link" @click.prevent=" $emit('changeshow');"> Shows</a>
            </li>
            <li>
                <a class="nav-link" @click.prevent=" $emit('changemovie');"> Movies</a>
            </li>
            <!--
            <li>
                <a class="nav-link" @click.prevent=" $emit('changesummary');"> Summary</a>
            </li>
            -->
        </ul>

        <button class="btn btn-outline-success my-2 my-sm-0 logout" type="submit" @click="lout()">Log Out</button>
    </nav>
</template>
 
    
<script>
export default {
    name: "NavBar",
    props: {
        name: {
            default: "",
        },
    },
    data() {
        return {
            current_email: null,
            current_name: null,
            auth_token: null,
        };
    },
    async created() {
        this.auth_token = sessionStorage.getItem("auth-token");
        this.current_email = sessionStorage.getItem("email");
        this.current_name = sessionStorage.getItem("name");
        if (!this.auth_token) {
            alert("Please Login to see your dashboard.");
            this.$router.push("/");
        }
    },

    methods: {
        async lout() {
            console.log("clear");
            sessionStorage.clear();
            localStorage.clear();
            this.$router.push("/");
        },
    },
};
</script>
    
<style>
nav {
    color: white;
    font-size: 25px;
}

.navbar-brando {
    font-size: 30px;
    padding: 20px;
    color: white;
}

.text {
    display: inline-block;
    color: white;
    font-size: 20px;
    margin-right: 20px;
}

.ulist {
    list-style: none;
    height: fit-content;
    vertical-align: auto;
}

.ulist li {
    display: inline-block;
    margin-right: 25px;
    padding-top: 15px;
}

.ulist li:hover {
    color: grey;
}

.logout {
    margin-right: 20px;
}
</style>
