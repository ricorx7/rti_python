<template>
  <div>
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

              <md-button class="md-icon-button" @click="toggleRightSidenavSysConfig">
                  <md-icon>assignment</md-icon>
              </md-button>
              <md-button class="md-icon-button" @click="openInfoDialog">
                  <md-icon>info</md-icon>
              </md-button>
          </md-toolbar>

          <div class="content">
            <div class="batt-img">
              <img id="battery" src="~@/assets/battery.png" alt="RTI Battery">
            </div>

            <md-input-container class="batt_input">
              <label>Select the Number of Batteries</label>
              <md-input type="number" min="0" v-model="numBatt"></md-input>
            </md-input-container>
          </div>


        <md-dialog ref='infoDialog'>
            <md-dialog-title>
                <div class="md-toolbar-container">
                    <h3 class="md-title">Battery Information</h3>
                </div>
            </md-dialog-title>
            <md-dialog-content>
              <div class="info">
                Battery consumption is calculated in the prediction model.  An self contained ADCP typically holds 2 batteries.  An additional external battery case can also be used to power the ADCP.  Making in total 4 batteries.  External battery cases can also be daisy chained together if more than 4 batteries are needed. 
                </br>
                </br>
                Battery Voltage: <div class="bold">30v</div></br>
                ADCP Min Voltage: <div class="bold">12v</div></br>
                ADCP Max Voltage: <div class="bold">36v</div></br>
              </div>

          <md-card class="card">

            <md-card-media class="batt-life-img">
              <img id="battery" src="~@/assets/battery_life.png" alt="RTI Battery Life">
            </md-card-media>

            <md-card-content>
                Plot of the Battery Life from 30v to 12v.
              </md-card-content>
          </md-card>

            </md-dialog-content>
        </md-dialog>

        <md-sidenav class="md-right" ref="rightSidenavSysConfig">
            <md-toolbar>
                <div class="md-toolbar-container">
                    System Configuration
                </div>
            </md-toolbar>
            <system-information></system-information>
        </md-sidenav>

        <md-sidenav class="md-left" ref="leftSidenav">
            <md-toolbar>
                <div class="md-toolbar-container">
                    Main Menu
                </div>
            </md-toolbar>
            <MainMenu></MainMenu>
        </md-sidenav>

      </div>
  </div>
</template>

<script>
  import SystemInformation from './SystemInformation';
  import MainMenu from './MainMenu';

  export default {
    name: 'batteries',
    data() {
      return {
      };
    },
    components: {
      SystemInformation,
      MainMenu,
    },
    created() {
      if (this.$store.getters.numBatteries === 0 && this.$store.getters.type === 'SeaWatch') {
        this.numBatt = 2;
      }
    },
    computed: {
      numBatt: {
        get() {
          return this.$store.getters.numBatteries;
        },
        set(value) {
          this.$store.commit('NUMBER_BATTERIES', value);
        },
      },
    },
    methods: {
      nextNav() {
        this.$router.push({ name: 'freq' });
      },
      backNav() {
        this.$router.push({ name: 'freq' });
      },
      openInfoDialog() {
        this.$refs.infoDialog.open();
      },
      toggleRightSidenavSysConfig() {
        this.$refs.rightSidenavSysConfig.toggle();
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
    margin: 40px;
  }

  .info {
    margin: 40px;
  }

  .batt-img {
    width: 35%;
  }

  .batt-life-img {
    margin: 20px;
  }

  .batt-input {
    margin: 40px;
  }

  .card {
    margin: 20px;
  }

  .bold {
    font-weight: bold;
    display: inline-block;
    margin-left: 5px;
  }

  body { font-family: 'Source Sans Pro', sans-serif; }

  
</style>
