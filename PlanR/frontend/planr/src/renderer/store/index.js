import Vue from 'vue';
import Vuex from 'vuex';
import VueMaterial from 'vue-material';

import modules from './modules';

Vue.use(Vuex);
Vue.use(VueMaterial);

export default new Vuex.Store({
  modules,
  strict: process.env.NODE_ENV !== 'production',
});
