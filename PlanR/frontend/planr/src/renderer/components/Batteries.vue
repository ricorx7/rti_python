<template>
  <div id="wrapper">
    <main>
      <div>
            <md-toolbar>
              <md-button class="md-icon-button" @click="toggleLeftSidenav">
                  <md-icon>menu</md-icon>
              </md-button>
              <h2 class="md-title" style="flex: 1">ADCP Batteries</h2>
              
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
              Select the Number of Batteries
            </p>
            <div class="batt-img">
              <img id="battery" src="~@/assets/battery.png" alt="RTI Battery">
            </div>
          </div>

        <md-sidenav class="md-right" ref="rightSidenav">
            <md-toolbar>
                <div class="md-toolbar-container">
                    <h3 class="md-title">Sidenav content</h3>
                </div>
            </md-toolbar>
            Infomation about frequency.
        </md-sidenav>

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
    methods: {
      onAdcpSelection(adcpType) {
        this.$store.dispatch('adcpTypeAsyncTask', adcpType);
      },
      nextNav() {
        this.$router.push({ name: 'freq' });
      },
      backNav() {
        this.$router.push({ name: 'freq' });
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

  .content {
    margin-top: 40px;
  }

  .batt-img {
    width: 50%;
  }

  body { font-family: 'Source Sans Pro', sans-serif; }

  
</style>
