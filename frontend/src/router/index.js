import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AdminView from "../views/AdminView.vue";

const routes = [
  {
    path: "/home",
    name: "home",
    component: HomeView,
  },
  
  {
    path: "/admin",
    name: "admin",
    component: AdminView,
  },
  {
    path: "/signup",
    name: "signup",
    component: () => import("../components/SignUp.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../components/LogIn.vue"),
  },
  {
    path: "/",
    name: "start",
    component: () =>
      import("../views/StartView.vue"),
  },
  {
    path: "/venue",
    name: "venue",
    component: () => import("../components/VenuePage.vue"),
  },
  {
    path: "/movie",
    name: "movie",
    component: () => import("../components/MoviePage.vue"),
  },
  {
    path: "/show",
    name: "show",
    component: () => import("../components/ShowPage.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
