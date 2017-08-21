<template>
  <div class="info">
    <md-list>
        <md-list-item @click="$router.push({ name: 'adcp-type' })">
            <md-icon>view_module</md-icon> <span>ADCP Type</span>
        </md-list-item>
        <md-list-item @click="$router.push({ name: 'freq' })">
            <md-icon>rss_feed</md-icon> <span>Frequency</span>
        </md-list-item>
        <md-list-item @click="$router.push({ name: 'batt' })">
            <md-icon>battery_charging_full</md-icon> <span>Batteries</span>
        </md-list-item>
    </md-list>
  </div>
</template>

<script>
  export default {
    data() {
      return {
      };
    },
  };
</script>

<style scoped>

  .info {
    margin: 20px;
  }

  .title {
    color: #888;
    font-size: 18px;
    font-weight: initial;
    letter-spacing: .25px;
    margin-top: 10px;
  }

  .items { margin-top: 8px; }

  .item {
    display: flex;
    margin-bottom: 6px;
  }

  .item .name {
    color: #6a6a6a;
    margin-right: 6px;
  }

  .item .value {
    color: #35495e;
    font-weight: bold;
  }
</style>
