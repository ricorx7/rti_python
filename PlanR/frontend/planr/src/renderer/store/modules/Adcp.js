const state = {
  type: 'SeaProfiler',
  cepo: '',
  primaryBeams: [],
  secondaryBeams: [],
  verticalBeam: [],
  numBatteries: 0,
};

const mutations = {
  ADCP_TYPE(state, type) {
    state.type = type;
  },
  CEPO(state, cepo) {
    state.cepo = cepo;
  },
  PRIMARY_BEAMS(state, val) {
    state.primaryBeams = val;
  },
  SECONDARY_BEAMS(state, val) {
    state.secondaryBeams = val;
  },
  VERTICAL_BEAM(state, val) {
    state.verticalBeam = val;
  },
  NUMBER_BATTERIES(state, val) {
    state.numBatteries = val;
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
  primaryBeams: state => state.primaryBeams,
  secondaryBeams: state => state.secondaryBeams,
  verticalBeam: state => state.verticalBeam,
  numBatteries: state => state.numBatteries,
};

export default {
  state,
  mutations,
  actions,
  getters,
};
