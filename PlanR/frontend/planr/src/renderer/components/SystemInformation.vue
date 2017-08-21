<template>
  <div class="info">
    <div class="title">Information</div>
    <div class="items">
      <div class="item">
        <div class="name">ADCP Type:</div>
        <div class="value">{{ type }}</div>
      </div>
      <div class="item">
        <div class="name">CEPO:</div>
        <div class="value">{{ cepo }}</div>
      </div>
      <div class="item">
        <div class="name">Number of Batteries:</div>
        <div class="value">{{ numBatteries }}</div>
      </div>
      <div class="item">
        <div class="name">Salinity:</div>
        <div class="value">{{ salinity }}</div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
      };
    },
    computed: {
      type() {
        return this.$store.getters.type;
      },
      cepo() {
        return this.$store.getters.cepo;
      },
      numBatteries() {
        return this.$store.getters.numBatteries;
      },
      salinity() {
        return this.$store.getters.salinity;
      },
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
