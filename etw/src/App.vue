<template>
  <!-- eslint-disable vue/no-deprecated-slot-attribute -->
  <div id="main">
    <div id="left" class="block">
      <Panel :title="'全国热门景点销量排行'" :panelHeight="'50%'" :panelWidth="'100%'" style="float:left" :titleStyle="{'height':titleHeight+'px','line-height':titleHeight+'px'}">
        <template v-slot:panelBody>
          <RankView></RankView>
        </template>
      </Panel> 
      <Panel :title="'全国各省市4A-5A景区数量'" :panelHeight="'50%'" :panelWidth="'100%'" style="float:left" :titleStyle="{'height':titleHeight+'px','line-height':titleHeight+'px'}">
        <template v-slot:panelBody>
          <BarView></BarView>
        </template>
      </Panel>
    </div>
    <div id="right" class="block">
      <Panel :title="'全国各省市假期出行数据地图'" :panelHeight="'50%'" :panelWidth="'100%'" style="float:left" :titleStyle="{'height':titleHeight+'px','line-height':titleHeight+'px'}">
        <template v-slot:panelBody>
          <MapView></MapView>
        </template>
      </Panel>
      <Panel :title="'全国各景点简介文本统计词云图'" :panelHeight="'50%'" :panelWidth="'100%'" style="float:left" :titleStyle="{'height':titleHeight+'px','line-height':titleHeight+'px'}">
        <template v-slot:panelBody>
          <CloudView></CloudView>
        </template>
      </Panel>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-unused-vars,vue/no-unused-components */
import Panel from './components/panel';

import BarView from './components/bar';
import CloudView from './components/cloud';
import RankView from './components/rank';
import MapView from './components/map';


export default {
  name: 'App',
  components: {
    Panel,
    BarView,
    CloudView,
    RankView,
    MapView,
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
  text-align: center;
}
#main {
  height:959px;
  width: 1918px;
  position: fixed;
  left: 1px;
  top: 1px;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
}
.block {
  width: 50%;
  height: 100%;
}
</style>
