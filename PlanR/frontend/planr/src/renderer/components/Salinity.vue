<template>
  <div>
      <div>
            <md-toolbar>
              <md-button class="md-icon-button" @click="toggleLeftSidenav">
                  <md-icon>menu</md-icon>
              </md-button>
              <h2 class="md-title" style="flex: 1">Water Salinity</h2>
              
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
            <div class='inline'>

              <md-button @click="onSalinitySelection('ocean')">
                <md-card>
                  <md-card-media-cover md-text-scrim>
                    <md-card-media>
                      <img id="salinity_ocean" src="~@/assets/salinity_ocean.png" alt="Ocean Salinity">
                    </md-card-media>
                    <md-card-area>
                      <md-card-header>
                        <div class="md-title">Ocean</div>
                        <div class="md-subhead">35 ppt</div>
                      </md-card-header>
                    </md-card-area>
                  </md-card-media-cover>
                </md-card>
              </md-button>

              <md-button @click="onSalinitySelection('fresh')">
                <md-card>
                  <md-card-media-cover md-text-scrim>
                    <md-card-media>
                      <img id="salinity_fresh" src="~@/assets/salinity_fresh.png" alt="Fresh Salinity">
                    </md-card-media>
                    <md-card-area>
                      <md-card-header>
                        <div class="md-title">Fresh Water</div>
                        <div class="md-subhead">0 ppt</div>
                      </md-card-header>
                    </md-card-area>
                  </md-card-media-cover>
                </md-card>
              </md-button>

              <md-button @click="onSalinitySelection('estuary')">
                <md-card>
                  <md-card-media-cover md-text-scrim>
                    <md-card-media>
                      <img id="salinity_ocean" src="~@/assets/salinity_estuary.png" alt="Estuary Salinity">
                    </md-card-media>
                    <md-card-area>
                      <md-card-header>
                        <div class="md-title">Estuary</div>
                        <div class="md-subhead">15 ppt</div>
                      </md-card-header>
                    </md-card-area>
                  </md-card-media-cover>
                </md-card>
              </md-button>

            </div>

            <md-input-container class="salinity_input">
              <label>Set the salinity value of the water in ppt:</label>
              <md-input type="number" min="0" v-model="salinity"></md-input>
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
                Salinity of the water.  This value is used in the Speed of Sound calculation.  A more accurate value can be read by a CTD and feed into the ADCP.  But if no lave value is available, this value will be used to make the Speed of Sound calculation.
                <br />
                <br />          
                <div class="title">Ocean</div>
                <div class="desc">
                Salt water.  Water in the ocean.  Default value is typically 35ppt.  Some may use 32ppt.
                </div>

                <div class="title">Fresh</div>
                <div class="desc">
                Fresh water.  Water in the lake or river.  This value may be for some water near ice melting.  Default value is typically 0ppt.
                </div>

                <div class="title">Estuary</div>
                <div class="desc">
                Estuary water.  Locations where salt water and fresh water mix.  Default value is typically 15ppt.
                </div>
              </div>

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
    name: 'salinity',
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
        this.salinity = 35;
      }
    },
    computed: {
      salinity: {
        get() {
          return this.$store.getters.salinity;
        },
        set(value) {
          this.$store.commit('SALINITY', value);
        },
      },
    },
    methods: {
      onSalinitySelection(type) {
        if (type === 'ocean') {
          this.salinity = 35;
        }
        if (type === 'fresh') {
          this.salinity = 0;
        }
        if (type === 'estuary') {
          this.salinity = 15;
        }
      },
      nextNav() {
        this.$router.push({ name: 'freq' });
      },
      backNav() {
        this.$router.push({ name: 'batt' });
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
