<template>
  <div id="wrapper">
    <img id="logo" src="~@/assets/logo.png" alt="electron-vue">
    <main>
      <div class="left-side">
        <span class="title">
          System Configuration
        </span>
        <system-information></system-information>
        <button @click="nextNav">NEXT</button> 
        <button @click="backNav">BACK</button>
      </div>

      <div class="right-side">

        <div class="doc">
            <md-toolbar>
                <md-button class="md-icon-button" @click="toggleRightSidenav">
                    <md-icon>menu</md-icon>
                </md-button>
                <h2 class="md-title" style="flex: 1">ADCP Frequencies</h2>
                <md-button class="md-icon-button">
                    <md-icon>info</md-icon>
                </md-button>
            </md-toolbar>

          <div class="cepo">
            <p>
              <div>
                  <img id="adcp" :src='adcpImage' alt="adcp-image">
              </div>
              <div class="cepoLabel">
                CEPO {{ cepoValue }}</br>
              </div> 
              <div class="adcpDescLabel">
               {{ adcpDesc }}
              </div>
            </p>
          </div>
          <p>
            Select the Frequencies of the ADCP
          </p>
        </div>
        <div class="beams">
            <label class="beamTypeLabel">Select the Primary Beam Freqency</label>
            <multiselect v-model="primaryBeamValue" deselect-label="Select a different subsystem" track-by="label" label="label" placeholder="Select one" :options="primaryBeamOptions" :searchable="true" :allow-empty="false"></multiselect>
        </div>
        <div class="beams">
            <label class="beamTypeLabel">Select the Secondary Beams Frequency</label>
            <multiselect v-model="secondaryBeamValue" deselect-label="Remove this subsystem" track-by="label" label="label" placeholder="Select one" :options="secondaryBeamOptions" :searchable="true" :allow-empty="true"></multiselect>
        </div>
        <div class="beams">
            <label class="beamTypeLabel">Select the Vertical Beam Frequnency</label>
            <multiselect v-model="verticalBeamValue" deselect-label="Remove this subsystem" track-by="label" label="label" placeholder="Select one" :options="verticalBeamOptions" :searchable="true" :allow-empty="true"></multiselect>
        </div>

        <md-sidenav class="md-right" ref="rightSidenav">
            <md-toolbar>
            <div class="md-toolbar-container">
                <h3 class="md-title">Sidenav content</h3>
            </div>
            </md-toolbar>
            Infomation about frequency.
        </md-sidenav>

      </div>
    </main>
  </div>
</template>

<script>
  import Multiselect from 'vue-multiselect';
  import SystemInformation from './LandingPage/SystemInformation';

  export default {
    name: 'adcp-freq',
    data() {
      return {
        primaryBeamValue: [],
        secondaryBeamValue: [],
        verticalBeamValue: [],
        adcpDesc: '',
        primaryBeamOptions: [
            { label: '2 - 1200kHz', value: '2' },
            { label: '3 - 600kHz', value: '3' },
            { label: '4 - 300kHz', value: '4' },
        ],
        secondaryBeamOptions: [
            { label: '6 - 1200kHz  45 degree offset', value: '6' },
            { label: '7 - 600kHz  45 degree offset', value: '7' },
            { label: '8 - 300kHz  45 degree offset', value: '8' },
        ],
        verticalBeamOptions: [
            { label: 'A - 1200kHz Vertical Beam', value: 'A' },
            { label: 'B - 600kHz  Vertical Beam', value: 'B' },
            { label: 'C - 300kHz  Vertical Beam', value: 'C' },
        ],
      };
    },
    components: {
      SystemInformation,
      Multiselect,
    },
    created() {
      this.primaryBeamValue = this.$store.getters.primaryBeams;
      this.secondaryBeamValue = this.$store.getters.secondaryBeams;
      this.verticalBeamValue = this.$store.getters.verticalBeam;
    },
    computed: {
      cepoValue() {
        let primVal = '';
        if (this.primaryBeamValue !== null && typeof this.primaryBeamValue.value !== 'undefined') {
          primVal = this.primaryBeamValue.value;
          this.$store.commit('PRIMARY_BEAMS', this.primaryBeamValue);
        }

        let secVal = '';
        if (this.secondaryBeamValue !== null && typeof this.secondaryBeamValue.value !== 'undefined') {
          secVal = this.secondaryBeamValue.value;
          this.$store.commit('SECONDARY_BEAMS', this.secondaryBeamValue);
        } else {
          this.secondaryBeamValue = [];
          secVal = '';
          this.$store.commit('SECONDARY_BEAMS', []);
        }

        let vertVal = '';
        if (this.verticalBeamValue !== null && typeof this.verticalBeamValue.value !== 'undefined') {
          vertVal = this.verticalBeamValue.value;
          this.$store.commit('VERTICAL_BEAM', this.verticalBeamValue);
        } else {
          this.verticalBeamValue = [];
          vertVal = '';
          this.$store.commit('VERTICAL_BEAM', []);
        }

        // Combined all the beam configurations
        const result = primVal + secVal + vertVal;

        // Pass the configuration
        this.$store.dispatch('cepoAsyncTask', result);

        return result;
      },
      adcpImage() {
        // 4 Beam
        if ((this.primaryBeamValue !== null && typeof this.primaryBeamValue.value !== 'undefined') &&
          (this.secondaryBeamValue !== null && typeof this.secondaryBeamValue.value === 'undefined') &&
          (this.verticalBeamValue !== null && typeof this.verticalBeamValue.value === 'undefined')) {
          this.adcpDesc = '4 Beam system';
          return this.getImgUrl('4beam');
        }

        // 5 Beam
        if ((this.primaryBeamValue !== null && typeof this.primaryBeamValue.value !== 'undefined') &&
          (this.secondaryBeamValue !== null && typeof this.secondaryBeamValue.value === 'undefined') &&
          (this.verticalBeamValue !== null && typeof this.verticalBeamValue.value !== 'undefined')) {
          this.adcpDesc = 'Vertical Beam system';
          return this.getImgUrl('5beam');
        }

        // 8 Beam
        if ((this.primaryBeamValue !== null && typeof this.primaryBeamValue.value !== 'undefined') &&
          (this.secondaryBeamValue !== null && typeof this.secondaryBeamValue.value !== 'undefined') &&
          (this.verticalBeamValue !== null && typeof this.verticalBeamValue.value === 'undefined')) {
          this.adcpDesc = 'Dual Frequency system';
          return this.getImgUrl('8beam');
        }

        // 7 Beam
        if ((this.primaryBeamValue !== null && typeof this.primaryBeamValue.value !== 'undefined') &&
          (this.secondaryBeamValue !== null && typeof this.secondaryBeamValue.value !== 'undefined') &&
          (this.verticalBeamValue !== null && typeof this.verticalBeamValue.value !== 'undefined')) {
          this.adcpDesc = 'SeaSeven - Dual Frequency with Vertical Beam system.';
          return this.getImgUrl('7beam');
        }

        // Backup value
        return this.getImgUrl('4beam');
      },
    },
    methods: {
      nextNav() {
        this.$router.push({ name: 'batt' });
      },
      backNav() {
        this.$router.push({ name: 'adcp-type' });
      },
      getImgUrl(adcpType) {
        // Workaround for the binding to a path
        const images = require.context('../assets/', false, /\.png$/);
        return images(`./${adcpType}.png`);
      },
      toggleRightSidenav() {
        this.$refs.rightSidenav.toggle();
      },
    },
  };
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
  @import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro');

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  .md-icon-button {
      background-color: transparent;
  }

  body { font-family: 'Source Sans Pro', sans-serif; }

  #logo {
    height: auto;
    margin-bottom: 20px;
    width: 420px;
  }

  .beams {
      margin-top: 20px;
  }

  .cepo {
      margin-top: 40px;
      margin-bottom: 40px;
  }

  .cepoLabel {
    font-weight: bold;
  }

  .adcpDescLabel {
    background: lightsteelblue;
  }

  .beamTypeLabel {
    color: blue;
    font-weight: bold;
  }


  main > div { flex-basis: 50%; }

  .left-side {
    display: flex;
    flex-direction: column;
  }


</style>
