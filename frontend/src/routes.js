import api from './api'
import { createWebHistory, createRouter } from "vue-router";

import Content from './components/Content.vue';
import LoginPage from './components/LoginPage.vue';
import RegisterPage from './components/RegisterPage.vue';

// Admin
import AdminDashboard from './components/admin/AdminDashboard.vue';
import AddParkingLot from './components/admin/AddParkingLot.vue';
import EditParkingLot from './components/admin/EditParkingLot.vue';
import AddSpots from './components/admin/AddSpots.vue';
import ViewParkingLots from './components/admin/ViewParkingLots.vue';
import ViewUsers from './components/admin/ViewUsers.vue';
import ViewOccupiedSpots from './components/admin/ViewOccupiedSpots.vue';
import AdminSummary from './components/admin/AdminSummary.vue';
import ViewReservations from './components/admin/ViewReservations.vue';
import UserDetails from './components/admin/UserDetails.vue';

// User
import UserDashboard from './components/user/UserDashboard.vue';
import BookSpot from './components/user/BookSpot.vue';
import ManageBookings from './components/user/ManageBookings.vue';
import ParkingHistory from './components/user/ParkingHistory.vue';
import UserSummary from './components/user/UserSummary.vue';

const routes = [
    { path: '/', component: Content },
    { path: '/login', component: LoginPage },
    { path: '/register', component: RegisterPage },

    // Admin Routes
    {
        path: '/admin',
        component: AdminDashboard,
        meta: { requiresAuth: true, role: 'admin' },
        children: [
            { path: '', redirect: '/admin/view' },
            { path: 'view', component: ViewParkingLots },
            { path: 'users', component: ViewUsers },
            { path: 'users/:id', component: UserDetails },
            { path: 'reservations', component: ViewReservations },
            { path: 'search', component: () => import('./components/admin/AdminSearch.vue') },
            { path: 'summary', component: AdminSummary },
            { path: 'add-lot', component: AddParkingLot },
            { path: 'edit-lot/:id', component: EditParkingLot },
            { path: 'add-spots/:lot_id', component: AddSpots },
            { path: 'occupied', component: ViewOccupiedSpots }
        ]
    },

    // User Routes
    {
        path: '/user',
        component: UserDashboard,
        meta: { requiresAuth: true },
        children: [
            { path: '', redirect: '/user/summary' },
            { path: 'book/:lot_id', component: BookSpot },
            { path: 'manage-bookings', component: ManageBookings },
            { path: 'history', component: ParkingHistory },
            { path: 'summary', component: UserSummary }
        ]
    }
];

export const router = createRouter({
    history: createWebHistory(),
    routes
});

async function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) return false;
    try {
        await api.get('/api/user_home');
        return true;
    } catch {
        return false;
    }
}

async function checkAdmin() {
    const token = localStorage.getItem('token');
    if (!token) return false;
    try {
        await api.get('/api/admin_home');
        return true;
    } catch {
        return false;
    }
}

router.beforeEach(async (to) => {
    const requiresAuth = to.matched.some(r => r.meta && r.meta.requiresAuth);
    const requiresAdmin = to.matched.some(r => r.meta && r.meta.role === 'admin');
    if (to.path === '/') {
        const token = localStorage.getItem('token');
        if (token) {
            const isAdmin = await checkAdmin();
            return { path: isAdmin ? '/admin' : '/user' };
        }
        return true;
    }
    if (!requiresAuth) return true;
    if (requiresAdmin) {
        const ok = await checkAdmin();
        if (!ok) return { path: '/login', query: { next: to.fullPath } };
        return true;
    }
    const ok = await checkAuth();
    if (!ok) return { path: '/login', query: { next: to.fullPath } };
    return true;
});