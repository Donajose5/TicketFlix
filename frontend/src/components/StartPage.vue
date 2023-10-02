<template>

<div class='head'>
Welcome to TicketFlix !!
</div>

<div class='main'>

<button class="btn1" @click.prevent=" $emit('changel');"> Log In </button><br><br>
<button class="btn1" @click.prevent=" $emit('changes');"> Sign Up </button>

</div>

</template>


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

</style>


