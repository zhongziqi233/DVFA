<template>
    <div class="panel" :style="{'height':panelHeight,'width':panelWidth}" >
        <div class="title" :style="titleStyle" >
            <el-icon color="#333333" class="no-inherit">
                <Place />
            </el-icon>
            {{title}}
            <slot name="title"></slot>
        </div>
        <div class="panelBody" :style="{'height':'calc(100% - '+ titleStyle.height+')'} " ref="root">
            <slot name="panelBody"></slot>
        </div>
    </div>
</template>

<script>
export default {
    name:'PanelComponent',
    props:['title','panelHeight','panelWidth','titleHeight','titleStyle'],
}
</script>

<style scoped>
.panel {
    border: 1px solid #aaaaaa;
    box-sizing: border-box;
}
.title {
    width:100%;
    box-sizing: border-box;
    text-indent:10px;
    color: #333333dd;
    font-size: 1rem;
    font-weight: bolder;
    vertical-align: middle;
    background: rgb(236,240,243);
    text-align: left;
    border-bottom:1px solid #ccc;
}
.panelBody {
    width:100%;
    position: relative;
    box-sizing: border-box;
    border: 2px solid #ebebeb;
    background: #ffffff;
    border-top:none;
}
</style>