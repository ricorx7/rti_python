import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'landing-page',
      component: require('@/components/LandingPage'),
    },
    {
      path: '/type',
      name: 'adcp-type',
      component: require('@/components/AdcpType'),
    },
    {
      path: '/freq',
      name: 'freq',
      component: require('@/components/AdcpFrequency'),
    },
    {
      path: '/batt',
      name: 'batt',
      component: require('@/components/Batteries'),
    },
    {
      path: '/salinity',
      name: 'salinity',
      component: require('@/components/Salinity'),
    },
    {
      path: '*',
      redirect: '/',
    },
  ],
});
