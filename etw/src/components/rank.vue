<template>
    <div id="rankMain" v-infinite-scroll="loadMore">
        <div class="rankBlock" id="rankLegend"></div>
    </div>
</template>
<script>
/* eslint-disable no-unused-vars,no-empty */
import * as d3 from 'd3';
import axios from 'axios';

export default {
    name: 'rankView',
    data() {
        return {
            data: null,
            amount: 20, // 默认排多少个
            scale: null,
            offset: { x: 60, y: 30 },
            size: { w: 800, h: 30},
        }
    },
    mounted() {
        // 获取数据
        axios.get('./旅游景点.json').then((res) => {
            var d = res.data;
            // 排序
            d.sort(function(a, b){ return b.sales - a.sales });
            this.data = d;
            console.log(this.data)
            // 初始化
            this.init(this.amount);
        })
    },
    methods: {
        init(amount) {
            const size = this.size;
            const offset = this.offset;
            const data = this.data;
            const scale = d3.scaleLinear().domain([0, this.getDomainMax(data[0].sales)]).range([0, size.w]);
            const div = d3.select("#rankMain");
            // 绘制坐标轴
            const svgLegend = d3.select("#rankLegend").append("svg")
                .attr("width", '100%')
                .attr("height", '100%');
            this.scale = scale;
            svgLegend.append('g').call(d3.axisTop(scale))
                .attr("transform", `translate(${offset.x}, ${offset.y})`)
                .attr("font-size", 15);
            // 绘制排名
            for(let i = 0; i < amount; i++) {
                var svg = div.append("div")
                    .attr("class", "rankBlock")
                    .style("width", "100%")
                    .style("height", "50px")
                    .append("svg")
                        .attr("width", "100%")
                        .attr("height", "100%");
                
            }
        },
        // 无限滚动依托
        loadMore() {

        },
        getDomainMax(n) {
            let l, c = -1;
            while(n) {
                l = n % 10;
                n = parseInt(n / 10);
                c += 1;
            }
            return (l + 1) * 10 ** c
        }
    }
}
</script>
<style scoped>
#rankMain {
    width: 100%;
    height: 100%;
    float: left;
    overflow: auto;
    font-family: monospace;
    /* background-color: chartreuse; */
}
.rankBlock {
    width: 100%;
    height: 50px;
}
</style>