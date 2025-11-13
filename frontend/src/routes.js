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

// User
import UserDashboard from './components/user/UserDashboard.vue';
import BookSpot from './components/user/BookSpot.vue';
import ReleaseSpot from './components/user/ReleaseSpot.vue';
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
        children: [
            { path: 'add-lot', component: AddParkingLot },
            { path: 'edit-lot/:id', component: EditParkingLot },
            { path: 'add-spots/:lot_id', component: AddSpots },
            { path: 'view-lots', component: ViewParkingLots },
            { path: 'users', component: ViewUsers },
            { path: 'occupied', component: ViewOccupiedSpots },
            { path: 'summary', component: AdminSummary }
        ]
    },

    // User Routes
    {
        path: '/user',
        component: UserDashboard,
        children: [
            { path: 'book/:lot_id', component: BookSpot },
            { path: 'release/:spot_id', component: ReleaseSpot },
            { path: 'history', component: ParkingHistory },
            { path: 'summary', component: UserSummary }
        ]
    }
];

export const router = createRouter({
    history: createWebHistory(),
    routes
});