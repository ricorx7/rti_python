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
          <div class="title">ADCP Types</div>
          <p>
            Select your ADCP Type
          </p>
        </div>
        <button @click="onAdcpSelection('SeaProfiler')"><img id="seaprofiler" src="~@/assets/RoweTech_SeaPROFILER.jpg" alt="SeaPROFILER"></button>
        <button @click="onAdcpSelection('SeaWatch')"><img id="seawatch" src="~@/assets/RoweTech_SeaWATCH.jpg" alt="SeaWATCH"></button>
        <button @click="onAdcpSelection('SeaPilot')"><img id="seapilot" src="~@/assets/RoweTech_SeaPILOT.jpg" alt="SeaPILOT"></button>
        <button @click="onAdcpSelection('SeaWave')"><img id="seawave" src="~@/assets/RoweTech_SeaWAVE.jpg" alt="SeaWAVE"></button>
        <button @click="onAdcpSelection('SeaSeven')"><img id="seaseaven" src="~@/assets/RoweTech_SeaSEVEN.jpg" alt="SeaSEVEN"></button>
      </div>
    </main>
  </div>
</template>

<script>
  import SystemInformation from './LandingPage/SystemInformation';

  export default {
    name: 'landing-page',
    components: { SystemInformation },
    methods: {
      onAdcpSelection(adcpType) {
        this.$store.dispatch('adcpTypeAsyncTask', adcpType);
      },
      nextNav() {
        this.$router.push({ name: 'freq' });
      },
      backNav() {
        this.$router.push({ name: 'landing-page' });
      },
    },
  };
</script>

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
