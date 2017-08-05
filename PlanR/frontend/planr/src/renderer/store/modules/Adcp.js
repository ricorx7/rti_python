const state = {
  type: 'SeaProfiler',
  freq: '300',
};

const mutations = {
  ADCP_TYPE(state, type) {
    state.type = type;
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
};

const getters = {
  type: state => state.type,
  freq: state => state.freq,
};

export default {
  state,
  mutations,
  actions,
  getters,
};
