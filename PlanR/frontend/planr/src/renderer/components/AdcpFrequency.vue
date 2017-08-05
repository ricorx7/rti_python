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
          <p>
            Select the Frequencies of the ADCP
          </p>
        </div>
        <div>
        <label class="typo__label">Groups</label>
        <multiselect v-model="value" :options="options" :multiple="true" group-values="libs" group-label="config" placeholder="Type to search" track-by="name" label="name"><span slot="noResult">Oops! No elements found. Consider changing the search query.</span></multiselect>
        <pre class="language-json"><code>{{ value  }}</code></pre>
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
        value: [],
        options: [
          {
            config: 'Primary',
            libs: [
                { name: '2 - 1200kHz', code: '2' },
                { name: '3 - 600kHz', code: '3' },
                { name: '4 - 300kHz', code: '4' },
            ],
          },
          {
            config: '45 degree offset',
            libs: [
                { name: '6 - 1200kHz  45 degree offset', code: '6' },
                { name: '7 - 600kHz  45 degree offset', code: '7' },
                { name: '8 - 300kHz  45 degree offset', code: '8' },
            ],
          },
          {
            config: 'Vertical Beam',
            libs: [
                { name: 'A - 1200kHz Vertical Beam', code: 'A' },
                { name: 'B - 600kHz  Vertical Beam', code: 'B' },
                { name: 'C - 300kHz  Vertical Beam', code: 'C' },
            ],
          },
        ],
      };
    },
    components: {
      SystemInformation,
      Multiselect,
    },
    methods: {
      onAdcpSelection(adcpType) {
        this.$store.dispatch('adcpTypeAsyncTask', adcpType);
      },
      backNav() {
        this.$router.push({ name: 'adcp-type' });
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
