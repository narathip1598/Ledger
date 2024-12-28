// src/router.js
import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from './components/LoginPage.vue';
import QuestionPage from './components/QuestionPage.vue';

const routes = [
  {
    path: '/login', // URL path
    name: 'Login',
    component: LoginPage, // The component to render
  },
  {
    path: '/', // Default route (e.g., homepage)
    name: 'QuestionPage',
    component: QuestionPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
