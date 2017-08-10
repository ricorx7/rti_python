<template>
  <div id="wrapper">
    <main>
      <div>
        <md-toolbar>
            <md-button class="md-icon-button" @click="toggleLeftSidenav">
                <md-icon>menu</md-icon>
            </md-button>
            <h2 class="md-title" style="flex: 3" >ADCP Type</h2>
            
            <md-button class="md-icon-button" @click="backNav">
                <md-icon>chevron_left</md-icon>
            </md-button>
            <md-button class="md-icon-button" @click="nextNav">
                <md-icon>chevron_right</md-icon>
            </md-button>

            <md-button class="md-icon-button" @click="toggleRightSidenav">
                <md-icon>info</md-icon>
            </md-button>
        </md-toolbar>

        <div class="content">
          <p>
            Select your ADCP Type
          </p>
          <div class="type">
            <h2>{{ type }}</h2>
          </div>
            <md-button @click="onAdcpSelection('SeaProfiler')"><img id="seaprofiler" src="~@/assets/RoweTech_SeaPROFILER.jpg" alt="SeaPROFILER"></md-button>
            <md-button @click="onAdcpSelection('SeaWatch')"><img id="seawatch" src="~@/assets/RoweTech_SeaWATCH.jpg" alt="SeaWATCH"></md-button>
            <md-button @click="onAdcpSelection('SeaPilot')"><img id="seapilot" src="~@/assets/RoweTech_SeaPILOT.jpg" alt="SeaPILOT"></md-button>
            <md-button @click="onAdcpSelection('SeaWave')"><img id="seawave" src="~@/assets/RoweTech_SeaWAVE.jpg" alt="SeaWAVE"></md-button>
            <md-button @click="onAdcpSelection('SeaSeven')"><img id="seaseaven" src="~@/assets/RoweTech_SeaSEVEN.jpg" alt="SeaSEVEN"></md-button>
        </div>
        <md-sidenav-container>
        <md-sidenav class="md-right" ref="rightSidenav">
            <md-toolbar>
                <div class="md-toolbar-container">
                    <h3 class="md-title">ADCP Type Details</h3>
                </div>
            </md-toolbar>
            <div class="desc">
            Select the ADCP type.  This will determine the default setup for your ADCP.
            </div>

            <h3>SeaPROFILER</h3>
            <div class="desc">
            A direct reading ADCP.  This ADCP will have unlimited power to the ADCP through the underwater cable.  It will record all data to a computer.  It will be typically on a moving boat.
            </div>

            <h3>SeaWATCH</h3>
            <div class="desc">
            A self contained ADCP.  This ADCP will be powered by batteries.  It will record to the internal SD card.  It will be typically mounted on the sea floor looking upward.  Pay attention when configuring this ADCP of the power usage in the prediction model.
            </div>

            <h3>SeaPILOT</h3>
            <div class="desc">
            A direct reading ADCP.  This ADCP will have unlimited power to the ADCP through the underwater cable.  It will give data in a DVL NMEA ASCII style format.  It will be typically mounted to a ROV/AUV for navigation purposes.  
            </div>

            <h3>SeaWAVE</h3>
            <div class="desc">
            A self contained ADCP.  This ADCP will be powered by batteries.  It will record to the internal SD card.  This ADCP will typically include a vertical beam and pressure sensor to measure the wave height and vertical velocity.  It will be typically mounted on the sea floor looking upward in around 20 meters of water.  The data will be output in bursts of between 1024 and 4096 ensembles over a 17 minute period.  Pay attention when configuring this ADCP of the power usage and data usage in the prediction model.
            </div>

            <h3>SeaSEVEN</h3>
            <div class="desc">
            A self contained ADCP.  This ADCP will be powered by batteries.  It will record to the internal SD card.  This ADCP is a dual frequency system with a vertical beam.  It will be typically mounted on the sea floor looking upward.  Pay attention when configuring this ADCP of the power usage in the prediction model.
            </div>

        </md-sidenav>
        </md-sidenav-container>

        <md-sidenav class="md-left" ref="leftSidenav">
            <md-toolbar>
                <div class="md-toolbar-container">
                    System Configuration
                </div>
            </md-toolbar>
            <system-information></system-information>
        </md-sidenav>
      </div>
    </main>
  </div>
</template>

<script>
  import SystemInformation from './LandingPage/SystemInformation';

  export default {
    name: 'landing-page',
    components: { SystemInformation },
    data() {
      return {
        type: '',
      };
    },
    created() {
      this.type = this.$store.getters.type;
    },
    methods: {
      onAdcpSelection(adcpType) {
        this.$store.dispatch('adcpTypeAsyncTask', adcpType);
        this.type = adcpType;
      },
      nextNav() {
        this.$router.push({ name: 'freq' });
      },
      backNav() {
        this.$router.push({ name: 'landing-page' });
      },
      toggleRightSidenav() {
        this.$refs.rightSidenav.toggle();
      },
      toggleLeftSidenav() {
        this.$refs.leftSidenav.toggle();
      },
    },
  };
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro');

  .type {
    background: lightsteelblue;
    text-align: center;
    margin: 20px;
  }

  img {
      width: 100%;
  }

  body { font-family: 'Source Sans Pro', sans-serif; }

  .desc {
      margin-top: 0px;
      margin-bottom: 20px;
      margin-left: 20px;
      margin-right: 20px;
  }


</style>
