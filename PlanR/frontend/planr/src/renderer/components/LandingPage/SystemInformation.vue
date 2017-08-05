<template>
  <div>
    <div class="title">Information</div>
    <div class="items">
      <div class="item">
        <div class="name">ADCP Type:</div>
        <div class="value">{{ type }}</div>
      </div>
      <div class="item">
        <div class="name">Frequency:</div>
        <div class="value">{{ freq }}</div>
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
      freq() {
        return this.$store.getters.freq;
      },
    },
  };
</script>

<style scoped>
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
