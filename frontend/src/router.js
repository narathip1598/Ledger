import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from './components/LoginPage.vue';
import RegisterPage from './components/RegisterPage.vue'; // Register page component
import QuestionPage from './components/QuestionPage.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
  },
  {
    path: '/register',  // Add Register route
    name: 'Register',
    component: RegisterPage, // Make sure to create the RegisterPage.vue component
  },
  {
    path: '/',
    name: 'QuestionPage',
    component: QuestionPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
