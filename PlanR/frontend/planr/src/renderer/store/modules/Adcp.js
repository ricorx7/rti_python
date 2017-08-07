const state = {
  type: 'SeaProfiler',
  cepo: '',
};

const mutations = {
  ADCP_TYPE(state, type) {
    state.type = type;
  },
  CEPO(state, cepo) {
    state.cepo = cepo;
  },
};

const actions = {
  someAsyncTask({ commit }) {
    // do something async
    commit('INCREMENT_MAIN_COUNTER');
  },
  adcpTypeAsyncTask({ commit }, type) {
    // do something async
    commit('ADCP_TYPE', type);
  },
  cepoAsyncTask({ commit }, cepo) {
    // do something async
    commit('CEPO', cepo);
  },
};

const getters = {
  type: state => state.type,
  cepo: state => state.cepo,
};

export default {
  state,
  mutations,
  actions,
  getters,
};
