<template>
  <div id="main">
    <div id="left" class="block">
      <Panel :title="'Ranking'" :panelHeight="'50%'" :panelWidth="'100%'" style="float:left" :titleStyle="{'height':titleHeight+'px','line-height':titleHeight+'px'}">
      </Panel> 
      <Panel :title="'Bar'" :panelHeight="'50%'" :panelWidth="'100%'" style="float:left" :titleStyle="{'height':titleHeight+'px','line-height':titleHeight+'px'}">
      </Panel>
    </div>
    <div id="right" class="block">
      <Panel :title="'Map'" :panelHeight="'50%'" :panelWidth="'100%'" style="float:left" :titleStyle="{'height':titleHeight+'px','line-height':titleHeight+'px'}">
      </Panel>
      <Panel :title="'Cloud'" :panelHeight="'50%'" :panelWidth="'100%'" style="float:left" :titleStyle="{'height':titleHeight+'px','line-height':titleHeight+'px'}">
      </Panel>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-unused-vars */
/* eslint-disable vue/no-unused-components */
import Panel from './components/panel';
import barView from './components/bar';
import cloudView from './components/cloud';
import rankView from './components/rank';
import mapView from './components/map';

export default {
  name: 'App',
  components: {
    Panel,
    barView, cloudView, rankView, mapView,
  },
  data(){
    return {
        titleHeight: 40,
    }
  },
}
</script>

<style scoped>
* {
  float: left;
}
#main {
  height:959px;
  width: 1918px;
  position: fixed;
  left: 1px;
  top: 1px;
}
.block {
  width: 50%;
  height: 100%;
}
</style>
