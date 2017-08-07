<template>
  <div id="wrapper">
    <img id="logo" src="~@/assets/logo.png" alt="electron-vue">
    <main>
      <div class="left-side">
        <span class="title">
          Info
        </span>
        <system-information></system-information>
        <button @click="nextNav">NEXT</button> 
        <button @click="backNav">BACK</button>
      </div>

      <div class="right-side">
        <div class="doc">
          <div class="title">ADCP Frequiences</div>
          <div class="cepo">
            <p>
              <div>
                  <img id="adcp" :src='adcpImage' width="150" height="200" :alt="adcp-image">
              </div>
              <div class="cepoLabel">
                CEPO {{ cepoValue }}
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
            <pre class="language-json"><code>{{ primaryBeamValue  }}</code></pre>
        </div>
        <div class="beams">
            <label class="beamTypeLabel">Select the Secondary Beams Frequency</label>
            <multiselect v-model="secondaryBeamValue" deselect-label="Remove this subsystem" track-by="label" label="label" placeholder="Select one" :options="secondaryBeamOptions" :searchable="true" :allow-empty="true"></multiselect>
            <pre class="language-json"><code>{{ secondaryBeamValue  }}</code></pre>
        </div>
        <div class="beams">
            <label class="beamTypeLabel">Select the Vertical Beam Frequnency</label>
            <multiselect v-model="verticalBeamValue" deselect-label="Remove this subsystem" track-by="label" label="label" placeholder="Select one" :options="verticalBeamOptions" :searchable="true" :allow-empty="true"></multiselect>
            <pre class="language-json"><code>{{ verticalBeamValue  }}</code></pre>
        </div>
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
    computed: {
      cepoValue() {
        let primVal = '';
        if (this.primaryBeamValue !== null && typeof this.primaryBeamValue.value !== 'undefined') {
          primVal = this.primaryBeamValue.value;
        }

        let secVal = '';
        if (this.secondaryBeamValue !== null && typeof this.secondaryBeamValue.value !== 'undefined') {
          secVal = this.secondaryBeamValue.value;
        } else {
          this.secondaryBeamValue = [];
          secVal = '';
        }

        let vertVal = '';
        if (this.verticalBeamValue !== null && typeof this.verticalBeamValue.value !== 'undefined') {
          vertVal = this.verticalBeamValue.value;
        } else {
          this.verticalBeamValue = [];
          vertVal = '';
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
          return this.getImgUrl('4beam');
        }

        // 5 Beam
        if ((this.primaryBeamValue !== null && typeof this.primaryBeamValue.value !== 'undefined') &&
          (this.secondaryBeamValue !== null && typeof this.secondaryBeamValue.value === 'undefined') &&
          (this.verticalBeamValue !== null && typeof this.verticalBeamValue.value !== 'undefined')) {
          return this.getImgUrl('5beam');
        }

        // 8 Beam
        if ((this.primaryBeamValue !== null && typeof this.primaryBeamValue.value !== 'undefined') &&
          (this.secondaryBeamValue !== null && typeof this.secondaryBeamValue.value !== 'undefined') &&
          (this.verticalBeamValue !== null && typeof this.verticalBeamValue.value === 'undefined')) {
          return this.getImgUrl('8beam');
        }

        // 7 Beam
        if ((this.primaryBeamValue !== null && typeof this.primaryBeamValue.value !== 'undefined') &&
          (this.secondaryBeamValue !== null && typeof this.secondaryBeamValue.value !== 'undefined') &&
          (this.verticalBeamValue !== null && typeof this.verticalBeamValue.value !== 'undefined')) {
          return this.getImgUrl('7beam');
        }

        // Backup value
        return this.getImgUrl('4beam');
      },
    },
    methods: {
      nextNav() {
        this.$router.push({ name: 'adcp-type' });
      },
      backNav() {
        this.$router.push({ name: 'adcp-type' });
      },
      getImgUrl(adcpType) {
        // Workaround for the binding to a path
        const images = require.context('../assets/', false, /\.png$/);
        return images(`./${adcpType}.png`);
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

  button {
      display: block;
      margin: 5px;
      border: 0px
  }

  body { font-family: 'Source Sans Pro', sans-serif; }

  #wrapper {
    background:
      radial-gradient(
        ellipse at top left,
        rgba(255, 255, 255, 1) 40%,
        rgba(229, 229, 229, .9) 100%
      );
    height: 100vh;
    padding: 60px 80px;
    width: 100vw;
  }

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
  }

  .beamTypeLabel {
    color: blue;
    font-weight: bold;
  }

  main {
    display: flex;
    justify-content: space-between;
  }

  main > div { flex-basis: 50%; }

  .left-side {
    display: flex;
    flex-direction: column;
  }

  .welcome {
    color: #555;
    font-size: 23px;
    margin-bottom: 10px;
  }

  .title {
    color: #2c3e50;
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 6px;
  }

  .title.alt {
    font-size: 18px;
    margin-bottom: 10px;
  }

  .doc p {
    color: black;
    margin-bottom: 10px;
  }

  .doc button {
    font-size: .8em;
    cursor: pointer;
    outline: none;
    padding: 0.75em 2em;
    border-radius: 2em;
    display: inline-block;
    color: #fff;
    background-color: #4fc08d;
    transition: all 0.15s ease;
    box-sizing: border-box;
    border: 1px solid #4fc08d;
  }

  .doc button.alt {
    color: #42b983;
    background-color: transparent;
  }
</style>
